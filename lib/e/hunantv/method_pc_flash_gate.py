# method_pc_flash_gate.py, parse_video/lib/e/hunantv/
from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import mango_tv3

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # NOTE --more mode to direct get vid_info
    if _check_use_more():
        var._['_use_more'] = True
        raw_more = var._['more']
        # [ OK ] log
        log.o(log_text.method_enable_more())
        # check method (and method args)
        common.method_more_check_method(method_arg_text, raw_more)
    # process method args
    def rest(r):
        if r == 'parse_m3u8':
            var._['flag_parse_m3u8'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    
    # get vid_info from more
    if not var._['_use_more']:
        vid_info = common.parse_load_page_and_get_vid(var)
    else:
        raw_data = raw_more['_data']
        vid_info = raw_data['vid_info']
        # set var._
        var._['_vid_info'] = vid_info
    pvinfo = _get_video_info(vid_info)
    # NOTE select hd here
    common.method_select_hd(pvinfo, var)
    out = _get_file_urls(pvinfo)
    # TODO support parse m3u8 and count here
    
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = vid_info
    return out

def _check_use_more():
    data_list = [
        'vid_info', 
    ]
    return common.method_check_use_more(var, data_list)

def _get_video_info(vid_info):
    # make first url
    first_url = mango_tv3.gen_first_url(vid_info['vid'])
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['status'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['status'], var))
    return common.parse_raw_first(first, _parse_raw_first_json)

def _parse_raw_first_json(first):
    data = first['data']
    out = {}
    # get base video info
    info = data['info']
    out['info'] = {}
    out['info']['title'] = info['title']
    out['info']['title_short'] = info['collection_name']
    out['info']['title_sub'] = info['sub_title']
    out['info']['title_no'] = b.simple_get_number_from_text(info['series'])
    
    # get video list
    duration = float(info['duration'])
    stream = data['stream']
    out['video'] = []
    for s in stream:
        name = s['name']
        one = {}
        one['hd'] = var.TO_HD[name]
        # set default values
        one['format'] = 'm3u8'	# NOTE the type should be m3u8
        one['size_px'] = [-1, -1]
        one['size_byte'] = -1
        one['time_s'] = duration
        one['count'] = 1
        # add one file info, the m3u8 file
        one['file'] = []
        f = {}
        f['time_s'] = duration
        f['url'] = mango_tv3.gen_before_url(s['url'])
        one['file'].append(f)
        out['video'].append(one)
    return out

def _get_file_urls(pvinfo):
    def worker(f, i):
        raw = f['url']
        before = b.dl_json(raw)
        # check code
        if before['status'] != var.BEFORE_OK_CODE:
            raise err.MethodError('before code ' + b.str_or_str(before['status']) + ' is not ' + str(var.BEFORE_OK_CODE) + ' ')
        f['url'] = before['info']	# update URL
        return f
    pool_size = var._['pool_size']['get_before']
    return common.simple_get_file_urls(pvinfo, worker, msg='getting m3u8 file URLs', pool_size=pool_size)

# end method_pc_flash_gate.py


