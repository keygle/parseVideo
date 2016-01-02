# method_flvsp.py, parse_video/lib/e/letv/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method
from .o import id_transfer

# global data
FLVSP_PLATID = 1
FLVSP_SPLATID = 104

# method_flvsp.parse(), entry function
def parse(method_arg_text):
    raw_more = method.get_raw_more(method_arg_text)
    # process method args
    def rest(r):
        return True	# NOTE no more args
    common.method_parse_method_args(method_arg_text, var, rest)
    
    vid_info = method.get_vid_info()
    pvinfo = _get_video_info(vid_info)
    # NOTE there is no need to get file URLs, already got
    common.method_simple_count(pvinfo)	# NOTE just count, not select
    out = method.check_enable_more(pvinfo)
    return out

def _get_video_info(vid_info):
    # make first_url
    first_url = id_transfer.get_url(vid_info['vid'], platid=FLVSP_PLATID, splatid=FLVSP_SPLATID)
    first = method.dl_first_json(first_url)
    return common.parse_raw_first(first, _parse_raw_first_json)

def _parse_raw_first_json(first):
    out, playurl = method.raw_first_get_base_info(first)
    # get video list
    domain, dispatch = playurl['domain'], playurl['dispatch']
    
    out['video'] = []
    for rateid, raw in dispatch.items():
        one = {}
        one['hd'] = var.TO_HD[rateid]
        # set default values
        one['size_px'] = [-1, -1]
        one['format'] = 'mp4'	# NOTE file format here should be mp4
        
        # get the only one file URL
        one['file'] = []
        f = {}
        f['time_s'], f['size'] = _get_file_info(raw[1])
        raw_url = domain[0] + raw[0]
        f['url'] = _gen_one_file_url(raw_url)
        
        one['file'].append(f)
        out['video'].append(one)
    return out

def _get_file_info(raw):
    raw = raw.rsplit('/', 1)[1].rsplit('.', 1)[0]
    p = raw.split('-')
    time, size = p[-4], p[-3]
    time_s = int(time) / 1e3
    return time_s, int(size)

def _gen_one_file_url(raw):
    # NOTE replace '&tss=ios&' to '&tss=no&'
    a, b = raw.split('&tss=', 1)
    out = a + '&tss=no&' + b.split('&', 1)[1]
    return out

# end method_flvsp.py


