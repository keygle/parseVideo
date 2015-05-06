# -*- coding: utf-8 -*-
# get_video_info.py, part for parse_video : a fork from parseVideo. 
# get_video_info: parse_video/lib/iqiyi 
# version 0.0.7.0 test201505062141
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.05. 
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

import xml.etree.ElementTree as etree
import math

from .o import exports
from .. import base

from . import get_base_info

get_video_url = exports.get_video_url1

# global vars

POOL_SIZE_GET_VINFO = 4
POOL_SIZE_GET_REAL_URL = 8

BID_TO_HD = {	# video bid to video hd
    '96' : -3, 	# topspeed, 	渣清
    '0' : -2, 	# none, 	超低清
    '1' : -1, 	# standard, 	低清
    '2' : 0, 	# high, 	普清
    '3' : 1, 	# super, 	高清
    '4' : 2, 	# super-high, 	720p
    '5' : 4, 	# fullhd, 	1080p
    '10' : 7, 	# 4k, 		4K
}

# functions

def get_one_video_meta_data(meta_url):
    # load it
    try:
        raw = base.get_html_content(meta_url)
    except Exception as err:
        raise Exception('parse_video: ERROR: iqiyi, get_one_video_meta_data http error', err)
    # parse xml
    root = etree.fromstring(raw)
    flv = root.find('flv')
    to_get_list = [
        'height', 
        'width', 
        'filesize', 
        'duration', 
    ]
    # process it
    meta = {}	# meta info obj
    for i in to_get_list:
        element = flv.find(i)
        meta[i] = element.text
    # done
    return meta

def number(string):	# convert number to string, use int or float
    f = float(string)	# make it float frist
    if math.floor(f) == f:	# check it is int
        return int(f)
    return f

def get_one_file_info(onef, more):
    info = {}	# one file info obj
    info['size'] = onef['b']
    info['time_s'] = onef['d'] / 1e3
    # get file url
    raw_link = onef['l']
    info['url'] = get_video_url.get_one_final_url(raw_link, more)
    # done
    return info

def get_one_info(one_raw):
    raw = one_raw
    vinfo = {}
    vinfo['hd'] = raw['hd']
    vinfo['format'] = 'flv'	# NOTE the format should be flv
    vinfo['file'] = []
    # get video meta data
    meta_url = raw['meta_base'] + raw['meta_url']
    meta = get_one_video_meta_data(meta_url)
    # add more info
    vinfo['size_byte'] = number(meta['filesize'])
    vinfo['time_s'] = number(meta['duration'])
    vinfo['size_px'] = [number(meta['width']), number(meta['height'])]
    # check flag_get_file
    if raw['flag_get_file']:
        # reset size_byte and time_s
        del vinfo['size_byte']
        del vinfo['time_s']
        # make more info
        more = {}
        more['bid'] = raw['bid']
        more['uid'] = raw['uid']
        more['tvid'] = raw['tvid']
        # get server_time and now
        more['server_time'] = get_video_url.get_server_time()
        more['time_now'] = get_video_url.get_time_now()
        # get each file info
        flist = raw['fs']
        for onef in flist:
            onef_info = get_one_file_info(onef, more)
            vinfo['file'].append(onef_info)
    # done
    return vinfo

def get_info(info, hd_min=0, hd_max=0, flag_debug=False, more=None):
    # get video list
    raw_list = info['data']['vp']['tkl'][0]['vs']
    video_list = []
    # get meta data base url
    meta_base = info['data']['vp']['dm']
    # get info from raw to fill video list
    for raw in raw_list:
        one = {}	# one video
        one['fs'] = raw['fs']
        one['meta_url'] = raw['mu']	# video meta data
        one['meta_base'] = meta_base	# add meta_base
        bid = raw['bid']
        # add more info to get final url
        one['bid'] = bid
        # get uid
        one['uid'] = get_base_info.user_uuid
        one['tvid'] = more['tvid']
        # get video hd number by bid
        one['hd'] = BID_TO_HD[str(bid)]
        # add this one
        video_list.append(one)
    # process hd_min and hd_max, set get_file flag
    for one in video_list:
        one['flag_get_file'] = False
        if (one['hd'] >= hd_min) and (one['hd'] <= hd_max):
            one['flag_get_file'] = True
    # sort video by hd
    video_list.sort(key=lambda item:item['hd'], reverse=False)
    # get video info, use base.map_do()
    vinfo = base.map_do(video_list, get_one_info, pool_size=POOL_SIZE_GET_VINFO)
    # TODO get real urls
    # done
    return vinfo

# end get_video_info.py


