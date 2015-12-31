# method_pc_flash_gate.py, parse_video/lib/e/bks1/

import re
import functools

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import mixer_remote
from .vv import vv_default

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # check --more mode
    data_list = [
        'vid_info', 
        'raw_first_json', 
    ]
    raw_more = common.method_simple_check_use_more(var, method_arg_text, data_list)
    # parse method args
    def rest(r):
        if r == 'set_um':
            var._['set_um'] = True
        elif r == 'set_vv':
            var._['set_vv'] = True
        elif r == 'set_flag_v':
            var._['flag_v'] = True
        elif r == 'fix_4k':
            var._['flag_fix_4k'] = True
        else:	# unknow method arg
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    # get vid_info from more if possible
    default_get_vid_info = functools.partial(common.parse_load_page_and_get_vid, var, _get_vid_info)
    vid_info = common.method_more_simple_get_vid_info(var, default_get_vid_info)
    
    # check use more mode to get raw_first_json
    if not var._['_use_more']:
        pvinfo = _get_video_info(vid_info)
    else:
        var._['_raw_first_json'] = raw_more['_data']['raw_first_json']	# set var._
        pvinfo = _get_video_info_2(var._['_raw_first_json'])	# just parse vms json info
    # check flag_v mode
    if var._['flag_v']:
        pvinfo = vv_default.add_tokens(pvinfo, vid_info)
    out = _get_file_urls(pvinfo)
    # check enable_more
    if var._['enable_more']:	# add more info
        out['_data'] = {}
        out['_data']['vid_info'] = vid_info
        out['_data']['raw_first_json'] = var._['_raw_first_json']
    return out

# TODO may be can clean here
def _get_vid_info(raw_html_text):
    def do_get(raw_html_text):
        out = common.method_vid_re_get(raw_html_text, var.RE_VID_LIST)
        # convert flag_vv
        to_flag_vv = {
            'true' : True, 
            'false' : False, 
        }
        out['flag_vv'] = to_flag_vv.get(out['flag_vv'], None)
        # get aid
        for key, r in var.RE_VID_LIST2.items():
            try:
                out[key] = re.findall(r, raw_html_text)[0]
            except Exception as e:	# NOTE just ignore Error
                out['key'] = ''	# set empty value
                # WARNING log
                log.w('vid_info [' + key + '] empty ')
        return out
    return common.method_get_vid_info(raw_html_text, var, do_get)

def _get_video_info(vid_info):
    # check flag_v mode
    if var._['flag_v']:
        first_url = vv_default.make_first_url(vid_info)
        log.o(log_text.method_got_first_url(first_url, prefix='flag_v, '))
    else:
        first_url = _make_first_url(vid_info)
        # [ OK ] log, load first vms info json
        log.o(log_text.method_got_first_url(first_url))
    # check fix_4k
    if var._['flag_fix_4k']:
        first_url = _first_url_fix_4k(first_url)
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['code'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['code'], var))
    # parse raw_vms json
    return _get_video_info_2(first)

def _first_url_fix_4k(raw):
    return raw.split('&src=', 1)[0] + '&' + raw.split('&src=', 1)[1].split('&', 1)[1]

def _get_video_info_2(first):
    pvinfo = common.parse_raw_first(first, _parse_raw_first_info)
    # select by hd_min, hd_max, i_min, i_max. count sum data, and sort videos by hd
    out = common.method_simple_count_and_select(pvinfo, var)
    return out

def _make_first_url(vid_info):
    tvid = vid_info['tvid']
    vid = vid_info['vid']
    
    set_um = var._['set_um']
    set_vv = var._['set_vv']
    
    out = mixer_remote.get_request(tvid, vid, flag_set_um=set_um, flag_set_vv=set_vv)
    return out

def _parse_raw_first_info(first):
    out = {}
    data = first['data']
    # get base video info
    vi = data['vi']
    out['info'] = {}
    
    out['info']['title'] = vi['vn']
    out['info']['title_sub'] = vi['subt']
    out['info']['title_short'] = vi['an']
    out['info']['title_no'] = vi['pd']
    # get video list
    vp = data['vp']
    du = vp['du']	# before final url, base part
    raw_list = vp['tkl'][0]['vs']
    
    out['video'] = [_parse_one_video_info(r, du) for r in raw_list]
    return out

def _parse_one_video_info(raw, du):
    bid = raw['bid']
    out = {}
    out['hd'] = var.TO_HD[bid]
    out['size_px'] = common.method_get_size_px(*raw['scrsz'].split('x'))
    out['format'] = 'flv'	# NOTE the video file format shoud be flv
    
    # get file list
    raw_list = raw['fs']
    out['file'] = [_parse_one_file_info(r, du) for r in raw_list]
    return out

def _parse_one_file_info(raw, du):
    out = {}
    out['size'] = raw['b']
    out['time_s'] = raw['d'] / 1e3
    
    l = raw['l']
    out['url'] = du + l	# NOTE before final url, just concat 'du' and 'l'
    return out

def _get_file_urls(pvinfo):
    def worker(f, i):
        raw_info = b.dl_json(f['url'])
        try:
            f['url'] = raw_info['l']	# update url
            return f
        except Exception as e:
            er = err.MethodError('get final file URL failed', f['url'])
            raise er from e
    pool_size = var._['pool_size']['get_file_url']
    return common.simple_get_file_urls(pvinfo, worker, msg='getting part file URLs', pool_size=pool_size)

# end method_pc_flash_gate.py


