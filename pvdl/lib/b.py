# b.py, parse_video/pvdl/lib/

import os, sys
import math, json
import hashlib
import multiprocessing.dummy as multiprocessing

import colored

from . import err, conf

## text functions

def replace_filename_bad_char(raw, replace=conf.FILENAME_REPLACE):
    bad_chars = conf.FILENAME_BAD_CHAR
    out = ('').join([i if not i in bad_chars else replace for i in raw])
    return out

def num_len(n, l=2):
    out = (str(n)).zfill(l)
    return out

def number(raw):
    f = float(raw)
    if int(f) == f:
        return int(f)
    return f


## make label (title) base functions

def gen_bitrate(size_byte, time_s, unit_k=1024):
    if (size_byte <= 0) or (time_s <= 0):
        return '-1'	# can not gen bitrate
    raw_rate = size_byte * 8 / time_s	# bps
    kbps = raw_rate / unit_k
    bitrate = str(round(kbps, 1)) + 'kbps'
    return bitrate

def byte_to_size(size_byte, flag_add_byte=True, flag_add_grey=False):
    unit_list = [
        ' Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
    ]
    size_byte = int(size_byte)
    # NOTE process size_byte < 0
    less_than_0 = ''
    if size_byte < 0:
        size_byte = math.abs(size_byte)
        less_than_0 = '-'
    # check < 1 Byte
    if size_byte < 1:
        return '-1'
    if size_byte < 1024:	    # check < 1 KB
        return str(size_byte) + unit_list[0]
    # get unit
    unit_i = math.floor(math.log(size_byte, 1024))
    if unit_i > (len(unit_list) -1):
        unit = unit_list[-1]
    else:
        unit = unit_list[unit_i]
    size_n = size_byte / pow(1024, unit_i)
    size_t = str(round(size_n, 2))
    
    size_str = less_than_0 + size_t + ' ' + unit
    if flag_add_byte:
        if flag_add_grey:
            size_str += colored.fg('grey_50')
        size_str += ' (' + less_than_0 + str(size_byte) + ' Byte)'
    return size_str

def second_to_time(time_s):
    raw = number(time_s)
    # NOTE process time_s < 0
    less_than_0 = ''
    if raw < 0:
        raw = math.abs(raw)
        less_than_0 = '-'
    # get time info
    sec = math.floor(raw)
    ms = raw - sec
    minute = math.floor(sec / 60)
    sec -= minute * 60
    hour = math.floor(minute / 60)
    minute -= hour * 60
    # make text, and add ms
    t = str(minute).zfill(2) + ':' + str(sec).zfill(2) + '.' + str(round(ms * 1e3))
    if hour > 0:	# check add hour
        t = str(hour).zfill(2) + ':' + t
    t = less_than_0 + t
    return t


## path functions

# join paths
def pjoin(*k, **kk):
    raw = os.path.join(*k, **kk)
    out = os.path.normpath(raw)
    return out

# to pvdl root path (parse_video/pvdl/)
def get_root_path(to_root='../'):
    now_dir = os.path.dirname(__file__)
    out = pjoin(now_dir, to_root)
    return out


## other functions

# deep clone a object with json
def json_clone(raw):
    out = json.loads(json.dumps(raw))
    return out

# common check size function
def check_size(real_size, ok_size, check_unit=1, keep=1e2):
    err_s = real_size - ok_size
    err_k = (err_s / ok_size) * 1e2	# %
    # NOTE err_k looks like 12.23 %
    err_k = (math.floor(err_k * keep) + 1) / keep
    if real_size != ok_size:
        er = True
    err_u = err_s / check_unit
    return err_s, err_k, er, err_u

CHECK_SIZE_MB = pow(1024, 2)	# for check size MB


# use many threads to do many tasks at the same time
def map_do(task_list, worker=lambda x:x, pool_size=1):
    pool = multiprocessing.Pool(processes=pool_size)
    result = pool.map(worker, task_list)
    pool.close()
    pool.join()
    return result

def md5sum(fpath, chunk_size=pow(1024, 2) * 16):	# NOTE default chunk size to road file bytes is 16 MB
    md5 = hashlib.md5()
    with open(fpath, 'rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            md5.update(data)
    out = md5.hexdigest()
    return out


# end b.py


