# -*- coding: utf-8 -*-
# restruct.py, part for parse_video : a fork from parseVideo. 
# parse_video:lib/restruct: restruct output evinfo, key sort. 
# version 0.1.5.0 test201507071335
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

import collections

# global vars
EV_INFO_VERSION = 'evdh info_source info_version 0.2.2.0 test201507071335'

# functions

def restruct_key(old, key_list):
    obj = collections.OrderedDict()
    for key in key_list:
        if key in old:
            obj[key] = old[key]
    return obj

def restruct_info(old):
    key_list = [
        'error', 
        'info_version', 
        'info_source', 
        'extractor', 
        'extractor_name', 
        'title', 
        'title_short', 
        'title_no', 
        'title_sub', 
        'site', 
        'site_name', 
        'url', 
    ]
    return restruct_key(old, key_list)

def restruct_video(old):
    # first sort video by hd
    old.sort(key=lambda item:item['hd'], reverse=True)
    # restruct each video
    video = []
    for one in old:
        video.append(restruct_one_video(one))
    # done
    return video

def restruct_one_video(old):
    key_list = [
        'hd', 
        'quality', 
        'size_px', 
        'size_byte', 
        'time_s', 
        'format', 
        'count', 
        'flag_fix_size', 
    ]
    one = restruct_key(old, key_list)
    # restruct files
    flist = old['file']
    one['file'] = []
    for f in flist:
        one['file'].append(restruct_one_file(f))
    # done
    return one

def restruct_one_file(old):
    key_list = [
        'size', 
        'time_s', 
        'url', 
        'url_more', 
    ]
    return restruct_key(old, key_list)

# restruct info, sort keys
def restruct_evinfo(old):
    evinfo = collections.OrderedDict()
    evinfo['info'] = restruct_info(old['info'])
    evinfo['video'] = restruct_video(old['video'])
    # done
    return evinfo

# end restruct.py


