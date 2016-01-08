# vv_default.py, parse_video/lib/e/letv/vv/

from .... import b, err, conf
from ....b import log
from ... import common

from .. import var
from ..o import (
    pay_token, 
)

# global data
etc = {}
etc['vv_conf'] = None


# add args to before urls
def add_args(pvinfo):
    # TODO use map_do
    # INFO log
    log.i('adding args for vv ')
    for v in pvinfo['video']:
        if '_data' in v:
            v['_data'] = _add_one_arg(v['_data'])
    return pvinfo

# TODO a_idx support
def _add_one_arg(data, a_idx=''):
    filename = data['filename']
    pid = var._['_vid_info']['pid']
    # get token info
    tinfo = get_token(pid, filename)
    # TODO use .o. add args code
    # add more args
    raw = data['url']
    raw += '&pay=1'
    raw += '&uinfo=' + tinfo['uinfo']
    raw += '&iscpn=f9051'
    raw += '&uuid=' + tinfo['uuid']
    raw += '&a_idx=' + a_idx
    raw += '&token=' + tinfo['token']
    raw += '&uid=' + tinfo['uid']
    data['url'] = raw	# update url
    return data

def get_token(pid, filepath):
    info = _load_vv_conf()
    raw_url = pay_token.gen_url(pid, info['uid'], filepath, lc=info['uuid'])
    # NOTE DEBUG log
    log.d('got token URL \"' + raw_url + '\" ')
    header = {	# add cookie
        'Cookie' : info['cookie'], 
    }
    raw = b.dl_json(raw_url, header=header)
    # TODO check status == 1
    # get token info from json text
    out = {}
    out['token'] = raw['token']
    out['uinfo'] = raw['uinfo']
    out['uuid'] = info['uuid']
    out['uid'] = info['uid']
    return out

# load config file
def _load_vv_conf(reload=False):
    if reload or (etc['vv_conf'] == None):
        etc['vv_conf'] = _do_load_vv_conf()
    return etc['vv_conf']

def _do_load_vv_conf():
    try:
        info = b.load_config_json(conf.e_letv_vv_conf)
    except Exception as e:
        er = err.ConfigError('can not load vv_conf file', conf.e_letv_vv_conf)
        raise er from e
    return info

# end vv_default.py


