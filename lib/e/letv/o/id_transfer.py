# id_transfer.py, parse_video/lib/e/letv/o/
# KLetvPlayer package com.letv.plugins.kernel.controller.auth.transfer.IDTransfer

from . import tkey

# global data
URL = 'http://api.letv.com/mms/out/video/playJson?id='
URL1 = 'http://api.www.letv.com/mms/out/video/playJson?id='
URL2 = 'http://117.121.54.104/mms/out/video/playJson?id='

# KLetvPlayer package com.letv.pluginsAPI.kernel.DefinitionType
STACK = ['350', '1000', '1300', '720p', '1080p']
LW = '350'
SD = '1000'
HD = '1300'
P720 = '720p'
P1080 = '1080p'

# IDTransfer.getURL()
def get_url(
        vid, 
        platid = 1, 
        splatid = 101, 
        domain = 'www.letv.com', 
        devid = '', 	# TODO
        default_d = STACK[-1], 
        base = URL):
    # private function getURL(param1:String) : String
    tk_ = tkey.calcTimeKey(tkey.gen_tm())
    
    out = base + str(vid)
    out += '&platid=' + str(platid)
    out += '&splatid=' + str(splatid)
    out += '&format=1'
    out += '&tkey=' + str(tk_)
    out += '&domain=' + domain
    #if this.model.user.baiduid != None:
    #    out += '&platuid=' + this.model.user.baiduid
    #    out += '&platfrom=baidu'
    out += '&dvtype=' + default_d
    out += '&accessyx=1'
    out += '&devid=' + devid
    return out

# end id_transfer.py


