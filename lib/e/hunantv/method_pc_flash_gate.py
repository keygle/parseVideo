# method_pc_flash_gate.py, parse_video/lib/e/hunantv/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method
from .o import mango_tv3

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    method.get_raw_more(method_arg_text)
    # process method args
    def rest(r):
        if r == 'parse_m3u8':
            var._['flag_parse_m3u8'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    vid_info = method.get_vid_info()
    
    pvinfo = method.get_video_info(vid_info, _parse_raw_first_json)
    # NOTE select hd here
    common.method_select_hd(pvinfo, var)
    out = _get_file_urls(pvinfo)
    # TODO support parse m3u8 and count here
    out = method.check_enable_more(out)
    return out

def _parse_raw_first_json(first):
    out, data, info = method.raw_first_get_base_info(first)
    # get video list
    duration, stream = float(info['duration']), data['stream']
    out['video'] = []
    for s in stream:
        one = {}
        one['hd'] = var.TO_HD[s['name']]
        # set default values
        one['format'] = 'm3u8'	# NOTE the type should be m3u8
        one['size_px'] = [-1, -1]
        one['size_byte'] = -1
        one['time_s'] = duration
        one['count'] = 1
        # add one file info, the m3u8 file
        one['file'] = []
        f = {}
        f['size'] = -1
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


