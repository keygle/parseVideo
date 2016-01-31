# player.py, parse_video/lib/e/vqq/o/, TencentPlayer.swf

import random

from ..var import var
from .. import bridge

APP_VER = '3.2.19.346'

# player global config data
CGI_GETVINFO = 'http://vv.video.qq.com/getvinfo'
CGI_GETKEY   = 'http://vv.video.qq.com/getvkey'
CGI_GETCLIP  = 'http://vv.video.qq.com/getvclip'
CGI_GETINFO  = 'http://vv.video.qq.com/getinfo'
CGI_QZGETINFO = 'http://uv.video.qq.com/qzgetinfo'
CGI_QZGETKEY  = 'http://uv.video.qq.com/qzgetkey'
CGI_STGETINFO = 'http://sv.video.qq.com/edugetvinfo'
CGI_STGETKEY  = 'http://sv.video.qq.com/edugetvkey'
CGI_STGECLIP  = 'http://sv.video.qq.com/edugetvclip'

def gen_ckey(vid):
    ckey_info = bridge.gen_ckey(vid, platform=var._['platform'])
    return ckey_info

# key POST functions

# POST getvinfo, make post data, return {'url' :, 'post_data' :, 'header' :, }
def getvinfo(vid, video_format=None, charge=0):
    raw = gen_ckey(vid)
    post_data = {	# make post data
        'encryptVer' 	: raw['enc_ver'], 
        'appver' 	: raw['player_ver'], 
        'platform' 	: raw['platform'], 
        'vid' 		: raw['vid'], 
        'cKey' 		: raw['ckey'], 
        'otype' 	: 'xml', 
        'ran' 		: random.random(), 
        
        'vids' 		: raw['vid'], 
        'utype' 	: var._['utype'], 
        
        'defnpayver' 	: '1', 
        'fp2p' 		: '1', 
        'charge' 	: charge, 
        
        # NOTE use auto format (vtype)
        'fhdswitch' 	: '0', 
        # TODO just reserved
        #'guid' 	: TODO
        #'ehost' 	: TODO
        #'speed' 	: TODO
        #'pid' 		: TODO
    }
    if video_format:	# check vtype
        post_data.update({
            'fhdswitch' 	: '1', 	# NOTE this should be 1
            'defaultfmt' 	: video_format, 
            'defn' 		: video_format, 
        })
    # add other info
    post_header = var._BASE_POST_HEADER
    return {
        'url' : CGI_GETVINFO, 
        'post_data' : post_data, 
        'header' : post_header, 
    }

# POST getvkey, return {'url' :, 'post_data' :, 'header' :, }
def getvkey(vid, format_, vt, filename, charge=0):
    raw = gen_ckey(vid)
    post_data = {	# make post data
        'encryptVer' 	: raw['enc_ver'], 
        'appver' 	: raw['player_ver'], 
        'platform' 	: raw['platform'], 
        'vid' 		: raw['vid'], 
        'cKey' 		: raw['ckey'], 
        'otype' 	: 'xml', 
        'ran' 		: random.random(), 
        
        'format' 	: format_, 
        'vt' 		: vt, 
        'filename' 	: filename, 
        
        'charge'	: charge, 
        # TODO just reserved
        #'guid' 	: TODO
        #'ehost' 	: TODO
    }
    # add more info
    post_header = var._BASE_POST_HEADER
    return {
        'url' : CGI_GETKEY, 
        'post_data' : post_data, 
        'header' : post_header, 
    }

# POST getvclip
def getvclip(vid, idx, fmt, format_, vt, charge=0):
    raw = gen_ckey(vid)
    post_data = {
        'encryptVer' 	: raw['enc_ver'], 
        'appver' 	: raw['player_ver'], 
        'platform' 	: raw['platform'], 
        'vid' 		: raw['vid'], 
        'cKey' 		: raw['ckey'], 
        'otype' 	: 'xml', 
        'ran' 		: random.random(), 
        
        'fmt' 		: fmt, 
        'format' 	: format_, 
        'idx' 		: idx, 
        
        'vt' 		: vt, 
        'charge' 	: charge, 
        'buffer' 	: 0, 
        'dltype' 	: 1, 
        # TODO NOTE just reserved
        #'ltime' 	: 0
        #'guid' 	: TODO
        #'ehost' 	: TODO
        #'speed' 	: TODO
    }
    post_header = var._BASE_POST_HEADER
    return {
        'url' : CGI_GETCLIP, 
        'post_data' : post_data, 
        'header' : post_header, 
    }


# end player.py


