# method_pc_flash_gate.py, parse_video/lib/e/hunantv/
from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import mango_tv3

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # TODO support --more
    # process method args
    def rest(r):
        if r == 'parse_m3u8':
            var._['flag_parse_m3u8'] = True
        elif r == 'fast_parse':
            var._['fast_parse'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    
    vid_info = common.parse_load_page_and_get_vid(var)
    pvinfo = _get_video_info(vid_info)
    # TODO support fast parse here
    out = _get_file_urls(pvinfo)
    # TODO support parse m3u8 and count and select here
    return out

def _get_video_info(vid_info):
    pass

def _get_file_urls(pvinfo):
    pass

# end method_pc_flash_gate.py


