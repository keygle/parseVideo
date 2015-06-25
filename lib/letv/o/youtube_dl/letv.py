# -*- coding: utf-8 -*-
# letv.py, part for parse_vidoe: a fork of parseVideo. 
# letv: lib/letv/o/youtube_dl/letv, letv support, get real urls. 

# import

from .compat import (
    compat_urllib_parse,	# NOTE used
    compat_urlparse,		# NOTE used
)

from .utils import (
    determine_ext,	# NOTE used
)

# base functions

def urshift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n

# ror() and calc_time_key() are reversed from a embedded swf file in KLetvPlayer.swf
def ror(param1, param2):
    _loc3_ = 0
    while _loc3_ < param2:
        param1 = urshift(param1, 1) + ((param1 & 1) << 31)
        _loc3_ += 1
    return param1

def calc_time_key(param1):
    _loc2_ = 773625421
    _loc3_ = ror(param1, _loc2_ % 13)
    _loc3_ = _loc3_ ^ _loc2_
    _loc3_ = ror(_loc3_, _loc2_ % 17)
    return _loc3_

# functions
def get_real_url(domain, dispatch_format_id):
    # get a raw final url, ready to process it
    media_url = domain[0] + dispatch_format_id[0]
    
    # Mimic what flvxz.com do
    url_parts = list(compat_urlparse.urlparse(media_url))
    qs = dict(compat_urlparse.parse_qs(url_parts[4]))
    qs.update({
        'platid': '14',
        'splatid': '1401',
        'tss': 'no',
        'retry': 1
    })
    url_parts[4] = compat_urllib_parse.urlencode(qs)
    media_url = compat_urlparse.urlunparse(url_parts)
    
    # get file ext
    ext_name = determine_ext(dispatch_format_id[1])
    
    # get final url done
    info = {}
    info['url'] = media_url
    info['ext'] = ext_name	# file ext, may be 'mp4'
    return info

# end letv.py


