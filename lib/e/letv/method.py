# method.py, parse_video/lib/e/letv/, method common code

import functools

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
try:
    from .o import m3u8_encrypt2 as m3u8_encrypt
except Exception:
    from .o import m3u8_encrypt

# NOTE support --more, try to enable more mode
def get_raw_more(method_arg_text):
    data_list = [	# NOTE --more mode to just get vid_info
        'vid_info', 
    ]
    raw_more = common.method_simple_check_use_more(var, method_arg_text, data_list)
    return raw_more

# try to get vid_info from more
def get_vid_info():
    # get vid_info from more if possible
    default_get_vid_info = functools.partial(common.parse_load_page_and_get_vid, var)
    vid_info = common.method_more_simple_get_vid_info(var, default_get_vid_info)
    return vid_info

# add --more data to out
def check_enable_more(out):
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = var._['_vid_info']
    return out

def dl_first_json(first_url):
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['statuscode'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['statuscode'], var))
    return first

def raw_first_get_base_info(first):
    playurl = first['playurl']
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = playurl['title']
    return out, playurl

# for process letv encrypt m3u8
def decode_m3u8(raw):
    return m3u8_encrypt.decode(raw)

def parse_m3u8(raw):	# parse letv's m3u8 file text
    # check raw text
    check_list = [
        '#EXTM3U', 
        '#EXT-X-VERSION:3', 
        '#EXT-LETV-M3U8-TYPE:VOD', 
        '#EXT-LETV-M3U8-VER:ver_00_22', 
    ]
    for c in check_list:
        if not c in raw:
            raise err.ParseError('letv m3u8 file format bad, not exist key value', c)
    lines = raw.splitlines()
    out = {}
    # parse head lines, get size_px
    out['size_px'] = [-1, -1]
    while len(lines) > 0:
        line, lines = lines[0], lines[1:]
        if line.startswith('#EXT-LETV-START-TIME:'):
            break
        elif line.startswith('#EXT-LETV-PIC-WIDTH:'):
            out['size_px'][0] = int(line.split(':', 1)[1])
        elif line.startswith('#EXT-LETV-PIC-HEIGHT:'):
            out['size_px'][1] = int(line.split(':', 1)[1])
    # get file info, use base m3u8 parse function
    out['file'] = b.simple_m3u8_parse(lines)
    for f in out['file']:	# get size from url
        filename = f['url'].split('?', 1)[0].rsplit('/', 1)[1]
        size = filename.split('_')[-3]	# NOTE fix this at 2016-01-24
        f['size'] = int(size)	# update size
    return out

# end method.py


