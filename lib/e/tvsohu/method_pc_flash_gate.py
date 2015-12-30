# method_pc_flash_gate.py, parse_video/lib/e/tvsohu/

import functools

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import main

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # TODO support --more
    # process method args
    def rest(r):
        if r == 'fast_parse':
            var._['flag_fast_parse'] = True
        elif r == 'gen_header':
            var._['flag_gen_header'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    # TODO get vid_info and first info from --more mode
    
    # TODO get vid_info
    #vid_info = common.parse_load_page_and_get_vid(var)
    
    pvinfo = _get_video_info(vid_info)
    # NOTE count and select
    pvinfo = _count_and_select(pvinfo)
    out = _get_file_urls(pvinfo)
    # NOTE add headers
    out = _add_headers(out)
    # TODO support enable_more
    return out

def _get_video_info(vid_info):
    # TODO support fast_parse here
    pass

def _count_and_select(pvinfo):
    pass

def _get_file_urls(pvinfo):
    pass

def _add_headers(pvinfo):
    # TODO support gen_header method arg here
    pass

# TODO
# end method_pc_flash_gate.py


