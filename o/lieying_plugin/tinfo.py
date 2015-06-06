# -*- coding: utf-8 -*-
# tinfo.py, part for parse_video : a fork from parseVideo. 
# tinfo: o/lieying_plugin/tinfo: translate info from parse_video to lieying_plugin. 
# version 0.0.1.0 test201506070243
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.06. 
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

from . import error

# global vars
LIEYING_PLUGIN_PROTOCOL = 'http'
LIEYING_PLUGIN_ARGS = []

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

# function

def make_format_text(vinfo):
    pass

def get_hd_from_format_text(format_tex):
    pass

def make_title(tinfo):
    t = '_' + tinfo['title'] + '_' + tinfo['title_sub'] + '_' + tinfo['site_name']
    if tinfo['title_no'] > 0:
        t = make_num_len(tinfo['title_no']) + t
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
        # only add null url list
        one['Urls'] = []
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
    if v == None
        raise error.HdError(hd)
        return
    # add urls
    ulist = []
    out = ulist
    # add each url
    for f in v['file']:
        one = {}
        one['Protocol'] = LIEYING_PLUGIN_PROTOCAL
        one['Args'] = LIEYING_PLUGIN_ARGS
        one['Value'] = f['url']
        # add one done
        ulist.push(one)
    # done
    return out

# end tinfo.py


