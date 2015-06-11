# -*- coding: utf-8 -*-
# get_base_info.py, part for parse_video : a fork from parseVideo. 
# parse_video: lib/letv/get_base_info
# version 0.0.5.0 test201506111905
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

transfer = exports.transfer

# global vars

# functions

def get_info(vid_info, flag_debug=False):
    # create transfer
    idt = transfer.IDTransfer()
    
    # try to one get info
    info = try_one_get_info(idt, vid_info['vid'], flag_debug=flag_debug)
    # load more info
    more_raw = load_more_info(info, flag_debug=flag_debug)
    
    # get more info
    more = get_more_info(info, more_raw)
    # done
    return info, more

def get_more_info(info, more_raw):
    more = {}	# more info
    video_no = more_raw['position']
    this_info = more_raw['data'][video_no - 1]
    # get it
    more['title'] = this_info['title']
    more['sub_title'] = this_info['subTitle']
    more['short_title'] = ''	# TODO not support this now
    more['no'] = this_info['key']
    # done
    return more

# TODO if load failed, should update set server_time (stime), and retry load
def try_one_get_info(id_transfer, vid, flag_debug=False):
    # try one time to get info
    
    # get url
    info_url = id_transfer.getURL(vid)
    # NOTE for debug
    if flag_debug:
        print('DEBUG: lib.letv, base_info url \"' + info_url + '\" ')
    # load json
    info = base.get_json_info(info_url)
    # done
    return info

def load_more_info(info, flag_debug=False):
    # create ListNewProxy
    lnp = exports.ListNewProxy()
    # set it
    play_url = info['playurl']
    lnp.vid = play_url['vid']
    lnp.pid = play_url['pid']
    lnp.cid = play_url['cid']
    # get url
    info_url = lnp.load()
    # NOTE for debug
    if flag_debug:
        print('DEBUG: lib.letv, more_info url \"' + info_url + '\" ')
    # load it
    raw = base.get_json_info(info_url)
    # done
    return raw

# end get_base_info.py


