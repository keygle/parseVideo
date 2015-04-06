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

# functions

# base functions
def md5_hash(string):
    return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

def calenc(tvid):
    return md5_hash(enc_key + str(deadpara) + tvid)

def calauth_key(tvid):
    return md5_hash('' + str(deadpara) + tvid)

def random_float(min=0, max=1):
    return min + random.random() * (max - min)

def calmd(t, fileid):
    
    l3 = ')(*&^flash@#$%a'
    l4 = math.floor(float(t) / 600)
    
    return md5_hash(str(l4) + l3 + fileid)

def get_vrs_xor_code(a1, a2):
    l3 = a2 %3
    if l3 == 1:
        return (a1 ^ 121)
    elif l3 == 2:
        return (a1 ^ 72)
    else:
        return (a1 ^ 103)

def from_char_code(codes):
    # NOTE this may be not complete
    string = ''
    
    if type(codes) == type(0):
        string += chr(codes)
        return string
    
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

def get_real_urls(raw_urls):
    real_urls = []
    
    # NOTE should get many urls at the same time
    for i in raw_urls:
        url_to = i['url']
        json_raw = base.cget(url_to).decode('utf-8')
        
        if json_raw:
            info = json.loads(json_raw)
            location = info['l']
            
            # NOTE fix iqiyi bug for /videosv0/ to /videos/v0/
            loc = location.replace('/videosv0/', '/videos/v0/', 1)
            
            # just modify it
            i['url'] = loc
    
    # done
    return raw_urls

# parse function

# make request api url
def make_request_url(vid, tvid):
    api_url = 'http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c'
    ap = '&tvId=' + tvid + '&vid=' + vid + '&vinfo=1&tm=' + str(deadpara)
    ap += '&enc=' + calenc(tvid) + '&qyid=08ca8cb480c0384cb5d3db068161f44f&&puid=&authKey='
    ap += calauth_key(tvid) + '&tn=' + str(random_float())
    
    return api_url + ap

def analyse_json(json_obj, tvid):
    
    vs = json_obj['data']['vp']['tkl'][0]['vs']		# .data.vp.tkl[0].vs
    
    time_url = 'http://data.video.qiyi.com/t?tn=' + str(random_float())
    
    # get time data
    json_raw1 = base.cget(time_url).decode('utf-8')
    time_data = json.loads(json_raw1)
    
    server_time = time_data['t']
    
    data = {}
    data['video'] = []
    
    # check info
    if len(vs) < 1:	# failed
        return None
    
    # get info
    for v in vs:
        # can not get 720p and 1080p video now
        if not 'time_s' in data:
            data['time_s'] = v['duration']
        
        files = []
        
        bid = v['bid']
        
        # get each file info
        for f in v['fs']:
            # get part_size, and part_time_s
            part_size = f['b']
            part_time_s = f['d'] / 1e3
            
            # get video real url
            this_link = f['l']
            
            if (bid == 4) or (bid == 5) or (bid == 10):
                this_link = get_vrs_encode_code(this_link)
            
            sp = this_link.split('/')
            sp_length = len(sp)
            
            fileid = sp[sp_length - 1].split('.')[0]
            this_key = calmd(server_time, fileid)
            
            # generate video part file url
            this_link += '?ran=' + str(deadpara)
            this_link += '&qyid=08ca8cb480c0384cb5d3db068161f44f&qypid=' + tvid + '_11&retry=1'
            
            final_url = 'http://data.video.qiyi.com/' + this_key + '/videos' + this_link
            
            one_file = {}
            one_file['url'] = final_url
            one_file['size'] = part_size
            one_file['time_s'] = part_time_s
            
            files.append(one_file)
        
        one = {}
        one['file'] = get_real_urls(files)
        # add part size and part time_s
        # get video format
        if bid == 96:
            one['quality'] = '超低画质'
        elif bid == 1:
            one['quality'] = '低画质'
        elif bid == 2:
            one['quality'] = '中等画质'
        elif bid == 3:
            one['quality'] = '高画质'
        elif bid == 4:
            one['quality'] = '720p'
        elif bid == 5:
            one['quality'] = '1080p'
        elif bid == 10:
            one['quality'] = '4k'
        # just add this video info
        data['video'].append(one)
    # get video sub title
    data['title'] = json_obj['data']['vi']['subt']
    # done
    return data

# parse_flv2, a second method to parse flv format video
def parse_flv2(vid, tvid):
    
    # make request api url
    api_url = make_request_url(vid, tvid)
    
    # http get json info
    json_raw = base.cget(api_url).decode('utf-8')
    
    # parse json string
    json_obj = json.loads(json_raw)
    
    # get info from json
    info = analyse_json(json_obj, tvid)
    
    # done
    return info

# main entry function
def parse(url):
    
    html = base.cget(url).decode('utf-8')
    
    vids = []
    tvids = []
    tvnames = []
    
    # use re to get info from html
    vids = re.findall('data-(player|drama)-videoid="([^"]+)"', html)
    tvids = re.findall('data-(player|drama)-tvid="([^"]+)"', html)
    tvnames = re.findall('data-videodownload-tvname="([^"]+)"', html)
    
    # get vid and tvid
    vid = vids[0][1]
    tvid = tvids[0][1]
    
    # parse video and return info
    info = parse_flv2(vid, tvid)
    
    # add video title
    try:
        info['title'] = tvnames[0] + '_' + info['title']
    except:
        info['title'] = ''
    
    # done
    return info


# end iqiyi.py



