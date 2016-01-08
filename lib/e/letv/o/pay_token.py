# pay_token.py, parse_video/lib/e/letv/o/
# KLetvPlayer, package com.letv.plugins.kernel.controller.auth.pay.LetvPayToken

import time
from .... import b

T_KEY = 'f8da39f11dbdafc03efa1ad0250c9ae6'
T_URL = 'http://yuanxian.letv.com/letv/getService.ldo?from=play&termid=1&end=5'

def gen_url(
        pid, 
        uid, 
        storepath, 
        lc = '', 
        ispay=1):
    # public function start(param1 :Object)
    out = T_URL
    out += '&pid=' + str(pid) + '&userid=' + str(uid) + '&ispay=' + str(ispay)
    out += '&sign=' + b.md5_hash(str(pid) + T_KEY + str(uid))
    out += '&storepath=' + storepath + '&devid=' + lc
    out += '&tn=' + str(int(time.time()))
    return out

# end pay_token.py


