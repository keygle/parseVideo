# _path.py, parse_video/lib/b :: path operations
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509232101

import os.path

# global data
etc = {}
etc['to_root_path'] = '../../'	# from now_dir to parse_video root_path
etc['root_path'] = ''	# used to cache get_root_path() result


def get_root_path(flag_no_cache=False):
    '''
    return parse_video's root_path
    '''
    if (not etc['root_path']) or flag_no_cache:
        now_dir = pdir(__file__)
        root_path = pn(pjoin(now_dir, etc['to_root_path']))
        etc['root_path'] = root_path
    return etc['root_path']

# shortcuts for os.path

def pdir(raw):
    return os.path.dirname(raw)

def pn(raw):
    return os.path.normpath(raw)

def pjoin(*k, **kk):
    return os.path.join(*k, **kk)

def pisfile(raw):
    return os.path.isfile(raw)

# end _path.py


