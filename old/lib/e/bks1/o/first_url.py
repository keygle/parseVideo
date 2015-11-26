# first_url.py, parse_video/lib/e/bks1/o
# NOTE get this code from com.qiyi.player.core.model.remote.MixerRemote

import random

from .... import b
from .. import var

def make(vid = None, 
        tvid = None, 
        enc = None, 
        tm = None, 	# should give enc, so tm can not be None
        qyid = '', 	# if not give qyid, will auto gen a uuid from local
        flag_v = False, 
        cid = '', 	# NOTE only for vv
        token = '', 
        uid = '', 
        puid = '', 	# may be empty
        raw_authkey = '', 	# (ugcAuthKey) password for the video, can be empty
        thdk = '', 	# can be empty
        thdt = '', 	# can be empty
        flag_set_vv = False, 
        flag_set_um = False, 
        flag_set_vinfo = True):
    '''
    make the first_url
    return first_url
    '''
    # check input args
    if not qyid:	# gen uuid at local
        qyid = b.gen_uuid()	# NOTE uuid can also be loaded from server
        var._['_qyid'] = qyid	# save qyid
    prefix = var.MIXER_VX_URL + '?key=fvip'
    if flag_v:
        flag_set_um = True
        flag_set_vv = True	# FIXME this may be not right
        prefix = var.MIXER_VX_VIP_URL + '?key=fvinp'
    prefix += '&src=1702633101b340d8917a69cf8a4b8c7c'
    # first_url
    url = prefix
    url += '&tvId=' + tvid + '&vid=' + vid
    if flag_v:
        url += '&cid=' + cid + '&token=' + token + '&uid=' + uid + '&pf=b6c13e26323c537d'
    url += '&vinfo='
    if flag_set_vinfo:
        url += '1'
    else:
        url += '0'
    url += '&tm=' + str(tm) + '&enc=' + enc
    url += '&qyid=' + qyid + '&puid=' + puid
    authkey = b.md5_hash(b.md5_hash(raw_authkey) + str(tm) + tvid)
    url += '&authKey=' + authkey
    url += '&um='
    if flag_set_um:
        url += '1'
    else:
        url += '0'
    if flag_set_vv:
        url += '&vv=821d3c731e374feaa629dcdaab7c394b'
    url += '&thdk=' + thdk + '&thdt=' + thdt + '&rs=1'
    url += '&tn=' + str(random.random())
    # gen first_url done
    return url

# end first_url.py


