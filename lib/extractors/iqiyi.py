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
import random
import math
import json

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

def calenc(tvid):
    return md5_hash(enc_key + deadpara + tvid)

def calauth_key(tvid):
    return md5_hash('' + deadpara + tvid)

def random_float(min=0, max=1):
    return min + random.random() * (max - min)

def calmd(t, fileid):
    
    l3 = ')(*&^flash@#$%a'
    l4 = math.floor(t / 600)
    
    return md5_hash(l4 + l3 + fileid)

def get_vrs_xor_code(a1, a2):
    l3 = a2 %3
    if l3 == 1:
        return (a1 ^ 121)
    elif:
        return (a1 ^ 72)
    else:
        return (a1 ^ 103)

def from_char_code(codes):
    # NOTE this may be not complete
    string = ''
    
    for i in codes:
        string += chr(i)
    
    return string

def get_vrs_encode_code(a1):
    
    l2 = ''
    l3 = a1.split('-')
    l4 = len(l3)
    l5 = l4 - 1
    
    while l5 > 0:
        l6_1 = int(l3[l4 - l5 - 1], 16)
        l6 = get_vrs_xor_code(l6_1, l5)
        
        l2 = from_char_code(l6) + l2
        
        l5 -= 1
    
    return l2

# parse function

# make request api url
def make_request_url(tvid):
    api_url = 'http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c'
    ap = '&tvId=' + tvid + '&vid=' + vid + '&vinfo=1&tm=' + deadpara
    ap += '&enc=' + calenc(tvid) + '&qyid=08ca8cb480c0384cb5d3db068161f44f&&puid=&authKey='
    ap += caluth_key(tvid) + '&tn=' + random_float()
    
    return api_url + ap

def analyse_json(json_obj):
    
    vs = json_obj['data']['vp']['tkl'][0]['vs']		# .data.vp.tkl[0].vs
    
    time_url = 'http://data.video.qiyi.com/t?tn=' + random_float()
    # get time data
    content1, info_err = base.cget(time_url)
    json_raw1 = content1.decode('utf-8')
    time_data = json.loads(json_raw1)
    
    server_time = time_data['t']
    
    urls_data = []
    data = []
    
    # check info
    if (type(vs) != type([])) or (len(vs) < 1):	# failed
        return None
    
    # get info
    for i in vs:
        # can not get 720p and 1080p video now
        data['seconds'] = i['duration']
        
        pass
    
    pass

# parse_flv2, a second method to parse flv format video
def parse_flv2(vid, tvid):
    
    # make request api url
    api_url = make_request_url(tvid)
    
    # http get json info
    json_raw, info_err = base.cget(api_url)
    json_text = json_raw.decode('utf-8')
    
    # FIXME debug here
    print(json_text)
    return
    
    # parse json string
    json_obj = json.loads(json_text)
    
    # get info from json
    info = analyse_json(json_obj)
    
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



