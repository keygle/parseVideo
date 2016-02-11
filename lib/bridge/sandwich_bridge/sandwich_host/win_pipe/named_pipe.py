# named_pipe.py, parse_video/lib/bridge/sandwich_bridge/sandwich_host/win_pipe/

from . import win_api

class NamedPipeServer(object):
    '''
    create a NamedPipe
    
    default without cache, no need to flush
    '''
    def __init__(self, pipe_name):
        self._handle = None	# handle of the NamedPipe
        
        self.pipe_name = pipe_name
        self._real_pipe_name = win_api.make_pipe_name(pipe_name)
        
        # create the named pipe
        self._handle = win_api.CreateNamedPipe(self._real_pipe_name)
    
    # base operations
    def close(self):
        win_api.CloseHandle(self._handle)
    
    def flush(self):
        pass	# NOTE nothing todo
    
    # accept NamedPipe connect from client
    def accept(self):
        win_api.ConnectNamedPipe(self._handle)
        # NOTE this will wait until connect
    
    # main operations
    def read(self, size=1):
        '''
        read bytes
        '''
        return win_api.ReadFile(self._handle, size=size)
    
    def write(self, data=None):
        '''
        write bytes
        '''
        # check input data, must be bytes
        if not isinstance(data, bytes):
            # if str, auto encode with utf-8
            if isinstance(data, str):
                data = data.encode('utf-8')
            else:
                raise TypeError('data to write must be bytes')
        return win_api.WriteFile(self._handle, data=data)
    
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

# open a NamedPipe
def open_named_pipe(pipe_name):
    real_pipe_name = win_api.make_pipe_name(pipe_name)
    # use open()
    pipe = open(real_pipe_name, mode='r+b', buffering=0)
    return pipe

# end named_pipe.py


