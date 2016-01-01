# utils.py, parse_video/lib/e/pptv/o/
# player4player2.swf, package cn.pplive.player.utils.Utils

import math
import random

from ....b import flash

# import flash.utils.ByteArray
# import flash.net.URLVariables
# public class Utils
#BASE64_KEY = 'kioe257ds'
#BASE64_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
SERVER_KEY = 'qqqqqww'
# public static const DELTA :uint = 2.654435769E9
DELTA = 2654435769
#public static var ChListId :String
#public static var ChannelId :String
#public static var CatalogId :String

# public static function constructKey(param1 :Number) :String
def constructKey(param1):
    raw = time2String(param1)
    if len(raw) < 16:
        raw = add(raw, 16 - len(raw))
    k = SERVER_KEY
    if len(k) < 16:
        k = add(k, 16 - len(k))
    out = encrypt(raw, k)
    out = Str2Hex(out)
    return out

# public static function getCharFromAscii(param1 :uint) :String
def getCharFromAscii(code):
    return chr(code)

# public static function add(param1 :String, param2 :Number) :String
def add(raw, length):
    for i in range(length):
        raw += getCharFromAscii(0)
    return raw

# public static function getkey(param1: String) :uint
def getkey(raw):
    out = 0
    for i in range(len(raw)):
        out = out ^ (ord(raw[i]) << i % 4 * 8)
    return out

# public static function time2String(param1 :Number) :String
def time2String(raw):
    #_loc3 :ByteArray = new ByteArray()
    k = '0123456789abcdef'
    out = ''
    for i in range(8):
        #j = param1 >>> 28 - i % 8 * 4 & 15
        j = int(raw) >> 28 - i % 8 * 4 & 15
        out += k[j]
    return out

# public static function Str2Hex(param1 :String) :String
def Str2Hex(raw):
    k = '0123456789abcdef'
    # out = new Array(2 * len(raw) + 1)
    out = ['' for i in range(2 * len(raw) + 1)]
    for i in range(len(raw)):
        if i < 8:
            #_loc7 = ord(raw[i]) & 15
            #_loc8 = ord(raw[i]) >>> 4 & 15
            out[2 * i] = k[ord(raw[i]) & 15]
            # out[2 * i + 1] = k[ord(raw[i]) >>> 4 & 15]
            out[2 * i + 1] = k[ord(raw[i]) >> 4 & 15]
        else:
            out[2 * i] = k[math.floor(random.random() * 15)]
            out[2 * i + 1] = k[math.floor(random.random() * 15)]
    return ('').join(out)

# public static function encrypt(param1 :String, param2 :String) :String
def encrypt(param1, param2):
    # NOTE fix for bit operations
    uint = flash.uint
    l2 = flash.l2
    r3 = flash.r3
    
    _loc5 = 0
    _loc6 = 0
    _loc7 = 0
    _loc13 = 0
    _loc14 = 0
    _loc15 = 0
    _loc16 = 0
    _loc17 = 0
    _loc18 = 0
    _loc19 = 0
    _loc20 = 0
    _loc21 = 0
    _loc22 = 0
    _loc23 = 0
    _loc24 = 0
    _loc25 = 0
    _loc26 = 0
    _loc27 = 0
    _loc28 = 0
    _loc29 = 0
    _loc30 = 0
    _loc31 = 0
    _loc32 = 0
    _loc33 = 0
    _loc34 = 0
    _loc35 = 0
    _loc36 = 0
    _loc37 = 0
    _loc38 = 0
    _loc39 = 0
    _loc40 = 0
    _loc41 = 0
    _loc3 = 16
    _loc4 = uint(getkey(param2))
    _loc8 = [i for i in param1]
    _loc9 = [i for i in param2]
    _loc10 = uint(_loc4)
    _loc5 = uint(l2(_loc10, 8) | r3(_loc10, 24))
    _loc6 = uint(l2(_loc10, 16) | r3(_loc10, 16))
    _loc7 = uint(l2(_loc10, 24) | r3(_loc10, 8))
    _loc11 = ''
    _loc12 = 0
    while _loc12 + _loc3 <= len(_loc8):
        _loc13 = l2(ord(_loc8[_loc12]), 0)
        _loc14 = l2(ord(_loc8[_loc12 + 1]), 8)
        _loc15 = l2(ord(_loc8[_loc12 + 2]), 16)
        _loc16 = l2(ord(_loc8[_loc12 + 3]), 24)
        _loc17 = l2(ord(_loc8[_loc12 + 4]), 0)
        _loc18 = l2(ord(_loc8[_loc12 + 5]), 8)
        _loc19 = l2(ord(_loc8[_loc12 + 6]), 16)
        _loc20 = l2(ord(_loc8[_loc12 + 7]), 24)
        _loc21 = uint(0 | _loc13 | _loc14 | _loc15 | _loc16)
        _loc22 = uint(0 | _loc17 | _loc18 | _loc19 | _loc20)
        _loc23 = 0
        _loc24 = 0
        while _loc24 < 32:
            _loc23 = uint(_loc23 + DELTA)
            _loc33 = uint(l2(_loc22, 4) + _loc4)
            _loc34 = uint(_loc22 + _loc23)
            _loc35 = uint(r3(_loc22, 5) + _loc5)
            _loc36 = uint(_loc33 ^ _loc34 ^ _loc35)
            _loc21 = uint(_loc21 + _loc36)
            _loc37 = uint(l2(_loc21, 4) + _loc6)
            _loc38 = uint(_loc21 + _loc23)
            _loc39 = r3(_loc21, 5)
            _loc40 = uint(_loc39 + _loc7)
            _loc41 = uint(_loc37 ^ _loc38 ^ _loc40)
            _loc22 = uint(_loc22 + _loc41)
            _loc24 += 1
        _loc25 = r3(_loc21, 0) & 255
        _loc26 = r3(_loc21, 8) & 255
        _loc27 = r3(_loc21, 16) & 255
        _loc28 = r3(_loc21, 24) & 255
        _loc29 = r3(_loc22, 0) & 255
        _loc30 = r3(_loc22, 8) & 255
        _loc31 = r3(_loc22, 16) & 255
        _loc32 = r3(_loc22, 24) & 255
        _loc11 = _loc11 + getCharFromAscii(r3(_loc21, 0) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc21, 8) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc21, 16) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc21, 24) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc22, 0) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc22, 8) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc22, 16) & 255)
        _loc11 = _loc11 + getCharFromAscii(r3(_loc22, 24) & 255)
        _loc12 = _loc12 + _loc3
    _loc11 = _loc11 + param1[8:8 + 8]
    return _loc11

# end utils.py


