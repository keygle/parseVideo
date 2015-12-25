# mixer_remote.py, parse_video/lib/e/bks1/o/
# package com.qiyi.player.core.model.remote.MixerRemote

import random

from ....b import md5_hash
from .. import bridge

# package com.qiyi.player.core.Config
MIXER_VX_URL = 'http://cache.video.qiyi.com/vms'

# MixerRemote.getRequest()
def get_request(
        tvid, 
        vid, 
        tm = None, 
        qyid = '', 	# TODO
        puid = '', 
        flag_set_um = False, 
        flag_set_vv = False, 
        
        flag_set_vinfo = True, 
        ugc_auth_key = '', 
        thdk = '', 
        thdt = '', 
        flag_set_locale = False):
    # override protected function getRequest() : URLRequest
    #
    #this._requestDuration = getTimer()
    #if this._holder.pingBack:
    #    this._holder.pingBack.sendStartLoadVrs()
    
    enc, tm = bridge.bite(tvid, tm=tm)
    
    auth_key = md5_hash(md5_hash(ugc_auth_key) + str(tm) + tvid)
    
    vinfo = 0
    if flag_set_vinfo:
        vinfo = 1
    vv = ''
    if flag_set_vv:
        vv = '&vv=821d3c731e374feaa629dcdaab7c394b'
    um = 0
    if flag_set_um:
        um = 1
    
    out = MIXER_VX_URL + '?key=fvip' + '&src=1702633101b340d8917a69cf8a4b8c7c'
    out += '&tvId=' + tvid + '&vid=' + vid + '&vinfo=' + str(vinfo)
    out += '&tm=' + str(tm) + '&enc=' + enc
    out += '&qyid=' + qyid + '&puid=' + puid
    out += '&authKey=' + auth_key
    out += '&um=' + str(um) + vv + '&pf=b6c13e26323c537d'
    out += '&thdk=' + thdk + '&thdt=' + thdt
    out += '&rs=1' + '&k_tag=1' + '&tn=' + str(random.random())
    
    if flag_set_locale:
        out += '&locale=zh_tw'
    return out
    # end mixer_remote.get_request

# end mixer_remote.py


