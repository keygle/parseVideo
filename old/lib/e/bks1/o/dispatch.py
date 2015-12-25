# dispatch.py, parse_video/lib/e/bks1/o
# NOTE get this code from <unknow>

import random

from .... import b, err
from .. import var

from . import key

def get_server_time():
    time_url = var.FIRST_DISPATCH_URL + '?tn=' + str(random.random())
    info = b.dl_json(time_url)
    try:
        server_time = info['t']
        return server_time
    except Exception as e:
        er = err.MethodError('get server_time failed')
        er.raw_info = info
        raise er from e

def get_dispatch_key(server_time, this_link):
    # get file id
    file_id = this_link.rsplit('/', 1)[-1].split('.', 1)[0]
    dispatch_key = key.getDispatchKey(server_time, file_id)
    return dispatch_key

def get_one_final_url(before_final_url):
    info = b.dl_json(before_final_url)
    try:
        final_url = info['l']
        return final_url
    except Exception as e:
        er = err.MethodError('get final_url from before_final_url failed', before_final_url)
        er.raw_info = info
        raise er from e

def get_dispatch_key_list(raw_link_list, server_time=None):
    if server_time == None:
        server_time = get_server_time()
    out = []
    for l in raw_link_list:
        key = get_dispatch_key(server_time, l)
        out.append(key)
    return out

# gen before_final_url list
def make_before_urls(raw_part_url_list, token_list=None, server_time=None):
    # NOTE part_url in raw_list has already been decoded by getVrsEncodeCode()
    if not var._['flag_v']:	# normal F video
        # get dispatch_key list
        dispatch_keys = get_dispatch_key_list(raw_part_url_list, server_time=server_time)
        # process du here
        du1, du2 = var._['_du'].rsplit('/', 1)
        # make before_final_url list
        out = []
        for i in range(len(raw_part_url_list)):
            raw = raw_part_url_list[i]
            if not raw:	# check to skip not needed urls
                out.append('')
                continue
            key = dispatch_keys[i]
            one = du1 + '/' + key + '/' + du2 + raw
            # NOTE there is no need to add many args to before_final_url
            out.append(one)
        return out
    else:	# if set flag_v, should give token_list
        du = var._['_du']
        ck_info = var._['_ck_info']
        vid = var._['_vid_info']['vid']
        qyid = var._['_qyid']
        qypid = var._['_vid_info']['tvid'] + '_11'
        # NOTE when got here, everything is ready, just gen before_final_url
        out = []
        for i in range(len(raw_part_url_list)):
            raw = raw_part_url_list[i]
            if not raw:	# check to skip not needed urls
                out.append('')
                continue
            token = token_list[i]
            url = du + raw.replace('.flv', '.hml', 1)
            # add more args
            url += '?t=' + token
            url += '&cid=' + ck_info['cid'] + '&vid=' + vid
            url += '&QY00001=' + ck_info['u']
            url += '&qyid=' + qyid + '&qypid=' + qypid
            # TODO not add ran args, should be OK
            # url += '&ran=' + str(more['time_now'])
            out.append(url)
        return out

# end dispatch.py


