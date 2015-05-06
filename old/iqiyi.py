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
import random
import json

# global config
deadpara = 1000

# functions

# base functions
def calmd(t, fileid):
    pass # to getDispatchKey
def get_vrs_encode_code(a1):
    pass # to getVrsEncodeCode

# parse function

def analyse_json(json_obj, tvid):
    
    vs = json_obj['data']['vp']['tkl'][0]['vs']		# .data.vp.tkl[0].vs
    
    data = {}
    data['video'] = []
    
    # get info
    for v in vs:
        files = []
        
        bid = v['bid']
        
        # get each file info
        for f in v['fs']:
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
        one['file'] = files
        # just set file format to flv
        one['type'] = 'flv'
    # TODO

# parse_flv2, a second method to parse flv format video
def parse_flv2(vid, tvid):
    # TODO
    # get info from json
    info = analyse_json(json_obj, tvid)
    
    # get real urls
    info = get_real_urls(info)
    
    # done
    return info

# end iqiyi.py



