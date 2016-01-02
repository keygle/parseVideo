#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# run.py, parse_video/, support lieying python3 parse plugin port_version 0.3.0, based on lyyc_plugin port_version 0.1.0 
# author sceext <sceext@foxmail.com>
# version 0.1.10.0 test201601022233

import math
import os, sys, io, json
import functools, traceback, tempfile

try:
    from . import lyyc_plugin
except Exception as e:
    import lyyc_plugin

# global data
PACK_VERSION = 9

FLAG_DEBUG = False
ERR_PREFIX = 'yy-6.1::'

RAW_VERSION_INFO = {	# raw output info obj
    'port_version' : '0.3.0', 
    'type' : 'parse', 
    'version' : '1.5.0', 
    'name' : '上古有颜6.1代', 
    
    'note' : 'parse_video for lieying_plugin. ', 
}

FILENAME_BAD_CHAR = ' \\:"/|?*<>'
FILENAME_REPLACE = '-'

# base functions

def _number(raw):
    f = float(raw)
    if int(f) == f:
        return int(f)
    return f

def _num_len(n, l=2):
    if (n < 1):
        return '-1'
    return str(n).zfill(l)

def _gen_bitrate(size_byte, time_s, unit_k=1024):
    if (size_byte <= 0) or (time_s <= 0):
        return '-1'	# can not gen bitrate
    raw_rate = size_byte * 8 / time_s	# bps
    kbps = raw_rate / unit_k
    bitrate = str(round(kbps, 1)) + 'kbps'
    return bitrate

def _byte_to_size(size_byte, flag_add_byte=True):
    unit_list = [
        ' Byte', 
        'KB', 
        'MB', 
        'GB', 
        'TB', 
        'PB', 
        'EB', 
    ]
    size_byte = int(size_byte)
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
    
    size_str = size_t + ' ' + unit
    if flag_add_byte:
        size_str += ' (' + str(size_byte) + ' Byte)'
    return size_str

def _second_to_time(time_s):
    raw = _number(time_s)
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
    return t

def _p_json(raw):
    if FLAG_DEBUG:
        text = json.dumps(raw, indent=4, sort_keys=True, ensure_ascii=False)
    else:
        text = json.dumps(raw)
    return text

def _print_err(e):
    line = traceback.format_exception(Exception, e, e.__traceback__)
    text = ERR_PREFIX + ('').join(line) + '\n'
    return text

def _gen_tmp_buffer():
    f = tempfile.TemporaryFile()
    w = io.TextIOWrapper(f)
    return w

# set sys.stdout and sys.stderr for lyyc_plugin
def _init_stdout_stderr():
    # check to set
    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = _gen_tmp_buffer()
    if not isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr = _gen_tmp_buffer()

# compatible functions
def _call_wrapper(f):
    try:	# NOTE common Error process here
        out = f()
    except Exception as e:
        if FLAG_DEBUG:
            raise
        out = {
            'error' : _print_err(e), 
        }
    text = _p_json(out)
    return text

def _do_parse(url, hd_min=None, hd_max=None):
    # init for parse_video core
    _init_stdout_stderr()
    # use lyyc_plugin to do parse
    pvinfo = lyyc_plugin.lyyc_parse(url, hd_min=hd_min, hd_max=hd_max)
    return pvinfo

def _t_parse_url(pvinfo, hd):
    # select video by hd
    video = None
    for v in pvinfo['video']:
        if v['hd'] == hd:
            video = v
            break
    if video == None:
        raise Exception('ERROR: can not select hd = ' + str(hd) + ' video info from raw pvinfo ')
    # gen url lists
    out = []
    for f in video['file']:
        one = {}
        one['protocol'] = 'http'
        one['value'] = f['url']
        if 'header' in f:
            one['args'] = f['header']
        out.append(one)
    # fix protocol for m3u8
    if video['format'] == 'm3u8':
        for f in out:
            f['protocol'] = 'm3u8'
    return out

def _t_parse(pvinfo):
    out = {
        'type' : 'formats', 
        'data' : [], 
    }
    out['name'] = _make_title(pvinfo['info'])
    out['data'] = _make_label_data(pvinfo['video'])
    return out

def _make_title(info):
    title = info['title']
    # NOTE process title_sub, ... not exist
    title_sub = ''
    title_no = -1
    if 'title_sub' in info:
        title_sub = info['title_sub']
    if 'title_no' in info:
        title_no = info['title_no']
    site = info['site_name']
    
    no = _num_len(title_no, 4)
    out = ('_').join([no, title, title_sub, site])
    # replace bad chars in filename
    out = ('').join([i if not i in FILENAME_BAD_CHAR else FILENAME_REPLACE for i in out])
    return out

# make output data info, include label text
def _make_label_data(video):
    out = []
    # make base output info
    for v in video:
        one = {}
        one['ext'] = v['format']
        one['size'] = _byte_to_size(v['size_byte'])
        one['label'] = ''
        out.append(one)
    # gen base label info
    label_info = []
    for v in video:
        label_info.append(_gen_label_info(v))
    
    # add label index
    video_len = len(video)
    n_len = math.floor(math.log(video_len, 10)) + 1
    for i in range(video_len):
        index = '(' + _num_len(i + 1, n_len) + ') '
        out[i]['label'] += index
    # add hd
    for i in range(video_len):	# process hd text like -1
        if not label_info[i][0].startswith('-'):
            label_info[i][0] = ' ' + label_info[i][0]
    out = _label_just_str(0, out, label_info)
    # add quality
    quality_max_len = 0
    for i in range(video_len):
        l = _quality_str_len(label_info[i][1])
        if l > quality_max_len:
            quality_max_len = l
    quality_max_len += 1
    for i in range(video_len):
        out[i]['label'] += _quality_ljust(label_info[i][1], quality_max_len)
    # add px and bitrate
    for i in [2, 3]:
        out = _label_just_str(i, out, label_info, rjust=True)
    # add time
    out = _label_just_str(4, out, label_info)
    # add count and format
    for i in [5, 6]:
        out = _label_just_str(i, out, label_info, rjust=True)
    # gen label text done
    return out

def _label_just_str(i, out, info, rjust=False, fill='_'):
    max_len = 0
    for j in range(len(info)):
        l = len(info[j][i])
        if l > max_len:
            max_len = l
    for j in range(len(out)):
        raw = info[j][i]
        if rjust:
            t = raw.rjust(max_len, fill) + fill
        else:
            t = raw.ljust(max_len + 1, fill)
        out[j]['label'] += t
    return out

# process no-ascii chars
def _quality_str_len(raw, max_ascii=128):
    i = 0
    for c in raw:
        if ord(c) > max_ascii:
            i += 2
        else:
            i += 1
    return i

def _quality_ljust(raw, l=0, fill='_'):
    while _quality_str_len(raw) < l:
        raw += fill
    return raw

def _gen_label_info(v):
    p = v['size_px']
    px = str(p[0]) + 'x' + str(p[1])
    bitrate = _gen_bitrate(v['size_byte'], v['time_s'])
    time = _second_to_time(v['time_s'])
    out = [str(v['hd']), v['quality'], px, bitrate, time, str(v['count']), v['format']]
    return out

def _parse_label(label):
    hd = label.split(' ', 1)[1].split('_', 1)[0]
    out = float(hd)
    return out

# before exports
def _get_version():
    raw = RAW_VERSION_INFO
    # get version info from lyyc_plugin
    out = lyyc_plugin.lyyc_about()
    old = out.copy()	# save raw lyyc_plugin info
    # add and overwrite some values
    for key, value in raw.items():
        out[key] = value
    # remove some values
    remove_list = [
        'mark_uuid', 
        'parse', 
    ]
    for r in remove_list:
        if r in out:
            out.pop(r)
    # set filter, pack_version
    out['filter'] = old['parse']
    out['pack_version'] = PACK_VERSION
    # update plugin name
    name = out['name']
    name += ' [' + str(out['pack_version']) + '] ' + old['name'] + ' version ' + old['version'] + ' '
    out['name'] = name
    # make version info done
    return out

def _parse(url):
    pvinfo = _do_parse(url, hd_min=1, hd_max=0)
    out = _t_parse(pvinfo)
    return out

def _parse_url(url, label, i_min=None, i_max=None):
    # TODO NOTE not support i_min and i_max now
    hd = _parse_label(label)
    pvinfo = _do_parse(url, hd_min=hd, hd_max=hd)
    out = _t_parse_url(pvinfo, hd)
    return out

# exports functions
def GetVersion():
    f = functools.partial(_get_version)
    return _call_wrapper(f)

def Parse(url):
    f = functools.partial(_parse, url)
    return _call_wrapper(f)

def ParseURL(url, label, i_min=None, i_max=None):
    f = functools.partial(_parse_url, url, label, i_min=i_min, i_max=i_max)
    return _call_wrapper(f)

# DEBUG functions
def p(o):
    print(json.dumps(json.loads(o), indent=4, sort_keys=True, ensure_ascii=False))

# end run.py


