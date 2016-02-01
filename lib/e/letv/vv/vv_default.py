# vv_default.py, parse_video/lib/e/letv/vv/

from .... import b, err, conf
from ....b import log
from ... import common

from ..var import var
from ..o import (
    pay_token, 
)

# global data
etc = {}
etc['vv_conf'] = None


# add args to before urls
def add_args(pvinfo, a_idx=''):
    # TODO a_idx support
    # TODO Error process
    # TODO use map_do
    # INFO log
    log.i('adding args for vv ')
    pid = var._['_vid_info']['pid']
    for v in pvinfo['video']:
        if '_data' in v:
            d = v['_data']
            filename = d['filename']
            d['url'] = make_one_url(d['url'], pid, filename, a_idx=a_idx)
    return pvinfo

def make_one_url(raw, pid, filename, a_idx=''):
    # get token info
    tinfo = get_token(pid, filename)
    # TODO use .o. add args code
    # add more args
    out = raw + '&pay=1'
    out += '&uinfo=' + tinfo['uinfo']
    out += '&iscpn=f9051'
    out += '&uuid=' + tinfo['uuid']
    out += '&a_idx=' + a_idx
    out += '&token=' + tinfo['token']
    out += '&uid=' + tinfo['uid']
    return out

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


