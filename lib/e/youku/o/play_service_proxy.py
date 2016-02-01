# play_service_proxy.py, parse_video/lib/e/youku/o/
# package com.youku.core.model.PlayServiceProxy

import random

from .. import bridge

# package com.youku.data.PlayerConstant
CTYPE = 10
PLAYSERVICE_NORMAL_SITE = 'play.youku.com'

# PlayServiceProxy.requestPlaylist()
def request_playlist(
        vid, 	# _rootData.videoId
        
        # can be empty
        cid = None, 	# _rootData.partnerId
        yktk = None, 
        r = None, 	# PlayerConfig.partnerData.stealsign
        passwords = None, 
        folder_info = None, 	# for _rootData.type == 'Folder'
        
        # const
        domain = PLAYSERVICE_NORMAL_SITE, 	# getServerDomain()
        ctype = CTYPE):
    # private function requestPlaylist(param1 :Number = 0) :void
    out = 'http://' + domain + '/play/get.json'
    out += '?vid=' + vid + '&ct=' + str(ctype)
    
    if folder_info != None:
        out += '&aid=' + folder_info['fid']
        out += '&pt=' + folder_info['pt']
        out += '&ob=' + folder_info['ob']
    if passwords != None:
        #out += '&pwd=' + escape(passwords)
        out += '&pwd=' + passwords	# TODO
    if cid != None:
        #out += '&cid=' + escape(cid)
        out += '&cid=' + cid	# TODO
    if yktk != None:
        out += '&yktk=' + yktk
    if r != None:
        #out += '&r=' + encodeURIComponent(r)
        out += '&r=' + r	# TODO
    
    out += '&ran=' + str(int(random.random() * 9999))
    return out
    # end request_playlist

# PlayServiceProxy.parseData()
def decode_security(ip, encrypt_string):
    #raw = PlayListUtil.getInstance().getSize(encrypt_string)
    raw = bridge.get_size(encrypt_string)
    sid, tk = raw.split('_')
    
    out = {
        'oip' : ip, 
        'sid' : sid, 
        'tk' : tk, 
    }
    return out

# PlayServiceProxy.getFileId
def get_fileid(raw, index):
    # private function getFileId(param1 :String, param2 :int) :String
    _loc5 = format(index, 'x')
    if len(_loc5) == 1:
        _loc5 = '0' + _loc5
    out = raw[0:8] + _loc5.upper() + raw[10:]
    return out

# end play_service_proxy.py


