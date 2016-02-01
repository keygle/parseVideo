# kill_ccyouku_bridge.py, parse_video/lib/bridge/, for extractor youku
# package com.youku.utils.PlayListUtil

# TODO improve sandwich_bridge support for parse_video

import os
from .ccyk_bridge.sandwich_bridge import sdw_up as up

from ..b import log

# NOTE set bridge callback function here
youku_set_size = None		# setSize(str) -> str
youku_get_size = None		# getSize(str) -> str
youku_change_size = None	# changeSize(str) -> str

# NOTE link to sandwich_bridge (kill_cmodule/kill_ccyouku)
etc = {}
etc['flag_inited'] = False
etc['swf_file'] = './ccyk_bridge/player_yknpsv_.swf'
etc['bridge_core'] = './ccyk_bridge/kill_ccyouku_bridge.xml'

def _init_bridge():
    # FIXME maybe BUG here
    if etc['flag_inited']:
        return	# not re-init
    # do init bridge
    _fix_sdw_up()	# fix sdw_up config here
    
    # INFO log here
    log.i('starting sandwich_bridge for kill_cmodule/kill_ccyouku ')
    # FIXME maybe BUG here
    sdw_up.start()

def _fix_sdw_up():
    now_dir = os.path.dirname(__file__)
    swf_file = os.path.join(now_dir, etc['swf_file'])
    bridge_core = os.path.join(now_dir, etc['bridge_core'])
    
    e = sdw_up.etc
    e['bridge_core'] = bridge_core
    e['swf_file'] = swf_file
    # fix done

# FIXME TODO maybe some DEBUG here
def _set_size(raw):
    _init_bridge()
    return sdw_up.set_size(raw)

def _get_size(raw):
    _init_bridge()
    return sdw_up.get_size(raw)

def _change_size(raw):
    _init_bridge()
    return sdw_up.change_size(raw)

# update callbacks here
youku_set_size = _set_size
youku_get_size = _get_size
youku_change_size = _change_size

# end kill_ccyouku_bridge.py


