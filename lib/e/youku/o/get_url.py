# get_url.py, parse_video/lib/e/youku/o/
# package com.youku.utils.GetUrl

from .. import bridge

# package com.youku.data.PlayerConstant
CTYPE = 10
EV = 1

# GetUrl.getFileParameters()
def get_file_paras(
        index, 		# param1, index number of the video clip
        sid, 		# TODO param2.sid
        filetype,	# TODO param2.fileType
        fileid, 	# TODO param3.fileId
        
        tk, 		# TODO param2.tk
        oip, 		# TODO param2.oip
        
        key = '', 	# TODO param3.key
        
        # TODO unknow
        bctime = 0, 	# TODO PlayerConfig.bctime
        flag_drm = False, 	# param2.drm
        
        # default values
        flag_is_houtai_player = False, 	# PlayerConfig.isHoutaiPlayer
        flag_k4 = False, 	# param4
        flag_show = False, 	# param2.show
        
        # not needed
        p3_type = None, 	# param3.type
        start = 0, 	# param5
        key2 = None, 	# param2.key2
        key1 = None, 	# param2.key1
        iku_flag = None, 	# CoreContext.playerProxy.playerData.IkuFlag
        seconds = None, 	# param3.seconds
        ypp = None, 	# P2PConfig.ypp
        flag_paid = False):	# param2.show.isVideoPaid == 1
    # public static function getFileParameters(param1 :int, param2 :IPlayListData, param3 :VideoSegmentData, param4 :Boolean, param5 :int = 0) :String
    #_loc7 = index.toString(16)
    _loc7 = format(index, 'x')
    if len(_loc7) == 1:
        _loc7 = '0' + _loc7
    out = '/sid/' + sid + '_' + _loc7
    
    _loc8 = filetype
    if flag_is_houtai_player:
        _loc8 = p3_type
    if _loc8 in ['hd2', 'hd3']:
        _loc8 = 'flv'
    if flag_drm:
        _loc8 = 'f4v'
    
    out += '/st/' + _loc8 + '/fileid/' + fileid
    
    if flag_k4:
        if flag_drm:
            out += '?K='
        else:
            out += '?start=' + str(int(start)) + '&K='
    else:
        out += '?K='
    if key == '':
        out += str(key2) + str(key1)
    else:
        out += key
    
    _loc9 = ''
    _loc10 = filetype
    if flag_is_houtai_player:
        _loc10 = p3_type
    if _loc10 in ['flv', 'flvhd']:
        _loc9 = '0'
    elif _loc10 == 'mp4':
        _loc9 = '1'
    elif _loc10 == 'hd2':
        _loc9 = '2'
    elif _loc10 == 'hd3':
        _loc9 = '3'
    # NOTE not needed args
    #out += '&hd=' + _loc9
    #out += '&myp=' + iku_flag
    #out += '&ts=' + str(int(seconds))
    
    if flag_show:
        if flag_paid:
            out += '&ypremium=1'
        else:
            out += '&ymovie=1'
    #out += '&ypp=' + ypp
    
    out += '&ctype=' + str(CTYPE) + '&ev=' + str(EV)
    
    # TODO gen token
    out += '&token=' + str(tk) + '&oip=' + str(oip)
    # NOTE gen ep here, use bridge (ccyouku)
    _loc12 = sid + '_' + fileid + '_' + tk + '_' + str(bctime)
    #_loc13 = PlayListUtil.getInstance().changeSize(_loc12)
    #_raw = _loc12 + '_' + _loc13.substr(0, 4)
    #out += '&ep=' + PlayListUtil.getInstance().setSize(_raw)
    _loc13 = bridge.change_size(_loc12)
    _raw = _loc12 + '_' + _loc13[0:4]
    out += '&ep=' + bridge.set_size(_raw)
    return out
    # end get_file_paras

# package com.youku.core.view.components.BaseVideo
# BaseVideo.requestFileURL()
def request_file_url(*k, **kk):	# will pass many args to get_file_paras
    # protected function requestFileURL() :void
    out = 'http://k.youku.com/player/getFlvPath'
    out += get_file_paras(*k, **kk)
    out += '&yxon=1&special=true'
    return out

# TODO
# end get_url.py


