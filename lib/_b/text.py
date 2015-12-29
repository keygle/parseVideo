# text.py, parse_video/lib/_b/, text process functions

from .. import err

def str_or_str(raw):
    '''
    if raw is str, add "" around it
    '''
    if isinstance(raw, str):
        return ('\"' + raw + '\"')
    return str(raw)

def _split_semicolon(raw):
    if ';' in raw:
        return raw.split(';', 1)
    return raw, None

def split_raw_extractor(raw_extractor):
    extractor, extractor_arg_text = _split_semicolon(raw_extractor)
    return extractor, extractor_arg_text

def split_raw_method(raw_method):
    method, method_arg_text = _split_semicolon(raw_method)
    return method, method_arg_text

def simple_get_number_from_text(raw):
    n = ('').join([i for i in raw if i.isdigit()])
    return int(n)

def simple_m3u8_parse(lines):
    out = []
    one = {}
    for line in lines:
        if (not line.startswith('#')) and (line.strip() != ''):
            # got URL line, append to out and reset one
            one['url'] = line
            out.append(one)
            one = {}
        elif line.startswith('#EXTINF:'):	# got time_s line
            time = line.split(':', 1)[1].split(',', 1)[0]
            one['time_s'] = float(time)
        elif line.startswith('#EXT-X-ENDLIST'):	# got m3u8 file end
            return out
    # not get m3u8 end
    raise err.ParseError('not get m3u8 file end #EXT-X-ENDLIST ')

# end text.py


