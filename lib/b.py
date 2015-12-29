# b.py, parse_video/lib/

import os
import json
import hashlib
import threading
import multiprocessing.dummy as multiprocessing

from . import err
from ._b import log, flash

from ._b.network import (
    dl_blob, 
    dl_html, 
    dl_json, 
    dl_xml, 
    post, 
    post_form, 
)
from ._b.text import (
    str_or_str, 
    split_raw_extractor, 
    split_raw_method, 
    simple_get_number_from_text, 
    simple_m3u8_parse, 
)

# global data
etc = {}
etc['to_root_path'] = '../'	# from now dir
etc['to_etc_path'] = './etc/'		# from root_path

# md5_hash
def md5_hash(raw):
    return hashlib.md5(bytes(raw, 'utf-8')).hexdigest()

# use many threads to do many tasks at the same time
def map_do(task_list, worker=lambda x:x, pool_size=1):
    pool = multiprocessing.Pool(processes=pool_size)
    result = pool.map(worker, task_list)
    pool.close()
    pool.join()
    return result

# root path : parse_video/
def get_root_path():
    now_dir = os.path.dirname(__file__)
    raw = os.path.join(now_dir, etc['to_root_path'])
    out = os.path.normpath(raw)
    return out

# etc path : parse_video/etc/
def get_etc_path():
    root_path = get_root_path()
    raw = os.path.join(root_path, etc['to_etc_path'])
    out = os.path.normpath(raw)
    return out

# load config file in etc/ dir
def load_config_file(fpath):
    conf_file_path = os.path.normpath(os.path.join(get_etc_path(), fpath))
    try:
        with open(conf_file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        er = err.ConfigError('can not load config file', conf_file_path)
        raise er from e

# load config file and parse as json
def load_config_json(fpath):
    raw_blob = load_config_file(fpath)
    try:
        text = raw_blob.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('can not decode blob to text, json config file', fpath)
        er.blob = raw_blob
        raise er from e
    try:
        out = json.loads(text)
        return out
    except Exception as e:
        er = err.ParseJSONError('can not parse json text, config file', fpath)
        er.text = text
        raise er from e

# end b.py


