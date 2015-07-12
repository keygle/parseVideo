# -*- coding: utf-8 -*-
# key.py, part for parse_video : a fork from parseVideo. 
# key: bks1, evparse:lib/bks1/o/base/utils_key.py

# import
import hashlib
import math

# base functions

def md5_hash(string):
    return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

def rotateRight(param1, param2):
    _loc3_ = 0
    _loc4_ = param1
    _loc5_ = 0
    while _loc5_ < param2:
        _loc3_ = _loc4_ & 1
        # TODO
        # _loc4_ = _loc4_ >>> 1
        _loc3_ = _loc3_ << 31
        _loc4_ = _loc4_ + _loc3_
        _loc5_ += 1
    return _loc4_

def getVRSXORCode(param1, param2):
    _loc3_ = param2 % 3
    if _loc3_ == 1:
        return param1 ^ 121
    if _loc3_ == 2:
        return param1 ^ 72
    return param1 ^ 103

# export functions
def getVrsEncodeCode(param1):
    _loc6_ = 0
    _loc2_ = ''
    _loc3_ = param1.split('-')
    _loc4_ = len(_loc3_)
    _loc5_ = _loc4_ - 1
    while _loc5_ >= 0:
        _loc6_ = getVRSXORCode(int(_loc3_[_loc4_ - _loc5_ - 1], 16), _loc5_)
        _loc2_ = chr(_loc6_) + _loc2_
        _loc5_ -= 1
    return _loc2_

def getDispatchKey(param1, param2):
    _loc3_ = ')(*&^flash@#$%a'
    _loc4_ = math.floor(float(param1) / 600)
    return md5_hash(str(_loc4_) + _loc3_ + param2)

def getPassportKey(param1):
    _loc2_ = param1
    _loc3_ = 2.391461978E9	# TODO
    _loc4_ = _loc3_ % 17	# TODO
    _loc2_ = rotateRight(_loc2_, _loc4_)
    _loc5_ = _loc2_ ^ _loc3_
    return str(_loc5_)

# end key.py


