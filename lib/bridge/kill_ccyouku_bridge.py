# kill_ccyouku_bridge.py, parse_video/lib/bridge/, for extractor youku
# package com.youku.utils.PlayListUtil
#
# NOTE use handwich_bridge here

import os

from .. import err, b, conf
from ..b import log

from . import ccyk_bridge
from . import flash_bridge

# NOTE set bridge callback function here
youku_set_size = None		# setSize(str) -> str
youku_get_size = None		# getSize(str) -> str
youku_change_size = None	# changeSize(str) -> str

# NOTE link to handwich_bridge (kill_cmodule/handwich_bridge)
etc = {}
etc['_flag_init_ed'] = False
etc['core'] = 'kill_ccyouku'
# core .swf for handwich_bridge
#etc['bridge_core'] = './ccyk_bridge/kill_ccyouku_c.swf'
# FIXME DEBUG here
etc['bridge_core'] = 'c:/users/a201508w/sandwich_bridge/kill_ccyouku.swf'


# TODO Error process

def _init_bridge():
    if etc['_flag_init_ed']:
        return	# not re-init
    _do_init_bridge()
    # NOTE init done, mark it
    etc['_flag_init_ed'] = True

def _do_init_bridge():
    # TODO support make core path
    flash_bridge.init_handwich_bridge(etc['core'], etc['bridge_core'])

def _do_call(f, a):
    _init_bridge()
    try:	# NOTE error process here
        raw = flash_bridge.handwich_call(etc['core'], f=f, a=[a])
    except Exception as e:
        er = err.UnknowError('kill_ccyouku_bridge', 'call handwich_bridge', f, a)
        raise er from e
    result = raw[1]	# raw: ['ret', result]
    return result
    # TODO maybe some DEBUG here

# exports functions
def _set_size(raw):
    return _do_call('set_size', raw)

def _get_size(raw):
    return _do_call('get_size', raw)

def _change_size(raw):
    return _do_call('change_size', raw)

# update callbacks here
youku_set_size = _set_size
youku_get_size = _get_size
youku_change_size = _change_size

# end kill_ccyouku_bridge.py


