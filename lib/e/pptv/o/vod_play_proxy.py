# vod_play_proxy.py, parse_video/lib/e/pptv/o/
# player4player2.swf, package cn.pplive.player.model.VodPlayProxy

import time
import urllib.parse

from . import ctx_query

# package cn.pplive.player.common.VodParser
ph = [
    'http://web-play.pptv.com', 
    'http://web-play.pplive.cn', 
    'http://211.151.82.252', 
]

PID = 5701	# TODO

def get_play_url(
        cid, 
        
        vvid = '', 	# TODO
        pid = PID, 
        token = None, 
        play_type = 'web.fpp', 
        user_type = 0, 
        os = 0, 
        user_name = '', 
        set_open = False, 
        set_lm = True, 
        ph_count = 0, 
        zone = 8, 
        play_str = None):
    #public function get playUrl() :String
    #if VodCommon.priplay:
    #    return VodCommon.priplay
    out = ph[ph_count]
    if out[-1] != '/':
        out += '/'
    if play_str != None:
        out += '?playStr=' + play_str
    else:
        if set_lm:
            out += 'webplay3'
        else:
            out += 'webplay4'
        out += '-0-' + str(cid) + '.xml' + '?zone=' + str(zone)
        out += '&pid=' + str(pid) + '&vvid=' + str(vvid) + '&version=4'
        if set_open:
            out += '&open=1'
    if token != None:
        out += '&token=' + token
    out += '&username=' + urllib.parse.quote(user_name)
    out += '&param=' + urllib.parse.quote('type=' + play_type + '&userType=' + str(user_type) + '&o=' + str(os))
    # TODO not gen every argument
    pctx = ctx_query.get_pctx()
    if pctx != '':
        out += '&' + pctx
    out += '&' + ctx_query.get_cctx()
    out += '&r=' + str(int(time.time() * 1e3))
    return out
    # end get_play_url

# end vod_play_proxy.py


