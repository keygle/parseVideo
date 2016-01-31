# method_m3u8.py, parse_video/lib/e/letv/

from ... import err, b
from ...b import log
from .. import common

from .var import var
from . import method

# method_m3u8.parse(), entry function
def parse(method_arg_text):
    # NOTE not support method args
    # TODO WARNING (not support method arg) here
    
    # get m3u8 blob data
    m3u8_blob = _get_raw_m3u8(var._['_raw_url'])
    # parse m3u8 to get video info
    pvinfo = _do_parse_one_m3u8(m3u8_blob)
    # count it
    common.method_count_video(pvinfo)
    # NOTE not support enable_more here
    return pvinfo

def _get_raw_m3u8(raw_url):
    # check download m3u8 file
    if raw_url.startswith('http://'):
        # INFO log
        log.i('downloading m3u8 file \"' + raw_url + '\" ')
        blob = b.dl_blob(raw_url)
        return blob
    # check local m3u8 file
    if not raw_url.startswith('file:///'):
        raise err.NotSupportURLError('not support this url', raw_url)
    # INFO log
    log.i('loading local m3u8 file \"' + raw_url + '\" ')
    try:	# try to open file
        fpath = raw_url.split('file://', 1)[1]
        with open(fpath, 'rb') as f:
            blob = f.read()
    except OSError:	# try remove / in fpath
        if fpath[0] == '/':
            fpath = fpath[1:]
        with open(fpath, 'rb') as f:
            blob = f.read()
    return blob

def _do_parse_one_m3u8(raw):
    # INFO log
    log.i('decoding m3u8 file ')
    try:	# decode raw m3u8 data
        m3u8_text = method.decode_m3u8(raw)
    except Exception as e:
        er = err.DecodingError('can not decode raw m3u8 data')
        raise er from e
    # parse m3u8 text to get raw video info
    try:
        v = method.parse_m3u8(m3u8_text)
    except Exception as e:
        er = err.ParseError('parse m3u8 text failed')
        raise er from e
    # add hd, format
    v['hd'] = _get_hd_from_px(v['size_px'])
    v['format'] = 'ts'	# NOTE file format here should be ts
    # create pvinfo
    out = {}
    out['info'] = {}
    out['info']['title'] = '[unknow video]'	# NOTE unknow video title
    out['video'] = [v]
    common.method_sort_video(out)
    return out

def _get_hd_from_px(size_px):
    x = size_px[0]
    if x > 3500:
        hd = 7	# 4K
    elif x > 1600:
        hd = 4	# 1080p
    elif x > 1100:
        hd = 2	# 720p
    else:
        hd = 0	# base quality
    return hd

# end method_m3u8.py


