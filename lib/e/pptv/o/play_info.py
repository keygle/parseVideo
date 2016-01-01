# play_info.py, parse_video/lib/e/pptv/o/
# VodCore.swf, package com.pplive.play.PlayInfo

import time

from . import utils

# package com.pplive.play.Version
version = '1.3.0.19'

server_time_offset = 0

# public function constructCdnURL(param1 :uint, param2 :String = null, param3 :uint = 0, param4 :uint = 0): String
def make_cdn_url(server, filename, index, more={}):
    # NOTE not fully support the function
    out = 'http://' + server + '/' + str(index) + '/' + filename
    out += '?fpp.ver=' + version
    return add_vars(out, more)

# private function addVariables(param1 :String) :String
def add_vars(raw, more):
    out = raw + '&key=' + more['key']
    out += '&k=' + more['k']
    if 'type' in more:
        out += '&' + more['type']
    else:
        out += '&type=web.fpp'
    if 'var' in more:
        out += '&' + more['var']
    return out

# for get file key
def gen_key():
    t = _get_server_time()
    # player4player2.swf, package cn.pplive.player.view.components.VodP2PPlayer.addNetStream()
    # (VodPlay.serverTime - 60 * 1000) / 1000
    key = utils.constructKey((t - 60 * 1e3) / 1e3)
    return key

# TODO may be not stable
def _get_server_time():
    now = int(time.time() * 1e3)
    return now + server_time_offset

# play_info.py


