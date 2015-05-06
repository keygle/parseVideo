# -*- coding: utf-8 -*-
# get_base_info.py, part for parse_video : a fork from parseVideo. 
# get_base_info: parse_video/lib/iqiyi 
# version 0.1.0.0 test201505062236
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

from .o import exports
from .. import base

# global vars
user_uuid = ''

# functions

def get_more_info(info):
    more = {}	# output more info
    data = info['data']
    vi = data['vi']
    more['title'] = vi['vn']
    more['sub_title'] = vi['subt']
    more['short_title'] = vi['an']
    more['no'] = vi['pd']
    # done
    return more

def get_info(vid_info, flag_debug=False):
    # create MixerRemote
    mixer = exports.MixerRemote()
    # set data
    mixer.vid = vid_info['vid']
    mixer.tvid = vid_info['tvid']
    # load uuid and set it
    global user_uuid
    um = exports.UUIDManager()
    user_uuid = um.get_uuid()
    mixer.uuid = user_uuid
    # get request url
    url_to = mixer.getRequest()
    # DEBUG info
    if flag_debug:
        print('lib.iqiyi: DEBUG: first url \"' + url_to + '\"')
    try:
        # load it
        info = base.get_json_info(url_to)
    except Exception as err:
        raise Exception('parse_video: ERROR: iqiyi, load first url http error', err)
    # get more info
    more = get_more_info(info)
    # done
    return info, more

# end get_base_info.py


