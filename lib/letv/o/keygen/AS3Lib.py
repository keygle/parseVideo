# -*- coding: utf-8 -*-
# AS3Lib.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# AS3Lib: letv/timestamp_flascc, com.letv.keygen

# import
import hashlib

# base functions
def md5_hash(string):
    return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

# functions

# def ror(param1:int, param2:int): int
def ror(param1, param2):	# TODO may be not stable
    _loc3_ = 0
    while _loc3_ < param2:
        # param1 = (param1 >>> 1) + ((param1 & 1) << 31)
        param1 = (param1 >> 1) + ((param1 & 1) << 31)
        _loc3_ += 1
    return param1

# def calcTimeKey(param1:int): int
def calcTimeKey(param1):
    _loc2_ = 773625421
    _loc3_ = ror(param1, _loc2_ % 13)
    _loc3_ = _loc3_ ^ _loc2_
    _loc3_ = ror(_loc3_, _loc2_ % 17)
    return _loc3_

# def calcURLKey(param1:String, param2:String, param3:int): String
def calcURLKey(param1, param2, param3):
    _loc4_ = 'drwfad012b0580d706'
    return md5_hash(param1 + param2 + str(param3) + _loc4_)

# def calcLiveKey(param1:String, param2:int): String
def calcLiveKey(param1, param2):
    _loc3_ = 'a2915e518ba60169f77'
    return md5_hash(param1 + ',' + str(param2) + ',' + _loc3_)

# end AS3Lib.py


