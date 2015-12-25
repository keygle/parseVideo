# err.py, parse_video/lib/

'''

Error class for parse_video

Exception			# python 3 base Error class
    PVError			# parse_video Error
        UnknowError
        NotSupportURLError	# not support the given URL
        ConfigError		# config item or user input error
        
        ParseError		# parse video info Error
            NetworkError	# download network resources failed
            DecodingError	# decode blob data to text failed
            ParseJSONError	# parse json text failed (json text format error)
            ParseXMLError	# parse xml text failed (xml text format error)
            
            MethodError		# parse method Error (maybe out-of-date)

'''

class PVError(Exception):
    pass

class UnknowError(PVError):
    pass
class NotSupportURLError(PVError):
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

# end err.py


