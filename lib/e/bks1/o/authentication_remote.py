# authentication_remote.py, parse_video/lib/e/bks1/o/
# package com.qiyi.player.core.model.remote.AuthenticationRemote

# package com.qiyi.player.core.Config
VIP_AUTH_URL = 'http://api.vip.iqiyi.com/services/ckn.action'
OK_CODE = 'A00000'

# AuthenticationRemote.getRequest()
def get_request(
        raw_url, 	# NOTE raw before final URL
        tvid, 
        aid, 
        uid = '', 		# NOTE same as puid
        device_id = '', 	# NOTE same as qyid
        # TODO
        play_type = 'main'): 	# NOTE default value should be ''
    # override protected function getRequest() : URLRequest
    out = {}
    out['version'] = '2.0'
    out['platform'] = 'b6c13e26323c537d'
    out['aid'] = aid
    out['tvid'] = tvid
    out['uid'] = uid
    out['deviceId'] = device_id
    out['playType'] = play_type
    
    # get info from raw before final url
    rid = raw_url.split('?', 1)[0].rsplit('/', 1)[1].rsplit('.', 1)[0]
    
    out['filename'] = rid
    # add qd items
    qd = raw_url.split('?', 1)[1]
    qd_item = qd.split('&')
    for item in qd_item:	# NOTE each item is 'qd_'* item
        key, value = item.split('=', 1)
        out[key] = value
    # make post data, done
    return VIP_AUTH_URL, out

# end authentication_remote.py


