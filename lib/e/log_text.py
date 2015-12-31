# log_text.py, parse_video/lib/e/
# TODO support other languages

from ..b import str_or_str

# extractor common log text

def entry_log_use_method(method, method_arg_text):
    return ('use method \"' + method + '\" and method_args ' + str_or_str(method_arg_text) + ' ')

def method_enable_more():
    return ('--more mode enabled ')

def method_loading_page(raw_url):
    return ('loading page \"' + raw_url + '\" ')

def method_got_vid_info(vid_info):
    return ('got vid_info ' + str(vid_info))

def method_got_first_url(first_url, prefix=''):
    return (prefix + 'got first URL \"' + first_url + '\" ')

# extractor common err text

def entry_err_no_method(method):
    return ('no method \"' + method + '\" ')

def method_err_first_code(code, var):
    return ('first info code ' + str_or_str(code) + ' is not ' + str(var.FIRST_OK_CODE) + ' ')

def method_err_parse_raw_first():
    return ('parse raw first info failed')

# end log_text.py


