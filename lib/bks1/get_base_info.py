# -*- coding: utf-8 -*-
# get_base_info.py, part for parse_video : a fork from parseVideo. 
# get_base_info: parse_video/lib/bks1
# version 0.1.8.0 test201507181711
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

import json

from .o import exports
from .. import base

# global vars
user_uuid = ''

# FIXME debug here
FIX_FIRST_HTTP_HEADER = {
#    'Accept-Encoding' : 'gzip', 
}

# functions

def get_more_info(info, vid_info):
    more = {}	# output more info
    data = info['data']
    vi = data['vi']
    more['title'] = vi['vn']
    more['sub_title'] = vi['subt']
    more['short_title'] = vi['an']
    more['no'] = vi['pd']
    # done
    return more

def get_info(vid_info, flag_debug=False, flag_v=False):
    # create MixerRemote
    mixer = exports.MixerRemote()
    # set data
    mixer.vid = vid_info['vid']
    mixer.tvid = vid_info['tvid']
    
    # load uuid and set it
    global user_uuid
    um = exports.UUIDManager()
    user_uuid = um.get_uuid(flag_debug)
    mixer.qyid = user_uuid
    # DEBUG info
    if flag_debug:
        print('lib.bks1: DEBUG: got uuid \"' + user_uuid + '\"')
    
    # set tm
    tm = exports.getTimer()
    mixer.tm = tm
    
    # check vvflag
    vvflag = vid_info['vvflag']
    # NOTE auto turn off flag_v
    if flag_v and (not vvflag):
        flag_v = False
    
    a = None	# AuthRemote obj
    auth_conf = None
    # check flag_v
    if flag_v:
        a, uuid, auth_conf = set_remote_mixer(mixer, vid_info, flag_debug=flag_debug)
        # NOTE save uuid here
        user_uuid = uuid
        
        if flag_debug:
            # DEBUG info
            print('lib.bks1: DEBUG: flag_v, set mixer done')
    
    # get request url
    url_to = mixer.getRequest()
    # DEBUG info
    if flag_debug:
        print('lib.bks1: DEBUG: first url \"' + url_to + '\"')
    try:
        # load it
        info = base.get_json_info(url_to, header=FIX_FIRST_HTTP_HEADER)
    except Exception as err:
        raise Exception('parse_video: ERROR: bks1, load first url http error', err)
    # debug info
    if flag_debug:
        print('lib.bks1: DEBUG: got first url data done. ')
    # get more info
    more = get_more_info(info, vid_info)
    # add a
    more['a'] = a
    more['auth_conf'] = auth_conf
    # done
    return info, more

# 271v, set remote mixer
def set_remote_mixer(mixer, vid_info, flag_debug=False):
    # create a
    a, conf = create_a(vid_info)
    
    # load ck info
    info = load_ck_info(a, conf, flag_debug)
    
    # get token
    t = info['data']['t']
    uuid = conf['qyid']
    
    # DEBUG info
    if flag_debug:
        print('lib.bks1: DEBUG: got token \"' + t + '\"')
    
    # update conf
    conf['token'] = t
    # set remote_mixer
    exports.p271vc.set_remote_mixer(mixer, conf)
    
    # done
    return a, uuid, conf

def create_a(vid_info):
    # load config
    conf = exports.p271vc.load_conf()
    # set auth_remote
    a = exports.vr.AuthRemote()
    a.album_id = vid_info['albumid']
    a.cid = conf['cid']
    a.vid = vid_info['videoid']
    a.uuid = conf['qyid']
    # done
    return a, conf

def create_a2(a):
    a2 = exports.vr.AuthRemote()
    a2.album_id = a.album_id
    a2.cid = a.cid
    a2.vid = a.vid
    a2.uuid = a.uuid
    # done
    return a2

def load_ck_info(a, conf, flag_debug=False):
    # get token url
    raw_data = a.getRequest()
    post_str = exports.vr.make_post_string(raw_data[1])
    
    # DEBUG info
    if flag_debug:
        print('lib.bks1: DEBUG: post to \"' + raw_data[0] + '\" with data \"' + post_str + '\"')
    
    # NOTE use http POST
    post_recv = base.http_post(raw_data[0], post_data=post_str, fix_header=conf['header'], flag_debug=flag_debug)
    
    # clean json text
    text = post_recv.split('{', 1)
    text = '{' + text[1]
    text = text.rsplit('}', 1)
    text = text[0] + '}'
    
    # DEBUG info
    if flag_debug:
        print('lib.bks1: DEBUG: got json text [' + text + ']')
    
    # parse as json
    info = json.loads(text)
    
    # done
    return info

# end get_base_info.py


