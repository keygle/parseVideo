# -*- coding: utf-8 -*-
# get_video_info.py, part for parse_video : a fork from parseVideo. 
# get_video_info: parse_video/lib/letv
# version 0.0.5.0 test201507071806
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

from .o import exports

# global vars

DISPATCH_TYPE_TO_HD = {	# letv video dispatch type to hd
    '350' : -3, 	# 350, 		渣清
    '1000' : -1, 	# 1000, 	低清
    '1300' : 0, 	# 1300, 	普清
    '720p' : 2, 	# 720p, 	720p
    '1080p' : 4, 	# 1080p, 	1080p
}

# base functions
def number(string):	# convert number to string, use int or float
    f = float(string)	# make it float frist
    if math.floor(f) == f:	# check it is int
        return int(f)
    return f

# functions
def get_info(info, hd_min=0, hd_max=0, flag_debug=False, flag_fix_size=False, flag_enable_parse_more=False):
    # get video list
    playurl = info['playurl']
    domain_list = playurl['domain']
    video_time_s = number(playurl['duration'])
    raw_list = playurl['dispatch']
    # make video list
    video_list = []
    # debug info
    if flag_debug:
        print('lib.letv: DEBUG: getting video info ... ')
    # get info from raw to fill video list
    for i in raw_list:
        one = {}	# one video
        # get hd
        hd = DISPATCH_TYPE_TO_HD[i]
        one['hd'] = hd
        one['dispatch'] = raw_list[i]
        one['domain'] = domain_list
        one['time_s'] = video_time_s
        
        # add rateid
        one['rateid'] = i
        # add flags
        one['flag_debug'] = flag_debug
        one['flag_enable_parse_more'] = flag_enable_parse_more
        
        # add one info
        video_list.append(one)
    # process hd_min and hd_max, set get_file flag
    for one in video_list:
        one['flag_get_file'] = True
        one['flag_fix_size'] = True
        if (one['hd'] >= hd_min) and (one['hd'] <= hd_max):
            one['flag_fix_size'] = False
        # check fix size
        elif not flag_fix_size:
            one['flag_get_file'] = False
            one['flag_fix_size'] = False
    # sort video by hd
    video_list.sort(key=lambda item:item['hd'], reverse=False)
    # get each video info, no need to use map_do()
    vinfo = []
    for one in video_list:
        onev = get_one_info(one)
        # set flag_fix_size
        if one['flag_fix_size']:
            onev['flag_fix_size'] = True
        
        vinfo.append(onev)
    # get video info done
    # done
    return vinfo

def get_one_info(one_raw):
    raw = one_raw
    vinfo = {}
    vinfo['hd'] = raw['hd']
    
    # get flags
    flag_debug = raw['flag_debug']
    flag_enable_parse_more = raw['flag_enable_parse_more']
    
    # get info from o.exports
    domain = raw['domain']
    dispatch = raw['dispatch']
    rateid = raw['rateid']
    
    # check parse_more flag
    if flag_enable_parse_more and (not raw['flag_fix_size']):
        final_info = exports.letv_more_url.parse_more_url(domain, dispatch, rateid, flag_debug=flag_debug)
    else:	# use old parse method
        final_info = exports.youtube_dl_letv.get_real_url(domain, dispatch)
    
    # add more video info
    vinfo['format'] = final_info['ext']
    vinfo['file'] = []
    # add more info
    vinfo['size_byte'] = -1	# TODO not support this
    vinfo['time_s'] = raw['time_s']
    vinfo['size_px'] = [-1, -1]	# TODO not support this
    # add count
    vinfo['count'] = 1	# for letv, count should be 1
    # check flag_get_file
    if raw['flag_get_file']:
        # add file info
        onef = {}
        onef['size'] = -1	# TODO not support this
        onef['time_s'] = raw['time_s']
        # add final url
        onef['url'] = final_info['url']
        
        # check url_more
        if 'url_more' in final_info:
            onef['url_more'] = final_info['url_more']
        
        # TODO check set user_agent and referer
        vinfo['file'].append(onef)
    # get video info done
    return vinfo

# end get_video_info.py


