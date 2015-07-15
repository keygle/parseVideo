# -*- coding: utf-8 -*-
# AS3Lib.py, part for parse_video : a fork from parseVideo. 
# letv/o/keygen: timestamp_flascc, com.letv.keygen
# last_update 2015-07-15 13:48 GMT+0800 CST

# import
import hashlib

# base functions
def md5_hash(string):
    return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

# functions

# function ror(param1 :int, param2 :int): int
def ror(param1, param2):
    _loc3 = 0
    while _loc3 < param2:
        # param1 = (param1 >>> 1) + ((param1 & 1) << 31)
        param1 = (param1 >> 1) + ((param1 & 1) << 31)
        _loc3 += 1
    return param1

# function calcTimeKey(param1 :int): int
def calcTimeKey(param1):
    _loc2 = 773625421
    _loc3 = ror(param1, _loc2 % 13)
    _loc3 = _loc3 ^ _loc2
    _loc3 = ror(_loc3, _loc2 % 17)
    return _loc3

# function calcURLKey(param1 :String, param2 :String, param3 :int): String
def calcURLKey(param1, param2, param3):
    _loc4 = 'drwfad012b0580d706'
    return md5_hash(param1 + param2 + param3 + _loc4)

# function calcLiveKey(param1 :String, param2 :int): String
def calcLiveKey(param1, param2):
    var _loc3 = 'a2915e518ba60169f77'
    return md5_hash(param1 + ',' + param2 + ',' + _loc3)

# end AS3Lib.py


