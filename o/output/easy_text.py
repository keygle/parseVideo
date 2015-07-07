# easy_text.py, part for parse_video : a fork from parseVideo. 
# easy_text: o/output/easy_text: output result in easy text. 
# version 0.0.11.0 test201507071827
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

# global vars

# base functions

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

# make number length
def make_num_len(n, l=4):
    t = str(n)
    while len(t) < l:
        t = '0' + t
    return t

def clean_file_name(text, remove_chars='/|\\ ?	*<>:\'\"', replace_char='_'):
    to = remove_chars
    out = ''
    for i in text:
        if i in to:
            out += replace_char
        else:
            out += i
    # done
    return out

# functions

# output sample text
'''
=====================================================================
---------------------------------------------------------------------
'''

def output_style(evinfo, flag_simple=False):
    t = []	# output text
    l = ''	# one line text
    # make video info
    info = evinfo['info']
    
    if not flag_simple:
        t += [
            ['info_title', '\n视频信息'], [None, '\n'], 
            ['gray', '=====================================================================\n'], 
        ]
    else:
        t += [
            [None, '\n'], 
        ]
    
    t += [
        [None, ''], 
        ['info_name', '标题	'], ['gray', ': '], ['bold', info['title']], [None, '\n'], 
        ['info_name', '小标题	'], ['gray', ': '], ['blue', info['title_sub']], [None, '\n'], 
    ]
    
    if not flag_simple:
        t += [
            ['info_name', '短标题	'], ['gray', ': '], [None, info['title_short']], [None, '\n'], 
            ['info_name', '集数	'], ['gray', ': '], ['big_blue', str(info['title_no'])], [None, '\n'], 
            ['info_name', '网站	'], ['gray', ': '], ['red', info['site_name']], [None, '\n'], 
            ['info_name', '源 URL	'], ['gray', ': '], ['a', info['url']], [None, '\n'], 
        ]
    
    t += [
        [None, ''], 
    ]
    
    if not flag_simple:
        t += [
            ['info_title', '\n\n下载信息'], 
        ]
    else:
        t += [
            [None, '']
        ]
    
    t += [
        ['gray', '					parse_video 发现 '], 
        ['bold', str(len(evinfo['video']))], ['gray', ' 个 '], [None, '视频'], ['gray', ' ! \n'], 
        ['gray', '=====================================================================\n'], 
        ['bold', '清晰度	'], 
        [None, '     '], ['blue', '分'], ['gray', '辨'], ['blue', '率'], 
        ['red', '       总大小      '], 
        ['blue', 'hd'], 
        [None, '  '], ['gray', '['], [None, '文件格式'], ['gray', ']'], 
        ['green', '            总时长'], 
        #      '1080p    1920 x 1072    1023.61 MB'], ['blue', '   hd=4 [flv]   15 个文件   45:43.12'
        [None, '\n\n'], 
    ]
    
    # NOTE url_count here
    url_count = 0
    
    # make download info
    for v in evinfo['video']:
        # print each video info
        t += [
            [None, '\n'], 
            ['bold', v['quality'] + '	'], 
        ]
        
        # check ok get size_px
        if (v['size_px'][0] < 0) or (v['size_px'][1] < 0):
            size_px_style = 'gray'
        else:
            size_px_style = 'blue'
        
        t += [
            [size_px_style, text_align(5, str(v['size_px'][0]), True)], 
            ['gray', ' x '], 
            [size_px_style, text_align(5, str(v['size_px'][1]))], 
        ]
        
        # check size_byte
        if v['size_byte'] < 0:
            size_byte_style = 'gray'
        else:
            size_byte_style = 'red'
        
        t += [
            [size_byte_style, text_align(14, byte2unit(v['size_byte']), True)], 
            ['blue', text_align(8, '   hd=' + str(v['hd']))], 
            ['gray', ' ['], [None, v['format']], ['gray', '] '], 
            ['bold', text_align(4, str(v['count']), True)], 
            ['gray', ' 个'], [None, '文件 '], 
            ['green', text_align(11, second2time(v['time_s']), True)], 
        ]
        t += [['gray', '\n---------------------------------------------------------------------']]
        
        # add urls
        for f in v['file']:
            t += [[None, '\n']]
            # NOTE add url_count here
            url_count += 1
            
            num_count = make_num_len(url_count)
            
            t += [['select_each_url_count', num_count]]
            
            t += [['a', f['url']]]
            
            # check to add url_more
            if 'url_more' in f:
                more_list = f['url_more']
                # add each item
                for m in more_list:
                    t += [[None, '\n\n']]
                    # add more name, NOTE there use select_each_url_count to add the select button
                    t += [['select_each_url_count', m['name'] + '			']]
                    
                    t += [['a', m['url']]]
            # add url_more items done
        # add urls done
        t += [[None, '\n']]
    # add one video info done
    
    # make output text with style done
    return t

# end output_text.py


