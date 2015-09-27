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
    log.d('[' + str(index) + '] POST to url \"' + post_url + '\" with str \"' + post_str + '\" ')
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

def get_token_list(flag_list=[]):
    '''
    will get ck token for each item in flag_list
        if the flag is True, will get the token
        if the flag is False, will just skip the token
    just get each token one by one, not get many at the same time to prevent more ERRORs
    return got token list
    '''
    # INFO log here
    log.i('start get token_list of max length ' + str(len(flag_list)) + ' ')
    count_token = 0
    # NOTE limit and config value for auto retry
    auto_retry_count = var._['_vv_conf']['auto_retry_count']
    sleep_time_s = var._['_vv_conf']['sleep_time_s']
    # start get tokens
    out = []
    for i in range(len(flag_list)):
        if flag_list[i]:
            # NOTE support auto retry and sleep before retry
            for j in range(auto_retry_count):
                try:
                    one = get_ck_token(i)
                    break	# get token OK
                except err.NetworkError as e:
                    # WARNING log here
                    log.w('POST to get token failed ' + str(j + 1) + ' ')
                    # check retry
                    if j < (auto_retry_count - 1):
                        # sleep first
                        log.d('sleep ' + str(sleep_time_s) + 's before retry ')
                        time.sleep(sleep_time_s)
                        # just retry
                        continue
                    else:	# no more retry
                        raise
            count_token += 1
        else:
            one = None
        out.append(one)
    # [ OK ] log here
    log.o('got ' + str(count_token) + ' tokens done. ')
    return out

# end ck_check.py


