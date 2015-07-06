# -*- coding: utf-8 -*-
# entry.py, part for parse_video : a fork from parseVideo. 
# entry: parse_video/lib/bks1
# version 0.2.2.0 test201507061115
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

import re

from .. import base
from .. import error
from . import get_base_info, get_video_info

from .o import s1

# global vars

# version of this extractor
THIS_EXTRACTOR_VERSION = 'parse_video lib/bks1 version 0.3.2.0 test201507061115'

# check supported, week check, not strong check
RE_SUPPORT_URL = []
# http://www.bks1.com/v_19rrn64t40.html
# http://www.bks1.com/w_19rrp737k5.html
# http://yule.bks1.com/pcb.html?src=focustext_0_20130527_7
# http://www.bks1.com/dianying/20130217/e72ffd87c2e9c5af.html
# http://www.bks1.com/dianshiju/sjll_wjt.html
# http://www.bks1.com/dianshiju/20121108/879eec15c7810d10.html
RE_SUPPORT_URL.append('^http://[a-z]+\.' + s1.get_s1()[0] + '\.com/.+\.html')

# global config obj
etc = {}	# NOTE should be set

etc['flag_debug'] = False
etc['flag_v'] = False
etc['flag_v_force'] = False
etc['flag_min_parse'] = False

etc['hd_min'] = 0
etc['hd_max'] = 0

etc['i_min'] = None
etc['i_max'] = None

# functions

def set_config(config):
    # just copy it
    etc['flag_debug'] = config['flag_debug']
    etc['flag_v'] = config['flag_v']
    etc['flag_v_force'] = config['flag_v_force']
    etc['flag_min_parse'] = config['flag_min_parse']
    
    etc['hd_min'] = config['hd_min']
    etc['hd_max'] = config['hd_max']
    
    etc['i_min'] = config['i_min']
    etc['i_max'] = config['i_max']

# get_vid
RE_VID = 'data-(player|drama)-videoid="([^"]+)"'
RE_TVID = 'data-(player|drama)-tvid="([^"]+)"'
RE_ALBUMID = 'data-(player|drama)-albumid="([^"]+)"'
RE_VIDEOID = 'data-(player|drama)-videoid="([^"]+)"'
RE_VVFLAG = 'data-(player|drama)-ismember="([^"]+)"'

def get_vid(url):
    html_text = ''
    try:
        # get html text
        html_text = base.get_html_content(url)
    except Exception as err:
        # check flag_debug
        if etc['flag_debug']:
            raise Exception('parse_video: ERROR: bks1, DEBUG: get_vid http error', err)
        else:
            raise error.NotSupportURLError('not support this url', url, 'load_page')
    # use re to get vid and tvid
    vids = re.findall(RE_VID, html_text)
    tvids = re.findall(RE_TVID, html_text)
    albumids = re.findall(RE_ALBUMID, html_text)
    videoids = re.findall(RE_VIDEOID, html_text)
    vvflags = re.findall(RE_VVFLAG, html_text)
    
    # check supported URL by get vid
    if (len(vids) < 1) or (len(tvids) < 1) or (len(albumids) < 1) or (len(videoids) < 1) or (len(vvflags) < 1):
        # get vid and tvid failed, not support this URL
        raise error.NotSupportURLError('not support this url', url, 'get_vid')
    
    # ok, get vid done
    vid = vids[0][1]
    tvid = tvids[0][1]
    albumid = albumids[0][1]
    videoid = videoids[0][1]
    
    vvflag = vvflags[0][1]
    # process vvflag
    if vvflag == 'true':
        vvflag = True
    else:
        vvflag = False
    # check flag_v_force
    if etc['flag_v_force']:
        vvflag = True
    
    # done
    vid_info = {}
    vid_info['vid'] = vid
    vid_info['tvid'] = tvid
    vid_info['albumid'] = albumid
    vid_info['videoid'] = videoid
    vid_info['vvflag'] = vvflag
    
    return vid_info

def parse(url_to):	# this site entry main entry function
    # frist re-check url, if supported by this
    flag_support = False
    for r in RE_SUPPORT_URL:
        if re.match(r, url_to):
            flag_support = True
            break
    if not flag_support:
        raise error.NotSupportURLError('not support this url', url_to)
    # create evinfo
    evinfo = {}
    evinfo['info'] = {}
    evinfo['video'] = []
    # add some base info
    evinfo['info']['url'] = url_to
    evinfo['info']['site'] = 'bks1'
    # get vid
    vid_info = get_vid(url_to)
    # get base, more info
    info, more = get_base_info.get_info(vid_info, flag_debug=etc['flag_debug'], flag_v=etc['flag_v'])
    # add more info
    evinfo['info']['title'] = more['title']
    evinfo['info']['title_sub'] = more['sub_title']
    evinfo['info']['title_short'] = more['short_title']
    evinfo['info']['title_no'] = more['no']
    # make more info
    more_info = {}
    more_info['vid_info'] = vid_info
    more_info['a'] = more['a']
    more_info['auth_conf'] = more['auth_conf']
    # get video info
    evinfo['video'] = get_video_info.get_info(
    				info, 
    				more=more_info, 
    				url=url_to, 
    				
    				hd_min=etc['hd_min'], 
    				hd_max=etc['hd_max'], 
    				
    				i_min=etc['i_min'], 
    				i_max=etc['i_max'], 
    				
    				flag_debug=etc['flag_debug'], 
    				flag_v=etc['flag_v'], 
    				
    				flag_min_parse=etc['flag_min_parse'])
    
    # done
    return evinfo

# end entry.py


