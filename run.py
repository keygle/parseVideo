#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# run.py, parse_video/, support lieying python3 parse plugin port_version 0.4.0, based on pv command line
# author sceext <sceext@foxmail.com>
# [BUG fix only] version 0.3.0.0 test201603261452

import os, sys
import math
import json
import functools
import subprocess

# global data
FLAG_DEBUG = True
ERR_PREFIX = 'pv6.lyp4::'

RAW_VERSION_INFO = {
    'port_version' : '0.4.0', 
    'type' : 'parse', 
    'version' : '3.0.0', 
    'name' : '负锐解析猎影插件', 
    
    'note' : '[BUG fix only] 负锐视频解析 猎影插件 \n parse_video for lieying_plugin. ', 
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

def _print_err(raw):
    line = raw.splitlines()
    out = ERR_PREFIX + ('\n').join(line) + '\n'
    return out

# call pv from command line
def _call_pv(args):
    # TODO support parse timeout
    py_bin = sys.executable
    now_dir = os.path.dirname(__file__)
    pv_bin = os.path.normpath(os.path.join(now_dir, './pv'))
    # run it
    argv = [py_bin, pv_bin] + args
    # TODO DEBUG log
    PIPE = subprocess.PIPE
    p = subprocess.run(argv, stdout=PIPE, stderr=PIPE)
    flag_err = False
    if p.returncode != 0:
        flag_err = True
    try:
        text = p.stdout.decode('utf-8')
        out = json.loads(text)
    except Exception as e:
        flag_err = True
    # process error
    if flag_err:
        stderr = p.stderr.decode('utf-8', 'ignore')
        stdout = p.stdout.decode('utf-8', 'ignore')
        err_text = 'pv Error, stderr \n' + stderr + '--> stdout \n' + stdout
        out = {
        	'type' : 'error', 
        	'error' : _print_err(err_text), 
        }
    return out	# done

# compatible functions
def _call_wrapper(f):
    # NOTE nothing to do now
    return f()

def _do_parse(url, hd_min=None, hd_max=None):
    # make pv command line arguments
    args = ['--fix-unicode']
    if hd_min != None:
        args += ['--min', str(hd_min)]
    if hd_max != None:
        args += ['--max', str(hd_max)]
    args += [url]
    # do call pv, NOTE just return json info
    return _call_pv(args)

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
        one['urls'] = [f['url']]
        if 'header' in f:
            one['args'] = f['header']
        # add more info for this file
        one['duration'] = f['time_s'] * 1e3
        one['length'] = f['size']
        
        one['maxDown'] = 1	# he he he he
        out.append(one)
    # fix protocol for m3u8
    if video['format'] == 'm3u8':
        for f in out:
            f['protocol'] = 'm3u8'
    return out

def _t_parse(pvinfo):
    out = {
        'type' : 'formats', 
        'icon' : 'http://www.ilewo.cn/images/qrcode.png', 
        'caption' : 'pv6.lyp4-result', 
        'warning' : 'N/A', 
        'sorted' : True, 
        'data' : [], 
    }
    out['name'] = _make_title(pvinfo['info'])
    out['provider'] = pvinfo['info']['site_name']
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

# call lyyc_plugin
def _lyyc_about():
    try:
        from . import lyyc_plugin
    except Exception as e:
        import lyyc_plugin
    return lyyc_plugin.lyyc_about()

# before exports
def _get_version():
    out = RAW_VERSION_INFO
    # get about info from lyyc_plugin
    raw = _lyyc_about()
    # add more info
    add_list = [
        'author', 
        'copyright', 
        'license', 
        'home', 
    ]
    for i in add_list:
        out[i] = raw['info'][i]
    # add uuid, NOTE not overwrite
    if not 'uuid' in out:
        out['uuid'] = raw['uuid']
    # set filter, pack_version
    out['filter'] = raw['parse']
    out['pack_version'] = str(raw['pack_version'])
    # update plugin name
    name = out['name']
    name += ' [' + str(out['pack_version']) + '] ' + raw['info']['name'] + ' version ' + raw['version'] + ' '
    out['name'] = name
    # make version info done
    return out

def _parse(url):
    pvinfo = _do_parse(url, hd_min=1, hd_max=0)
    # NOTE check error
    if 'error' in pvinfo:
        return pvinfo
    out = _t_parse(pvinfo)
    return out

def _parse_url(url, label, *k, **kk):
    # NOTE not support more features for lieying plugin ParseURL()
    hd = _parse_label(label)
    pvinfo = _do_parse(url, hd_min=hd, hd_max=hd)
    if 'error' in pvinfo:
        return pvinfo
    out = _t_parse_url(pvinfo, hd)
    return out

# exports functions
def GetVersion():
    f = functools.partial(_get_version)
    return _call_wrapper(f)

def Parse(url, *k, **kk):
    f = functools.partial(_parse, url)
    return _call_wrapper(f)

def ParseURL(url, label, *k, **kk):
    f = functools.partial(_parse_url, url, label, *k, **kk)
    return _call_wrapper(f)

# DEBUG functions
def p(o):
    print(json.dumps(o, indent=4, sort_keys=True, ensure_ascii=False))

# end run.py


