# -*- coding: utf-8 -*-
# iqiyi.py, part for parse_video
# iqiyi: extractor for iqiyi of parse_video. 
# author sceext <sceext@foxmail.com> 2015.04 
# copyright 2015 sceext 
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : parse videos from many websites. 
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

# import modules

# python3 modules
import re
import hashlib

# parse_video modules
from .. import base

# global config
deadpara = 1000
enc_key = 'ts56gh'

# classes

# functions

# base functions
def md5_hash(string):
    return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

# parse function
def parse_flv2(vid, tvid):
    
    pass

# main entry function
def parse(url):
    
    html, err_info = base.cget(url)
    html = html.decode('utf-8')
    
    vids = []
    tvids = []
    tvnames = []
    
    # use re to get info from html
    vids = re.findall('#data-(player|drama)-videoid="([^"]+)"#iU', html)
    tvids = re.findall('#data-(player|drama)-tvid="([^"]+)"#iU', html)
    tvnames = re.findall('#data-videodownload-tvname="([^"]+)"#iU', html)
    
    # get vid and tvid
    if vids[2]:
        vid = vids[2]
    else:
        vid = ''
    if tvids[2]:
        tvid = tvids[2]
    else:
        tvid = ''
    
    # check vid and tvid
    if (vid == '') or (tvid == ''):
        # failed
        return None
    
    # parse video and return info
    data = parse_flv2(vid, tvid)
    
    # add video title
    if tvnames[1]:
        data['title'] = tvnames[1]
    else:
        data['title'] = ''
    
    # done
    return data


# end iqiyi.py



