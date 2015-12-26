# _conf.py, parse_video/lib/b :: config file support
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509232304

import json
import xml.etree.ElementTree as ET

from .. import err
from ._path import *

# global data
etc = {}
etc['to_etc_path'] = './etc'	# from parse_video's root_path
etc['etc_path'] = ''

def get_etc_path(flag_no_cache=False):
    if (not etc['etc_path']) or flag_no_cache:
        etc['etc_path'] = pn(pjoin(get_root_path(), etc['to_etc_path']))
    return etc['etc_path']

def load_conf_file(file_path, parse='json', flag_ignore_encoding_error=False):
    '''
    load a config file, and return result
        file_path	the config file path from etc_path
        		config file should be a text file with utf-8 encoding
        parse		the method used to parse the config file
    support these formats to parse the file
        raw		not parse it, just return the raw text
        json		return the result of json.loads(raw_text)
        xml		return the result of ET.fromstring(raw_text)
    '''
    try:
        conf_file = pn(pjoin(get_etc_path(), file_path))
        with open(conf_file, 'rb') as f:
            blob = f.read()
        if flag_ignore_encoding_error:
            raw_text = blob.decode('utf-8', 'ignore')
        else:
            raw_text = blob.decode('utf-8')
        if parse == 'json':
            return json.loads(raw_text)
        elif parse == 'xml':
            return ET.fromstring(raw_text)
        return raw_text
    except Exception as e:
        raise err.LoadConfigError('can not load config file', conf_file) from e

# end _conf.py



def number(i):
    '''
    convert i to number, prefer int than float
    '''
    f = float(i)
    if f == int(f):
        return int(f)
    return f


import uuid

def gen_uuid():
    return uuid.uuid4().hex

# _parse.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509261456

'''
base and common parse function support, based on standard parse_video video_info format
'''

from .. import var

def select_hd(video_info):
    '''
    auto-select videos and mark the file, with var._ hd_min and hd_max data
    before remove files' info, will auto count items, such as size_byte
    will mark no-need video's file to [] (no items)
    '''
    # NOTE auto-count video files info
    video_info = auto_count(video_info)
    # select and ignore videos
    hd_min = var._['hd_min']
    hd_max = var._['hd_max']
    for v in video_info:
        hd = v['hd']
        flag_ignore = False
        if (hd_min != None) and (hd < hd_min):
            flag_ignore = True
        if (hd_max != None) and (hd > hd_max):
            flag_ignore = True
        if flag_ignore:
            v['file'] = []
    return video_info

def select_file_index(video_info):
    '''
    auto-select file with index for --min-i and --max-i
    will mark no-need file's url to '' (null string)
    '''
    i_min = var._['i_min']
    i_max = var._['i_max']
    for v in video_info:
        for i in range(len(v['file'])):
            f = v['file'][i]
            flag_ignore = False
            if (i_min != None) and (i < i_min):
                flag_ignore = True
            if (i_max != None) and (i > i_max):
                flag_ignore = True
            if flag_ignore:
                f['url'] = ''
    return video_info

def auto_count(video_info):
    '''
    auto-count info of video items
    will auto-ignore count-ed items
    '''
    for v in video_info:
        # set count
        count = len(v['file'])
        if not 'count' in v:
            v['count'] = count
        # count items
        size_byte = 0
        time_s = 0
        for f in v['file']:
            if f['size'] < 0:
                size_byte = -1
            elif size_byte >= 0:
                size_byte += f['size']
            if f['time_s'] < 0:
                time_s = -1
            elif time_s >= 0:
                time_s += f['time_s']
        # set size_byte and time_s
        if not 'size_byte' in v:
            v['size_byte'] = size_byte
        if not 'time_s' in v:
            v['time_s'] = time_s
    return video_info

# end _parse.py

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


