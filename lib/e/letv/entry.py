# -*- coding: utf-8 -*-
# entry.py, parse_video/lib/e/letv/, entry for extractor letv

from ... import err
from ...b import log

from . import var
from . import method_pc_flash_gate

def init():
    var.push()
    var._ = var.init()
    var._var_init_flag = True

def parse(raw_url, raw_arg='', raw_method=''):
    if not var._var_init_flag:
        init()
    var._['raw_arg'] = raw_arg
    var._['raw_method'] = raw_method
    var._['_raw_url'] = raw_url
    # DEBUG log
    log.d('parse, raw_url = \"' + raw_url + '\", raw_arg = \"' + raw_arg + '\", raw_method = \"' + raw_method + '\" ')
    try:
        pvinfo = _do_parse(raw_method)
    except err.PVError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow extractor Error')
        raise er from e
    finally:
        var.pop()
        var._var_init_flag = False
    return pvinfo

def _do_parse(raw_method):
    if ';' in raw_method:
        method, method_arg_text = raw_method.split(';', 1)
    else:
        method = raw_method
        method_arg_text = None
    # check method name
    if method == 'pc_flash_gate':
        # DEBUG log
        log.d('use method \"' + method + '\" and method_args \"' + str(method_arg_text) + '\" ')
        pvinfo = method_pc_flash_gate.parse(method_arg_text)
    else:
        raise err.ConfigError('no method \"' + method + '\" ')
    # add more info
    pvinfo['extractor_name'] = var.EXTRACTOR_NAME
    pvinfo['extractor'] = var._['raw_arg']
    pvinfo['method'] = var._['raw_method']
    
    pvinfo['info']['site'] = var.SITE
    pvinfo['info']['site_name'] = var.SITE_NAME
    pvinfo['info']['url'] = var._['_raw_url']
    
    return pvinfo

# end entry.py


