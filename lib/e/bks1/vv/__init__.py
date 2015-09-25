# __init__.py, parse_video/lib/e/bks1/vv
# version 0.0.2.0 test201509251733

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

# end __init__.py


