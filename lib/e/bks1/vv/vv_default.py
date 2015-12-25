# vv_default.py, parse_video/lib/e/bks1/vv/

import json

from .... import b, err, conf
from ....b import log

from .. import var
from ..o import (
    mixer_remote, 
    authentication_remote, 
    member_dispatch_remote, 
)

# global data
etc = {}
etc['vv_conf'] = None	# vv conf json info

def make_first_url(vid_info, set_um=True, set_vv=True):
    config = _load_vv_conf()
    tvid = vid_info['tvid']
    vid = vid_info['vid']
    out = mixer_remote.get_request(tvid, vid, qyid=config['qyid'], puid=config['uid'], flag_set_um=set_um, flag_set_vv=set_vv)
    return out

def add_tokens(pvinfo, vid_info):
    config = _load_vv_conf()
    # get raw_url and make token todo_list
    todo_list = []
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                one = {}
                one['i'] = i
                i += 1
                one['url'] = f['url']
                one['vid_info'] = vid_info
                one['config'] = config
                todo_list.append(one)
    # use map do to do get tokens
    pool_size = var._['pool_size_vv_get_token']
    # INFO log
    log.i('getting ' + str(len(todo_list)) + ' tokens for vv, pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo_list, worker=_get_one_token, pool_size=pool_size)
    # DEBUG log
    log.d('got tokens done ')
    # set back result
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                one = result[i]
                i += 1
                # get needed info
                raw_url = f['url']
                vid = vid_info['vid']
                key = one['data']['t']	# token
                uid = config['uid']
                qyid = config['qyid']
                # update url
                f['url'] = member_dispatch_remote.get_request(raw_url, vid, key, uid=uid, qyid=qyid)
    # update raw_url done
    return pvinfo

def _get_one_token(info):
    raw_url = info['url']
    vid_info = info['vid_info']
    config = info['config']
    i = info['i']
    try:
        out = _do_get_one_token(raw_url, vid_info, config, i)
        return out
    except err.PVError as e:
        er = err.ParseError('load token failed', i)
        raise er from e
    except Exception as e:
        er = err.UnknowError('unknow load token Error', i)
        raise er from e

def _do_get_one_token(raw_url, vid_info, config, index):
    tvid = vid_info['tvid']
    aid = vid_info['aid']
    uid = config['uid']
    device_id = config['qyid']
    
    # get post data
    post_url, post_data = authentication_remote.get_request(raw_url, tvid, aid, uid=uid, device_id=device_id)
    header = {
        'Cookie' : config['cookie'], 
    }
    # DEBUG log here
    log.d(str(index) + ' POST ' + post_url + ' with data ' + str(post_data) + ' ')
    
    raw_result = b.post_form(post_url, header=header, post_data=post_data)
    try:
        text = raw_result.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('decode token blob to text failed')
        er.blob = raw_result
        raise er from e
    # DEBUG log here
    log.d(str(index) + ' got raw token info \"' + text + '\" ')
    try:
        info = json.loads(text)
    except Exception as e:
        er = err.ParseJSONError('parse raw token info text failed', text)
        er.text = text
        raise er from e
    # check token
    ok_code = authentication_remote.OK_CODE
    if info['code'] != ok_code:
        raise err.MethodError('token code \"' + info['code'] + '\" is not ' + ok_code + ' ')
    return info

def _load_vv_conf(reload=False):
    if reload or (etc['vv_conf'] == None):
        return _do_load_vv_conf()
    return etc['vv_conf']

def _do_load_vv_conf():
    try:
        info = b.load_config_json(conf.e_bks1_vv_conf)
    except Exception as e:
        er = err.ConfigError('can not load vv_config file', conf.e_bks1_vv_conf)
        raise er from e
    etc['vv_conf'] = info
    return info

# end vv_default.py


