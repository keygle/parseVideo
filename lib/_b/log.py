# log.py, parse_video/lib/_b/

# TODO output color support

import sys

from .. import conf, err

# log output filter
log_filter = {
    'DEBUG:' : False, 
    'ERROR:' : True, 
    'WARNING:' : True, 
    'INFO:' : True, 
    '[ OK ]' : True, 
    None : True, 	# default value
    '__show_log_pos' : False, 	# show log package and function name
}

# set log level function
def set_log_level(level=None):
    if level == 'debug':
        log_filter['DEBUG:'] = True
        log_filter['__show_log_pos'] = True	# only show log pos under debug
    elif level == 'quiet':
        log_filter['INFO:'] = False
        log_filter['[ OK ]'] = False
        log_filter[None] = False
    else:	# set log level to default
        log_filter['DEBUG:'] = False
        log_filter['ERROR:'] = True
        log_filter['WARNING:'] = True
        log_filter['INFO:'] = True
        log_filter['[ OK ]'] = True
        log_filter[None] = True
        log_filter['__show_log_pos'] = False

# get caller's info for log and DEBUG
def get_caller_info(depth=2):
    f = sys._getframe(depth)
    module_name = f.f_globals['__name__']
    function_name = f.f_code.co_name
    return module_name, function_name

# base print function
def _p(text, file=sys.stderr, flush=True):
    print(text, file=file, flush=flush)

# base debug print function
def _pd(raw_text, depth=3, prefix=conf.PV_LOG_PREFIX, debug_type=''):
    caller_module, caller_function = get_caller_info(depth=depth)
    debug_prefix = caller_module + ':' + caller_function + ': '
    debug_text = debug_type + ' ' + raw_text
    if log_filter['__show_log_pos']:
        debug_text = debug_prefix + debug_text
    # add log prefix
    debug_text = prefix + debug_text
    # check log output filter
    if log_filter.get(debug_type, log_filter[None]):
        _p(debug_text)

# exports functions

def p(raw_text, file=sys.stdout):
    '''
    the replace of print() in parse_video's code
    '''
    # just print it
    _p(raw_text, file=file)

def raw(raw_text, debug_type=''):
    '''
    output with no type
    '''
    _pd(raw_text, debug_type=debug_type)

# NOTE r() is the same as raw()
r = raw

def d(raw_text):
    '''
    DEBUG: 
    '''
    _pd(raw_text, debug_type='DEBUG:')

def i(raw_text):
    '''
    INFO: 
    '''
    _pd(raw_text, debug_type='INFO:')

def w(raw_text):
    '''
    WARNING: 
    '''
    _pd(raw_text, debug_type='WARNING:')

def e(raw_text):
    '''
    ERROR: 
    '''
    _pd(raw_text, debug_type='ERROR:')

def o(raw_text):
    '''
    [ OK ] 
    '''
    _pd(raw_text, debug_type='[ OK ]')

# end log.py


