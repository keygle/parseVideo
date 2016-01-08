# method_flvsp.py, parse_video/lib/e/letv/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method
from .o import id_transfer
from .vv import vv_default

# global data
FLVSP_PLATID = 1
FLVSP_SPLATID = 104

# method_flvsp.parse(), entry function
def parse(method_arg_text):
    raw_more = method.get_raw_more(method_arg_text)
    # process method args
    def rest(r):
        if r == 'set_flag_v':	# TODO DEBUG here
            var._['flag_v'] = True
        else:	# unknow args
        return True
    common.method_parse_method_args(method_arg_text, var, rest)
    
    vid_info = method.get_vid_info()
    pvinfo = _get_video_info(vid_info)
    # NOTE there is no need to get file URLs, already got
    # check flag_v
    if var._['flag_v']:
        pvinfo = _add_args(pvinfo)
    common.method_simple_count(pvinfo)	# NOTE just count, not select
    # remove _data in video
    for v in pvinfo:
        if '_data' in v:
            v.pop('_data')
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
        # NOTE add _data
        one['_data'] = {
            'filename' : raw[1], 
        }
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

# add args for vv
def _add_args(pvinfo):
    # INFO log
    log.i('adding args for vv ')
    # TODO clean code here
    # TODO use map_do() here
    # TODO Error process
    pid = var._['_vid_info']['pid']
    for v in pvinfo['video']:
        if not '_data' in v:
            continue
        d = v['_data']
        filename = d['filename']
        f = v['file'][0]
        f['url'] = vv_default.make_one_url(f['url'], pid, filename)
    return pvinfo

# end method_flvsp.py


