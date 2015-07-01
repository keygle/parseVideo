# -*- coding: utf-8 -*-
# parsev.py, part for parse_video : a fork from parseVideo. 
# parsev:o/easy_dl/lib
# version 0.0.1.0 test201507011544
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

import os
import json
import subprocess

# global vars

etc = {}

etc['bin_parsev'] = '../../parsev'
etc['base_path'] = '../'

etc['flag_debug'] = False

# function

# parse, parsev entry function
def parse(url, hd=0, i_min=0, i_max=0, ext_opt=[]):
    
    arg = make_pv_arg(url, hd, i_min, i_max, ext_opt)
    
    # DEBUG info
    if etc['flag_debug']:
        print('easy_dl: DEBUG: start parsev with ' + str(arg) + ' ')
    
    stdout, stderr = run_sub(arg)
    
    # DEBUG info
    if etc['flag_debug']:
        print('easy_dl: DEBUG: got parsev stderr [' + stderr.decode('utf-8', 'ignore') + '] ')
    
    # parse stdout as json, just decode as utf-8
    text = stdout.decode('utf-8')
    
    try:
        evinfo = json.loads(text)
    except Exception as e:
        print('easy_dl: ERROR: parse parsev output as json failed, ' + str(e))
        print('easy_dl: DEBUG: parsev stdout text [' + text + '] ')
        
        return None
    
    # translate info
    pinfo = tinfo(evinfo)
    
    # done
    return pinfo

# base function

def get_pv_path():
    now_dir = os.path.dirname(__file__)
    base_path = os.path.join(now_dir, etc['base_path'])
    
    bin_pv = os.path.join(base_path, etc['bin_parsev'])
    
    # DEBUG info
    if etc['flag_debug']:
        print('easy_dl: DEBUG: got parsev bin path \"' + bin_pv + '\" ')
    
    # done
    return bin_pv

def make_pv_arg(url, hd, i_min, i_max, ext_opt):
    
    pv_bin = get_pv_path()
    
    arg = ['--min', str(hd), '--max', str(hd), '--min-i', str(i_min), '--max-i', str(i_max), url]
    arg = [pv_bin] + ext_opt + arg
    
    return arg

def run_sub(arg, shell=False):
    PIPE = subprocess.PIPE
    
    p = subprocess.Popen(arg, shell=shell, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    
    return stdout, stderr

# translate info
def tinfo(raw):
    pinfo = {}
    
    pinfo['info'] = {}	# video info
    pinfo['list'] = []	# file list info
    
    # add video info
    vinfo = pinfo['info']
    rinfo = raw['info']
    
    vinfo['title'] = rinfo['title']
    vinfo['title_short'] = rinfo['title_short']
    vinfo['title_no'] = rinfo['title_no']
    vinfo['title_sub'] = rinfo['title_sub']
    vinfo['site_name'] = rinfo['site_name']
    
    # select first video
    v = None
    for i in raw['video']:
        if len(i['file']) > 0:
            v = i
            break
    
    if v == None:
        return pinfo	# no more to do
    
    # add more vinfo
    vinfo['hd'] = v['hd']
    vinfo['quality'] = v['quality']
    vinfo['size_px'] = v['size_px']
    vinfo['size_byte'] = v['size_byte']
    vinfo['time_s'] = v['time_s']
    vinfo['format'] = v['format']
    vinfo['count'] = v['count']
    
    # just add list info
    pinfo['list'] = v['file']
    
    # done
    return pinfo

# end parsev.py



