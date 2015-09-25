# ck_check.py, parse_video/lib/e/bks1/vv
# NOTE get this code from com.qiyi.player.core.model.remote.AuthenticationRemote

import json, time

from .... import b, err
from ....b import log
from .. import var

def make_post_data(play_type = 'main', 	# should be main
        aid = '', 
        cid = '', 
        vid = '', 
        uuid = '', 
        ut = None, 	# can be None
        index = 0):	# segment_index
    '''
    make post data for ck check
    '''
    # s = uint(0 ^ 2.391461978E9).toString()
    # NOTE should be '2391461978', use avmshell to run the code
    s = '2391461978'
    # check ut
    if ut == None:
        ut = int(time.time() * 1e3)
    uts = str(ut)
    utt = str(ut % 1000 * int(uts[0:2]) + (100 + index))
    _ms = ('_').join([aid, cid, vid, uts, utt, s])
    vt = b.md5_hash(_ms)

    # post_data
    pd = {}
    # variables.version = '1.0'
    pd['version'] = '1%2E0'
    # pd['version'] = '1.0'
    pd['platform'] = 'b6c13e26323c537d'
    pd['uuid'] = uuid
    
    pd['ut'] = ut
    pd['vid'] = vid
    pd['cid'] = cid
    pd['aid'] = aid
    pd['utt'] = utt
    pd['v'] = vt
    
    if play_type != None:
        pd['playType'] = play_type
    return pd

def get_ck_token(index=0):
    '''
    post to ck port to check and get info
    return the token
    '''
    # get info from var
    cid = var.DEFAULT_CID
    aid = var._['_vid_info']['aid']
    vid = var._['_vid_info']['vid']
    uuid = var._['_qyid']
    # make post data
    post_data = make_post_data(aid=aid, vid=vid, cid=cid, uuid=uuid, index=index)
    post_str = b.make_post_str(post_data)
    post_blob = post_str.encode('utf-8')
    # get more info for post
    vvc = var._['_vv_conf']
    post_header = vvc['header']
    post_url = var.VIP_AUTH_URL
    # DEBUG log here
    log.d('POST to url \"' + post_url + '\" with str \"' + post_str + '\" ')
    # do post
    blob = b.post(post_url, post_data=post_blob, header=post_header)
    # parse got data
    try:
        raw_text = blob.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('decode ck POST got raw blob data failed')
        er.raw_blob = blob
        raise er from e
    # DEBUG log here
    log.d('got raw json text :: ' + raw_text + ' :: ')
    try:
        info = json.loads(raw_text)
    except Exception as e:
        er = err.ParseJSONError('parse ck got raw json text failed')
        er.raw_text = raw_text
        raise er from e
    # get token
    try:
        # save ck_info
        var._['_ck_info'] = info['data']
        token = info['data']['t']
        return token
    except Exception as e:
        er = err.MethodError('get token from ck port failed')
        er.raw_info = info
        raise er from e

def get_token_list(raw_list_len=0):
    '''
    will get token with index from 0 to raw_list_len - 1
        just get each token one by one, not get many at the same time to prevent more ERRORs
    return got token list
    '''
    # TODO support re-try and sleep before re-try
    # DEBUG log here
    log.d('start get token_list of length ' + str(raw_list_len) + ' ')
    out = []
    for i in range(raw_list_len):
        one = get_ck_token(i)
        out.append(one)
    # DEBUG log here
    log.d('got ' + str(raw_list_len) + ' tokens done. ')
    return out

# end ck_check.py


