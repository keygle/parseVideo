# tkey.py, parse_video/lib/e/letv/o/
# KLetvPlayer.tkey package com.letv.keygen.AS3Lib

import time
from ....b import md5_hash

# global data
etc = {}
etc['stime'] = 0
etc['now_time'] = 0

# private function ror(param1:int, param2:int) : int
def ror(param1, param2):
    for i in range(param2):
        # TODO
        #param1 = (param1 >>> 1) + ((param1 & 1) << 31)
        param1 = (param1 >> 1) + ((param1 & 1) << 31)
    return param1

# public function calcTimeKey(param1:int) : int
def calcTimeKey(param1):
    _loc2 = 773625421
    _loc3 = ror(param1, _loc2 % 13)
    _loc3 = _loc3 ^ _loc2
    _loc3 = ror(_loc3, _loc2 % 17)
    return _loc3

# public function calcURLKey(param1:String, param2:String, param3:int) : String
def calcURLKey(param1, param2, param3):
    _loc4 = 'drwfad012b0580d706'
    return md5_hash(param1 + param2 + str(param3) + _loc4)

# public function calcLiveKey(param1:String, param2:int) : String
def calcLiveKey(param1, param2):
    _loc3 = 'a2915e518ba60169f77'
    return md5_hash(param1 + ',' + str(param2) + ',' + _loc3)

# KLetvPlayer package com.letv.plugins.kernel.tools.TimeStamp
def gen_tm():
    # private function get tm() : int
    if etc['stime'] > 0:
        return etc['stime'] + int((_get_time() - etc['now_time']) * 1e-3)
    return int(_get_time() * 1e-3)

def _get_time():
    return int(time.time() * 1e3)

def set_stime(stime):
    etc['stime'] = stime
    etc['now_time'] = _get_time()

# end tkey.py


