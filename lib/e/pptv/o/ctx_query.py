# ctx_query.py, parse_video/lib/e/pptv/o/
# player4player2.swf, package cn.pplive.player.view.source.CTXQuery

import re
import urllib.parse

#import flash.net.URLVariables
#import cn.pplive.player.common.VIPPrivilege

flag_isvip = False

# public class CTXQuery
ctx = {}

REG = '{[p|d|a|v|s]+}'	# TODO

# public static function setCTX(param1 :String) :void
def setCTX(param1):
    # TODO can not fully support this function now
    raw = {}
    for i in urllib.parse.unquote(param1).split('&'):
        key, value = i.split('=', 1)
        raw[key] = value
    for i in raw:
        if not 'c' in ctx:
            ctx['c'] = {}
        ctx['c'][i] = raw[i]

# private static function getCTX(param1 :Object, param2 :String) :String
def getCTX(raw, key):
    out = ''
    if not key in raw:
        return out
    a = raw[key]
    for i in a:
        if i != 'isVip':
            if out != '':
                out += '&'
            out += i + '=' + urllib.parse.quote(a[i])
            # if (i == 'type') and VIPPrivilege.isVip and (not 'vip' in a[i]):
            if (i == 'type') and flag_isvip and (not 'vip' in a[i]):
                out += '.vip'
    return out

# public static function get pctx() :String
def get_pctx():
    return getCTX(ctx, 'p')

# public static function get dctx() :String
def get_dctx():
    return getCTX(ctx, 'd')

# public static function get actx() :String
def get_actx():
    return getCTX(ctx, 'a')

# public static function get vctx() :String
def get_vctx():
    return getCTX(ctx, 'v')

# public static function get cctx() :String
def get_cctx():
    return getCTX(ctx, 'c')

# public static function contain(param1 :String) :Boolean
def contain(param1):
    return bool(getAttr(param1))

# public static function getAttr(param1 :String) :String
def getAttr(param1):
    for i in ctx:
        for j in ctx[i]:
            if j == param1:
                return ctx[i][j]
    return None

# public static function setAttr(param1 :String, param2 :String) :void
def setAttr(param1, param2):
    if not 'c' in ctx:
        ctx['c'] = {}
    ctx['c'][param1] = param2

# end ctx_query.py


