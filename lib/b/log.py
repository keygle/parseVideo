# log.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509232135

'''
log functions for parse_video, and support DEBUG log file (such as vms.json file)
'''

import logging

# TODO support set log level

# export functions

def p(raw_text):
    '''
    the replace of print() in parse_video's code
    '''
    # TODO do more works here
    print(raw_text)

def raw():
    '''
    output with no type
    '''
    pass

def r():
    '''
    same as raw()
    '''
    pass

def d():
    '''
    DEBUG: 
    '''
    pass

def i():
    '''
    INFO: 
    '''
    pass

def w():
    '''
    WARNING: 
    '''
    pass

def e():
    '''
    ERROR: 
    '''
    pass

def o():
    '''
    [ OK ] 
    '''
    pass

# end log.py


