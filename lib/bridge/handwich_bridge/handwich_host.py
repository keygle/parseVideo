# handwich_host.py, parse_video/lib/bridge/handwich_bridge/
# TODO support start handwich_server

import json
import urllib.parse

from ... import err, b, conf
from ...b import log

from . import handwich_server

# global config
etc = {}
# TODO support start server here
# FIXME DEBUG here
etc['handwich_server'] = '192.168.222.3:48271'
# debug flag
flag_handwich_debug = False

def _gen_base_url(f=''):
    out = 'http://' + etc['handwich_server'] + '/handwich_bridge/' + f
    return out

def _gen_load_core_url(core, core_path):
    out = _gen_base_url('load_core')
    core_path = urllib.parse.quote(str(core_path))
    out += '?id=' + str(core) + '&path=' + core_path
    return out

def _gen_call_core_url(core, f='about', a=None):
    out = _gen_base_url('call')
    out += '?core=' + str(core) + '&f=' + str(f)
    if a != None:
        text = json.dumps(a)
        text = urllib.parse.quote(text)
        out += '&a=' + text
    return out

def _check_server_version():
    to = _gen_base_url('version')
    # DEBUG log
    log.d('handwich_bridge: check server version \"' + to + '\" ')
    try:
        blob = b.dl_blob(to)
        text = blob.decode('utf-8')
        return text
    except Exception as e:
        # TODO error log here
        return None

def _check_core_about(core):
    to = _gen_call_core_url(core, f='about')
    # DEBUG log
    log.d('handwich_bridge: check bridge_core \"' + to + '\" ')
    raw = b.dl_json(to)
    # check error
    if raw[0] == 'err':
        raise err.ConfigError('handwich_host._check_core_about', to, raw)
    else:
        return raw

def _load_core(core, core_path):
    to = _gen_load_core_url(core, core_path)
    log.d('handwich_bridge: load core \"' + to + '\" ')
    raw = b.dl_json(to)
    if raw[0] == 'err':
        log.e('handwich_bridge: load_core failed, ' + str(raw) + ' ')
        raise err.ConfigError('handwich_host._load_core', core, core_path, raw)
    # OK log
    log.d('handwich_bridge: core loaded, ' + str(raw) + ' ')

# exports functions
def init(core, core_path):
    try:
        _do_init(core, core_path)
    except Exception as e:
        er = err.ConfigError('handwich_bridge', 'handwich_host.init')
        raise er from e

def _do_init(core, core_path):
    # TODO support start handwich_server
    # check server running
    server_version = _check_server_version()
    if server_version == None:
        raise err.ConfigError('handwich_host.init', 'check_server_version')
    # DEBUG log
    log.d('handwich_bridge: server ' + server_version + ' ')
    # check core loaded
    try:
        core_about = _check_core_about(core)
    except Exception as e:	# ignore error
        # do load core
        _load_core(core, core_path)
        # check core loaded again
        core_about = _check_core_about(core)
    # DEBUG log
    log.d('handwich_bridge: core loaded, ' + str(core_about) + ' ')
    # end _do_init

def call(core, f='about', a=[]):
    a = a[:]
    # gen api url
    to = _gen_call_core_url(core, f=f, a=a)
    # DEBUG
    if flag_handwich_debug:
        log.d('handwich_host.call \"' + to + '\" ')
    try:
        raw = b.dl_json(to)
        # DEBUG
        if flag_handwich_debug:
            log.d('handwich_host.call, ret ' + str(raw) + ' ')
    except Exception as e:
        er = err.UnknowError('handwich_bridge.handwich_host.call', 'dl json', core, f, a, to)
        raise er from e
    # check error
    if raw[0] == 'err':
        raise err.UnknowError('handwich_bridge.handwich_host.call', 'return err', core, f, a, raw)
    return raw	# done

# end handwich_host.py


