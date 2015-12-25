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


