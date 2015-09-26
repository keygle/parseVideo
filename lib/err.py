# err.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.3.0 test201509261820

'''
ERRORs define and process of parse_video

ERROR class defined by parse_video

    Exception
        PVError				# parse_video's ERROR
            UnknowError
            NotSupportURLError		# not support the input raw_url
            LoadConfigError		# read and load config file failed
            ConfigError			# config item or user input error
            
            ParseError			# parse video info failed
                NetworkError		# network Error when loading web resources
                DecodingError		# decode blob data to text failed
                ParseJSONError		# parse json text download from network failed
                ParseXMLError		# parse xml text download from network failed
                
                MethodError		# the parse method used to parse video info may be not right
                			# this can be raised when the parse method is too old to work

'''

import traceback

# parse_video's base Error class
class PVError(Exception):
    pass
# other ERRORs defined by parse_video
class UnknowError(PVError):
    pass
class NotSupportURLError(PVError):
    pass
class LoadConfigError(PVError):
    pass
class ConfigError(PVError):
    pass
class ParseError(PVError):
    pass
class NetworkError(ParseError):
    pass
class DecodingError(ParseError):
    pass
class ParseJSONError(ParseError):
    pass
class ParseXMLError(ParseError):
    pass
class MethodError(ParseError):
    pass

# TODO

# end err.py


