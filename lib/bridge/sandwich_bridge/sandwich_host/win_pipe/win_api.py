# win_api.py, parse_video/lib/bridge/sandwich_bridge/sandwich_host/win_pipe/
# test201602111157

import ctypes

# import parts from ctypes
_WinError = ctypes.WinError
_c_uint = ctypes.c_uint
_c_wchar_p = ctypes.c_wchar_p
_c_void_p = ctypes.c_void_p
_byref = ctypes.byref
_create_string_buffer = ctypes.create_string_buffer

# load dlls
_kernel32 = ctypes.windll.kernel32

# consts used for windows API

_INVALID_HANDLE_VALUE = -1

# for CreateNamedPipe
_PIPE_ACCESS_DUPLEX = 0x00000003	# open_mode
_PIPE_ACCESS_INBOUND = 0x00000001
_PIPE_ACCESS_OUTBOUND = 0x00000002
_FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000
_FILE_FLAG_WRITE_THROUGH = 0x80000000
_FILE_FLAG_OVERLAPPED = 0x40000000
_WRITE_DAC = 0x00040000		# TODO 0x00040000L with L
_WRITE_OWNER = 0x00080000
_ACCESS_SYSTEM_SECURITY = 0x01000000
_PIPE_TYPE_BYTE = 0x00000000	# pipe_mode
_PIPE_TYPE_MESSAGE = 0x00000004
_PIPE_READMODE_BYTE = 0x00000000
_PIPE_READMODE_MESSAGE = 0x00000002
_PIPE_WAIT = 0x00000000
_PIPE_NOWAIT = 0x00000001
_PIPE_ACCEPT_REMOTE_CLIENTS = 0x00000000
_PIPE_REJECT_REMOTE_CLIENTS = 0x00000008
_PIPE_UNLIMITED_INSTANCES = 255	# max_instance

# structs used for windows API

# make pipe name from given raw pipe name to windows format
def make_pipe_name(raw_pipe_name):
    pipe_name = '\\\\.\\pipe\\' + raw_pipe_name	# \\.\pipe\pipename
    return pipe_name

# base windows API functions, in kernel32.dll

# CloseHandle
def CloseHandle(handle):
    _CloseHandle(handle)

def _ret_checker_CloseHandle(value):
    if value == 0:
        raise _WinError()
    return None

# CreateNamedPipe
def CreateNamedPipe(pipe_name, 
        # default flag allow read and write through pipe, and only allow 1 instance
        open_mode = _PIPE_ACCESS_DUPLEX | _FILE_FLAG_FIRST_PIPE_INSTANCE, 
        # default flag set pipe type to byte and reject remote connect
        pipe_mode = _PIPE_TYPE_BYTE | _PIPE_REJECT_REMOTE_CLIENTS, 
        max_instance=1, 
        out_buffer_size=0, 
        in_buffer_size=0, 
        default_timeout=0):
    return _CreateNamedPipe(pipe_name, open_mode, pipe_mode, max_instance, out_buffer_size, in_buffer_size, default_timeout, None)

def _ret_checker_CreateNamedPipe(value):
    if value == _INVALID_HANDLE_VALUE:
        raise _WinError()
    return value

# ConnectNamedPipe
def ConnectNamedPipe(pipe_handle):
    return _ConnectNamedPipe(pipe_handle, None)

def _ret_checker_ConnectNamedPipe(value):
    if value == 0:
        raise _WinError()
    return None

# ReadFile
def ReadFile(handle, size=1):
    if size < 1:
        return None
    # create buffer to receive data
    data_buffer = _create_string_buffer(size)
    readed = _c_uint()
    _ReadFile(handle, data_buffer, size, _byref(readed), None)
    # get readed file
    data = data_buffer.value[:readed.value]
    return data

def _ret_checker_ReadFile(value):
    if value == 0:
        raise _WinError()
    return None

# WriteFile
def WriteFile(handle, data=None):
    if data == None:
        return
    written = _c_uint()	# number of bytes written
    _WriteFile(handle, data, len(data), _byref(written), None)
    return written.value

def _ret_checker_WriteFile(value):
    if value == 0:
        raise _WinError()
    return None

# load dll functions, and init them

# CloseHandle
_CloseHandle = _kernel32.CloseHandle
_CloseHandle.argtypes = [
    _c_uint, 	# object handle
]
_CloseHandle.restype = _ret_checker_CloseHandle

# CreateNamedPipe
_CreateNamedPipe = _kernel32.CreateNamedPipeW
_CreateNamedPipe.argtypes = [
    _c_wchar_p, 	# pipe_name
    _c_uint, 		# open_mode
    _c_uint, 		# pipe_mode
    _c_uint, 		# max_instance
    _c_uint, 		# out_buffer_size
    _c_uint, 		# in_buffer_size
    _c_uint, 		# default_timeout
    _c_void_p, 		# security_attributes, TODO not support this now
]
_CreateNamedPipe.restype = _ret_checker_CreateNamedPipe

# ConnectNamedPipe
_ConnectNamedPipe = _kernel32.ConnectNamedPipe
_ConnectNamedPipe.argtypes = [
    _c_uint, 		# handle of named_pipe
    _c_void_p, 		# overlapped, TODO not support this now
]
_ConnectNamedPipe.restype = _ret_checker_ConnectNamedPipe

# ReadFile
_ReadFile = _kernel32.ReadFile
_ReadFile.argtypes = [
    _c_uint, 		# handle of the file
    _c_void_p, 		# buffer for readed data
    _c_uint, 		# number of bytes to read
    _c_void_p, 		# number of bytes readed
    _c_void_p, 		# overlapped, TODO not support this now
]
_ReadFile.restype = _ret_checker_ReadFile

# WriteFile
_WriteFile = _kernel32.WriteFile
_WriteFile.argtypes = [
    _c_uint, 		# handle of the file
    _c_void_p, 		# buffer of the bytes
    _c_uint, 		# number of bytes to write
    _c_void_p, 		# number of bytes written
    _c_void_p, 		# overlapped, TODO not support this now
]
_WriteFile.restype = _ret_checker_WriteFile

# end win_api.py


