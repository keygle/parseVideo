# err.py, parse_video/pvdl/lib/

'''

Exception
    PvdlError
        UnknowError
        CallError
        ConfigError
        CheckError
        
        RetryableError
            ParseError
            DownloadError
        RetryError
        MergeError

'''

class PvdlError(Exception):
    pass

class UnknowError(PvdlError):
    pass
class CallError(PvdlError):
    pass
class ConfigError(PvdlError):
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


# end err.py


