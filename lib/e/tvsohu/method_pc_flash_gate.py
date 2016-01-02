# method_pc_flash_gate.py, parse_video/lib/e/tvsohu/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method
from .o import main

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    method.get_raw_more(method_arg_text)
    # process method args
    def rest(r):
        if r == 'fast_parse':
            var._['flag_fast_parse'] = True
        elif r == 'gen_header':
            var._['flag_gen_header'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    vid_info = method.get_vid_info()
    
    pvinfo = method.get_video_info(vid_info, _gen_one_before_url)
    pvinfo = method.count_and_select(pvinfo)	# NOTE count and select
    out = _get_file_urls(pvinfo)
    # NOTE add headers
    out = _add_headers(out)
    out = method.check_enable_more(out)
    return out

def _gen_one_before_url(su_i, vid, tvid, ch):
    return main.gen_before_url(su_i, vid, tvid, ch)

def _get_file_urls(pvinfo):
    def worker(f, i):
        raw = b.dl_json(f['url'])
        try:
            f['url'] = raw['url']	# update URL
            return f
        except Exception as e:
            er = err.MethodError('get final file URL failed', f['url'])
            raise er from e
    pool_size = var._['pool_size']['get_final']
    return common.simple_get_file_urls(pvinfo, worker, msg='getting part file URLs', pool_size=pool_size)

def _add_headers(pvinfo):
    # NOTE add type and user_agent header for each file
    user_agent = main.gen_user_agent()
    file_type = var.TVSOHU_FILE_TYPE
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                f['header'] = {
                    'User-Agent' : user_agent, 
                }
                f['type'] = file_type
    # NOTE support gen_header method arg
    if var._['flag_gen_header']:
        for v in pvinfo['video']:
            for f in v['file']:
                if f['url'] != '':	# NOTE Range only for example
                    f['header']['Range'] = 'bytes=0-' + str(f['size'] - 1)
    return pvinfo

# end method_pc_flash_gate.py


