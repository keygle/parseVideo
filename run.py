#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# run.py, parse_video/, support lieying python3 parse plugin port_version 0.3.0, based on lyyc_plugin port_version 0.1.0 
# author sceext <sceext@foxmail.com>
# version 0.1.4.0 test201512310013

import math
import os, sys, io, json
import functools, traceback, tempfile

try:
    from . import lyyc_plugin
except Exception as e:
    import lyyc_plugin

# global data
PACK_VERSION = 4

FLAG_DEBUG = False
ERR_PREFIX = 'yy-6.1::'

RAW_VERSION_INFO = {	# raw output info obj
    'port_version' : '0.3.0', 
    'type' : 'parse', 
    'version' : '1.2.0', 
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
    t = _num_len(minute, 2) + ':' + _num_len(sec, 2) + '.' + str(round(ms * 1e3))
    if hour > 0:	# check add hour
        t = _num_len(hour, 2) + t
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

def _t_parse(pvinfo):
    out = {
        'type' : 'formats', 
        'data' : [], 
    }
    out['name'] = _make_title(pvinfo['info'])
    for v in pvinfo['video']:
        one = {}
        one['label'], one['size'] = _make_label(v)
        one['ext'] = v['format']
        out['data'].append(one)
    return out

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

def _make_label(video):
    hd = video['hd']
    quality = video['quality']
    size_px = video['size_px']
    size_byte = video['size_byte']
    time_s = video['time_s']
    format_ = video['format']
    count = video['count']
    # make label part str
    px = str(size_px[0]) + 'x' + str(size_px[1])
    size = _byte_to_size(size_byte)
    time = _second_to_time(time_s)
    bitrate = _gen_bitrate(size_byte, time_s)
    # gen label str
    label = ('_').join([str(hd), quality, px, bitrate, time, str(count), format_])
    return label, size

def _parse_label(label):
    hd = label.split('_', 1)[0]
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


