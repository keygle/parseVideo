# -*- coding: utf-8 -*-
# __init__.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.4.0 test201509262019

'''
entry of parse_video/lib's base part, the utils
'''

_flag_not_imported = True
if _flag_not_imported:
    _flag_not_imported = False
    from ._conf import *
    from ._key import *
    from ._net import *
    from ._parse import *
    from ._path import *
    from ._re import *
    from ._thread import *

def number(i):
    '''
    convert i to number, prefer int than float
    '''
    f = float(i)
    if f == int(f):
        return int(f)
    return f

# end __init__.py


