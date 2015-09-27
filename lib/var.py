# var.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.8.0 test201509271702

'''
parse_video/lib/var.py
    global common data for parse_video
'''

# static data

CONF_FILE = 'pv_main.conf.json'

# NOTE user_agent update at 2015-09-24 11:43 GMT+0800 CST from firefox on windows 10
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'

PV_DEBUG_PREFIX = 'pv ::'

# only for b.log output filter, used to set log level
log_filter = {	# default values are for default without --debug for --quiet
    '' : True, 	# default type, allow print, with --quiet will not show this
    'DEBUG:' : False, 	# with --debug will show this
    'INFO:' : True, 	# with --quiet will not show this
    '[ OK ]' : True, 	# with --quiet will not show this
    'WARNING:' : True, 	# will --quiet will not show this
    'ERROR:' : True, 	# will always show this
}

# var data
_ = {}

# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    # set default values
    out['flag_output_no_restruct'] = False	# for --output-no-restruct
    
    # for --min --max --min-i --max-i
    out['hd_min'] = None
    out['hd_max'] = None
    out['i_min'] = None
    out['i_max'] = None
    
    # config items
    out['user_agent'] = DEFAULT_USER_AGENT
    out['url_to_e_filter'] = None	# url to extractor re filter, used by lib.e.url_to_e
    out['default_method'] = None	# default method list for extractors
    
    return out

def push():
    __old.append(_)

def pop():
    return __old.pop()

# end var.py


