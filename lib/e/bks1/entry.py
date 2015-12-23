# -*- coding: utf-8 -*-
# entry.py, parse_video/lib/e/bks1/, entry for extractor bks1

from ... import err
from ...b import log

from . import var, conf
from . import method_pc_flash_gate

# init var data
def init():
    var.push()
    var._ = var.init(arg=raw_arg, method=raw_method)
    var._var_init_flag = True

# extractor parse entry function, return lyyc_parsev struct
def parse(raw_url, raw_arg='', raw_method=''):
    if not var._var_init_flag:
        init()
    # set var data
    var._['_raw_url'] raw_url
    # DEBUG log here
    log.d('parse, raw_url = \"' + raw_url + '\", raw_arg = \"' + raw_arg + '\", raw_method = \"' + raw_method + '\" ')
    try:
        pvinfo = _do_parse(raw_method)
    except err.PVError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow extractor Error')
        raise er from e
    finally:
        var.pop()	# clean var data
        var._var_init_flag = False
    return pvinfo

def _do_parse(raw_method):
    # split method name and method args
    if ';' in raw_method:
        method, method_arg_text = raw_method.split(';', 1)
    else:
        method = raw_method
        method_arg_text = None
    # check method name
    if method == 'pc_flash_gate':
        # DEBUG log here
        log.d('use method \"' + method + '\" and method_args \"' + str(method_arg_text) + '\" ')
        pvinfo = method_pc_flash_gate.parse(method_arg_text)
    else:
        raise err.ConfigError('no method \"' + method + '\" ')
    # add more info to pvinfo
    pvinfo['extractor_name'] = var.EXTRACTOR_NAME
    # NOTE use raw extractor args
    pvinfo['extractor'] = raw_arg
    pvinfo['method'] = raw_method
    
    pvinfo['info']['site'] = var.SITE
    pvinfo['info']['site_name'] = var.SITE_NAME
    pvinfo['info']['url'] = raw_url
    
    return pvinfo

# end entry.py


