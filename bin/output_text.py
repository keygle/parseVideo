# output_text.py, part for parse_video : a fork from parseVideo. 
# output_text: bin/output_text: output result in easy text. 
# version 0.0.5.0 test201506052105
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
import math

# global vars

# functions

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

def text_align(length, text, right=False):
    if right:
        while len(text) < length:
            text = ' ' + text
    else:
        while len(text) < length:
            text += ' '
    return text

# output sample text
'''
=====================================================================
---------------------------------------------------------------------
'''

def make_easy_text(evinfo, flag_write_output_file=False):
    t = []	# output text
    l = ''	# one line text
    # make video info
    info = evinfo['info']
    t.append('')
    t.append('视频信息')
    t.append('=====================================================================')
    t.append('标题      : ' + info['title'])
    t.append('小标题    : ' + info['title_sub'])
    t.append('短标题    : ' + info['title_short'])
    t.append('集数      : ' + str(info['title_no']))
    t.append('网站      : ' + info['site_name'])
    t.append('源 URL    : ' + info['url'])
    t.append('')
    t.append('下载信息                           parse_video 发现 ' + str(len(evinfo['video'])) + ' 个 视频 ! ')
    t.append('=====================================================================')
    t.append('清晰度     分辨率         总大小     hd  [文件格式]            总时长')
    # append('1080p    1920 x 1072    1023.61 MB   hd=4 [flv]   15 个文件   45:43.12')
    t.append('')
    # make download info
    for v in evinfo['video']:
        # print each video info
        l = ''	# video info
        l += text_align(9, v['quality'])
        l += text_align(10, str(v['size_px'][0]) + ' x ' + str(v['size_px'][1]), True)
        l += text_align(14, byte2unit(v['size_byte']), True)
        l += text_align(7, '   hd=' + str(v['hd']))
        l += text_align(5, ' [' + v['format'] + '] ')
        l += text_align(4, str(v['count']), True)
        l += ' 个文件 '
        l += text_align(11, second2time(v['time_s']), True)
        t.append(l)
        t.append('---------------------------------------------------------------------')
        # add urls
        for f in v['file']:
            t.append(f['url'])
        # add urls done
        t.append('')
    # add one video info done
    
    # make final text
    t = ('\n').join(t)
    # done
    return t

# end output_text.py


