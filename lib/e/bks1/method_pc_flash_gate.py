# method_pc_flash_gate.py, parse_video/lib/e/bks1/
from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import mixer_remote
from .vv import vv_default

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # check --more mode
    if _check_use_more():
        var._['_use_more'] = True
        raw_more = var._['more']
        # [ OK ] log
        log.o('--more mode enabled ')
        # TODO check method match
        # check method args match
        raw_method_arg = common.entry_split_method(raw_more['method'])[1]
        if raw_method_arg != method_arg_text:
            method_text_1 = common.method_str_method_arg(raw_method_arg)
            method_text_2 = common.method_str_method_arg(method_arg_text)
            # WARNING log
            log.w('now method args ' + method_text_2 + ' is different from old method args ' + method_text_1 + ' in more info ')
    # parse method args
    def rest(r):
        if r == 'set_um':
            var._['set_um'] = True
        elif r == 'set_vv':
            var._['set_vv'] = True
        elif r == 'set_flag_v':
            var._['flag_v'] = True
        else:	# unknow method arg
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    
    # check use more mode
    if not var._['_use_more']:
        vid_info = common.parse_load_page_and_get_vid(var, _get_vid_info)
        pvinfo = _get_video_info(vid_info)
    else:
        raw_data = raw_more['_data']
        vid_info = raw_data['vid_info']
        raw_first_json = raw_data['raw_first_json']
        # set var._
        var._['_vid_info'] = vid_info
        var._['_raw_first_json'] = raw_first_json
        # just parse vms json info
        pvinfo = _get_video_info_2(raw_first_json)
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

# return True to use more mode
def _check_use_more():
    data_list = [
        'vid_info', 
        'raw_first_json', 
    ]
    return common.method_check_use_more(var, data_list)

def _get_vid_info(raw_html_text):
    def do_get(raw_html_text):
        out = common.method_vid_re_get(raw_html_text, var.RE_VID_LIST)
        # convert flag_vv
        to_flag_vv = {
            'true' : True, 
            'false' : False, 
        }
        out['flag_vv'] = to_flag_vv.get(out['flag_vv'], None)
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
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['code'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['code'], var))
    # parse raw_vms json
    return _get_video_info_2(first)

def _get_video_info_2(first):
    pvinfo = common.parse_raw_first(first, _parse_raw_first_info)
    out = _count_and_select(pvinfo)
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

# select by hd_min, hd_max, i_min, i_max. count sum data, and sort videos by hd
def _count_and_select(pvinfo):
    return common.method_simple_count_and_select(pvinfo, var)

def _get_file_urls(pvinfo):
    # TODO maybe retry here
    # make task raw list
    raw = []
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                one = {}
                one['i'] = i	# add index number for DEBUG
                i += 1
                one['url'] = f['url']	# raw url
                raw.append(one)	# add one task
    # use map_do() to get many file_urls at the same time
    pool_size = var._['pool_size']['get_file_url']
    # INFO log
    log.i('getting ' + str(len(raw)) + ' part file URLs, pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(raw, worker = _get_one_file_url, pool_size=pool_size)
    # DEBUG log
    log.d('got file URLs done. ')
    # set back real file urls
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                f['url'] = result[i]
                i += 1
    # done
    return pvinfo

def _get_one_file_url(raw):
    i = raw['i']
    # DEBUG log
    log.d('start get index ' + str(i) + ' ')
    
    raw_info = b.dl_json(raw['url'])
    try:
        result = raw_info['l']
    except Exception as e:
        er = err.MethodError('get final file URL failed', raw['url'])
        raise er from e
    # DEBUG log
    log.d('[done] got index ' + str(i) + ' ')
    return result

# end method_pc_flash_gate.py


