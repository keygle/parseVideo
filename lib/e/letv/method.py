# method.py, parse_video/lib/e/letv/, method common code

import functools

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var

# NOTE support --more, try to enable more mode
def get_raw_more(method_arg_text):
    data_list = [	# NOTE --more mode to just get vid_info
        'vid_info', 
    ]
    raw_more = common.method_simple_check_use_more(var, method_arg_text, data_list)
    return raw_more

# try to get vid_info from more
def get_vid_info():
    # get vid_info from more if possible
    default_get_vid_info = functools.partial(common.parse_load_page_and_get_vid, var)
    vid_info = common.method_more_simple_get_vid_info(var, default_get_vid_info)
    return vid_info

# add --more data to out
def check_enable_more(out):
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = var._['_vid_info']
    return out

def dl_first_json(first_url):
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['statuscode'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['statuscode'], var))
    return first

def raw_first_get_base_info(first):
    playurl = first['playurl']
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = playurl['title']
    return out, playurl

# end method.py


