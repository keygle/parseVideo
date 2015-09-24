# log.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.3.0 test201509241447

# TODO support set log level

'''
log functions for parse_video, and support DEBUG log file (such as vms.json file)
'''

import sys
import logging

from .. import var

# get caller's info for log and DEBUG
def get_caller_info(depth=2):
    # NOTE may be not stable
    f = sys._getframe(depth)
    module_name = f.f_globals['__name__']
    function_name = f.f_code.co_name
    return module_name, function_name

# base print function
def _p(text, file=sys.stderr, flush=True):
    print(text, file=file, flush=flush)

# debug print function
def _pd(raw_text, depth=3, prefix=var.PV_DEBUG_PREFIX, debug_type=''):
    # get caller's info
    mn, fn = get_caller_info(depth=depth)
    # TODO may add time info
    debug_prefix = prefix + ' ' + mn + ':' + fn + ': ' + debug_type + ' '
    debug_text = debug_prefix + raw_text
    # just print it
    _p(debug_text)

# export functions

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


