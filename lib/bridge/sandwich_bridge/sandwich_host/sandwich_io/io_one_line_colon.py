# io_one_line_colon.py, parse_video/lib/bridge/sandwich_bridge/sandwich_host/sandwich_io/

def _encode(raw):
    out = (':').join([_encode_part(i) for i in (raw[:] + [''])]) + '\n'
    return out

# _encode_part(raw :str) -> str
def _encode_part(raw):
    encode_char = {
        '\\' : '\\\\', 
        ':' : '\\:', 
        '\n' : '\\n', 
    }
    out = ('').join([encode_char.get(i, i) for i in str(raw)])
    return out

def _decode(raw):
    # NOTE try to remove \n after raw str
    raw = str(raw)
    if (len(raw) > 0) and (raw[-1] == '\n'):
        raw = raw[:-1]
    
    decode_char = {
        'n' : '\n', 
        # NOTE other chars decode to itself, \: -> :, \\ -> \
    }
    out = []
    flag_decode = False	# decode \ char
    one = ''	# one part
    # scan each char
    for i in raw:
        if flag_decode:
            one += decode_char.get(i, i)
            flag_decode = False
        else:
            if i == '\\':
                flag_decode = True
            elif i == ':':	# reset part here
                out.append(one)
                one = ''
            else:	# normal char here
                one += i
    # NOTE no add last part here
    return out

# io_one_line_colon exports
encode = _encode	# encode(raw :[]) -> str
decode = _decode	# decode(raw :str) -> []
# end io_one_line_colon.py


