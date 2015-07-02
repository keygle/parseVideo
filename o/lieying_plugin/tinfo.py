# -*- coding: utf-8 -*-
# tinfo.py, part for parse_video : a fork from parseVideo. 
# tinfo: o/lieying_plugin/tinfo: translate info from parse_video to lieying_plugin. 
# version 0.1.3.0 test201507021305
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.07. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# import

import math

from . import error
from ..output import easy_text
from ..easy import make_name

# global vars
LIEYING_PLUGIN_PROTOCOL = 'http'
LIEYING_PLUGIN_ARGS = {}

# base function
# make number length
def make_num_len(n, l=4):
    t = str(n)
    while len(t) < l:
        t = '0' + t
    return t

def byte2unit(byte_n, unit0=['Byte', 'B']):
    units = 'KMGTPE'
    # check byte_n
    if byte_n < 1024:
        return str(byte_n) + ' ' + unit0[0]
    # whitch unit
    i = math.floor(math.log(byte_n, 1024))
    if i > len(units):
        i = len(units)
    byte_n /= math.pow(1024, i)
    # make byte_n to text
    t = str(byte_n)
    if t.find('.') != -1:
        ts = t.split('.')
    else:
        ts = [t, '']
    if len(ts[1]) > 2:
        ts[1] = ts[1][:2]
    while len(ts[1]) < 2:
        ts[1] += '0'
    t = ts[0] + '.' + ts[1]
    # done
    return t + ' ' + units[i - 1] + unit0[1]

def second2time(sec=0):
    # make minute and hour
    minute = math.floor(sec / 60)
    sec -= minute * 60
    hour = math.floor(minute / 60)
    minute -= hour * 60
    # make text
    t = str(sec)	# second
    # check .
    if t.find('.') != -1:
        ts = t.split('.')
        if len(ts[0]) < 2:
            ts[0] = '0' + ts[0]
        if len(ts[1]) > 3:
            ts[1] = ts[1][:3]
        if int(ts[1]) == 0:
            t = ts[0]
        else:
            t = ts[0] + '.' + ts[1]
    else:
        if len(t) < 2:
            t = '0' + t
    # minute
    m = str(minute)
    if len(m) < 2:
        m = '0' + m
    t = m + ':' + t
    # add hour
    if hour > 0:
        h = str(hour)
        if len(h) < 2:
            h = '0' + h
        t = h + ':' + t
    # done
    return t

# function

def make_format_text(vinfo):
    t = ''
    t += str(vinfo['hd']) + '_'
    t += vinfo['quality'] + '_'
    t += str(vinfo['size_px'][0]) + 'x' + str(vinfo['size_px'][1]) + '_'
    t += vinfo['format'] + '_'
    t += second2time(vinfo['time_s']) + '_'
    t += str(vinfo['count'])
    # done
    return t

def get_hd_from_format_text(format_text):
    hd = format_text.split('_', 1)[0]
    return int(hd)

def make_title(tinfo):
    # just use make_name host to generate name
    t = make_name_host(
    		title=tinfo['title'], 
    		title_sub=tinfo['title_sub'], 
    		title_no=tinfo['title_no'], 
    		title_short=tinfo['title_short'], 
    		site=tinfo['site_name'], 
    		quality=tinfo['quality'])
    return t

# just output video list, return as json obj
def t2list(evinfo):
    video_name = make_title(evinfo['info'])
    out = {}
    out['Name'] = video_name
    vlist = []
    out['Formats'] = vlist
    # add each video item
    for v in evinfo['video']:
        one = {}
        video_format = make_format_text(v)
        video_size = byte2unit(v['size_byte'])
        one['Label'] = video_format
        one['Size'] = video_size
        one['Ext'] = v['format']
        # add one info done
        vlist.append(one)
    # done
    return out

# output one video info, return as json obj
def t2one(evinfo, hd):
    # get one info by hd
    v = None
    for i in evinfo['video']:
        if i['hd'] == hd:
            v = i
            break
    # check v
    if v == None:
        raise error.HdError(hd)
        return
    # add urls
    ulist = []
    out = ulist
    # add each url
    for f in v['file']:
        # check f['url']
        if (not 'url' in f) or (f['url'] == None) or (f['url'] == ''):
            ulist.append(None)
            continue	# done, not add more info
        
        # add this file info
        one = {}
        one['Protocol'] = LIEYING_PLUGIN_PROTOCOL
        one['Args'] = LIEYING_PLUGIN_ARGS
        one['Value'] = f['url']
        # add one done
        ulist.append(one)
    # done
    return out

# make_name host function
def make_name_host(title='', title_short='', title_sub='', title_no='', part_i=0, ext='', quality='', site=''):
    raw_name, main_name = make_name.make(title, title_sub, title_no, title_short, quality, site, part_i, make_name_host_num_len, ext)
    # clean file name
    fname = easy_text.clean_file_name(raw_name)
    main_name = easy_text.clean_file_name(main_name)
    return fname, main_name

def make_name_host_num_len(title_no=-1, num_len=4):
    make_num_len = easy_text.make_num_len
    if title_no < 1:
        return ''
    else:
        return make_num_len(title_no, num_len)
    # done

# end tinfo.py


