# err.py, parse_video/o/plist/lib/
'''

Exception
    PlistError
        UnknowError
        ConfigError
            NotSupportURLError
        
        ParseError
            NetworkError
            DecodingError
            ParseJSONError
            ParseXMLError
            ParseHTMLError
            
            MethodError

TODO
'''

class PlistError(Exception):
    pass

class UnknowError(PlistError):
    pass
class ConfigError(PlistError):
    pass
class ParseError(PlistError):
    pass

class NotSupportURLError(ConfigError):
    pass

class NetworkError(ParseError):
    pass
class DecodingError(ParseError):
    pass
class ParseJSONError(ParseError):
    pass
class ParseXMLError(ParseError):
    pass
class ParseHTMLError(ParseError):
    pass
class MethodError(ParseError):
    pass

# end err.py


