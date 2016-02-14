# -*- coding: utf-8 -*-
# __init__.py, wuyan4/sandwich_bridge/win_pipe, support windows' named pipe for python3 with ctypes 
# LICENSE GNU GPLv3+, sceext <sceext@foxmail.com> 
# version 0.1.1.0 test201510031741

from . import b as _b

# main named_pipe_server class, to create a named pipe
class NamedPipeServer(object):
    '''
    NOTE default with no cache, no need to flush
    '''
    def __init__(self, pipe_name):
        self._handle = None	# handle of the NamedPipe
        
        self.pipe_name = pipe_name
        self._real_pipe_name = _b.make_pipe_name(pipe_name)
        
        # create the named pipe
        self._handle = _b.CreateNamedPipe(self._real_pipe_name)
    
    # base operation methods
    def close(self):
        _b.CloseHandle(self._handle)
    
    def flush(self):
        pass	# NOTE nothing to do
    
    # accept NamedPipe connect for pipe server
    def accept(self):
        _b.ConnectNamedPipe(self._handle)
    
    # main operation methods
    def read(self, size=1):
        '''
        read bytes
        '''
        return _b.ReadFile(self._handle, size=size)
    
    def write(self, data=None):
        '''
        write bytes
        '''
        # check input data, must be bytes
        if not isinstance(data, bytes):
            # if is str, will auto encode with utf-8
            if isinstance(data, str):
                data = data.encode('utf-8')
            else:
                raise TypeError('data to write must be bytes')
        return _b.WriteFile(self._handle, data=data)
    
    # convenient methods
    def readline(self):
        buffer = []
        while True:
            data = self.read(1)
            buffer.append(data)
            if data == b'\n':
                break
        out = (b'').join(buffer)
        return out
    
    # end NamedPipeServer class

# function to open a named_pipe
def open_named_pipe(pipe_name):
    real_pipe_name = _b.make_pipe_name(pipe_name)
    # just use the default open() function
    pipe = open(real_pipe_name, mode='r+b', buffering=0)
    return pipe

# end __init__.py


