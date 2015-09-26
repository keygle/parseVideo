# __init__.py, parse_video/lib/e/bks1/vv
# version 0.0.3.0 test201509261713

from .... import b
from .. import var

from . ck_check import get_ck_token, get_token_list

def load_conf():
    '''
    load vv config file
    '''
    # load main config file
    mc = b.load_conf_file(var.CONF_FILE)
    vv_conf_file = mc['vv_conf_file']
    # load vv config file
    vvc = b.load_conf_file(vv_conf_file)
    # save conf info
    var._['_vv_conf'] = vvc
    var._['_qyid'] = vvc['qyid']
    
    return vvc

def gen_token_flag_list(video_info):
    max_len = 0
    for v in video_info:
        l = len(v['file'])
        if l > max_len:
            max_len = l
    # create a long enough flag list and put default flag to False
    out = []
    for i in range(max_len):
        out.append(False)
    # check file url to set flag to True
    for v in video_info:
        for i in range(len(v['file'])):
            f = v['file'][i]
            if f['url']:
                out[i] = True
    return out

# end __init__.py


