# err.py, parse_video/pvdl/lib/

'''

Exception
    PvdlError
        UnknowError
        ConfigError
        CallError
        ExitCodeError
        CheckError
        
        RetryableError
            ParseError
            DownloadError
        RetryError
        MergeError
        
        DecodingError
        ParseJSONError

'''

class PvdlError(Exception):
    pass

class UnknowError(PvdlError):
    pass
class ConfigError(PvdlError):
    pass
class CallError(PvdlError):
    pass
class ExitCodeError(PvdlError):
    pass
class CheckError(PvdlError):
    pass

class RetryableError(PvdlError):
    pass
class ParseError(RetryableError):
    pass
class DownloadError(RetryableError):
    pass
class RetryError(PvdlError):
    pass

class MergeError(PvdlError):
    pass

class DecodingError(PvdlError):
    pass
class ParseJSONError(PvdlError):
    pass

# end err.py


