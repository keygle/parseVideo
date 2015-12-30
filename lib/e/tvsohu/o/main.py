# main.py, parse_video/lib/e/tvsohu/o/, Main.swf

import random

# package com.sohu.tv.mediaplayer.PlayerConfig
FETCH_VINFO_PATH = 'http://hot.vrs.sohu.com/vrs_flash.action?vid='
FETCH_VINFO_PATH_TRANSITION = 'http://hot.vrs.sohu.com/vrs_vms.action?p=flash&old='
FETCH_VINFO_PATH_MYTV = 'http://my.tv.sohu.com/play/videonew.do?vid='
FETCH_LIVE_PATH = 'http://live.tv.sohu.com/live/player_json.jhtml?encoding=utf-8&lid='
FETCH_VINFO_SUB_IP = ['220.181.118.25', '220.181.118.181', '123.126.48.47', '123.126.48.48']

# package configbag.Config
schedulIP = 'data.vod.itc.cn'	# or 220.181.61.211, 220.181.61.212
CONFIG_version = '1512071747'

# package server.LoadFromCDN
UA_PREFIX = 'sohuce:'

def gen_first_url(vid):
    out = FETCH_VINFO_PATH + str(vid) + '&t=' + str(random.random())
    return out

def gen_before_url(new, vid, tvid, ch, prod='flash'):
    out = 'http://' + schedulIP + '/cdnList?new=' + new
    out += '&vid=' + str(vid) + '&tvid=' + str(tvid)
    out += '&ch=' + ch + '&prod=' + prod
    return out

def gen_user_agent():
    out = UA_PREFIX + CONFIG_version
    return out

# end main.py


