# method.py, parse_video/lib/e/hunantv/

import functools

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import mango_tv3

# support --more
def get_raw_more(method_arg_text):
    data_list = [	# NOTE --more mode to direct get vid_info
        'vid_info', 
    ]
    raw_more = common.method_simple_check_use_more(var, method_arg_text, data_list)
    return raw_more

def get_vid_info():
    # get vid_info from more if possible
    default_get_vid_info = functools.partial(common.parse_load_page_and_get_vid, var)
    vid_info = common.method_more_simple_get_vid_info(var, default_get_vid_info)
    return vid_info

def check_enable_more(out):
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = var._['_vid_info']
    return out

def dl_first_json(vid_info):
    # make first url
    first_url = mango_tv3.gen_first_url(vid_info['vid'])
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['status'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['status'], var))
    return first

def get_video_info(vid_info, parse_raw_first):
    first = dl_first_json(vid_info)
    return common.parse_raw_first(first, parse_raw_first)

def raw_first_get_base_info(first):
    data = first['data']
    out = {}
    # get base video info
    info = data['info']
    out['info'] = {}
    out['info']['title'] = info['title']
    out['info']['title_short'] = info['collection_name']
    out['info']['title_sub'] = info['sub_title']
    out['info']['title_no'] = b.simple_get_number_from_text(info['series'])
    return out, data, info

# end method.py


