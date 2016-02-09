# -*- coding: utf-8 -*-
# entry.py, parse_video/o/plist/lib/

import re
import importlib

from . import err, b, conf, log

# entry data
class Var(object):
    pass
    # end Var class

# plist/lib, entry function
def _parse(url, extractor=None, method=None):
    # DEBUG log
    log.d('parse extractor = \"' + str(extractor) + '\", method = \"' + str(method) + '\", URL \"' + url + '\" ')
    try:
        plinfo = _do_parse(url, extractor=extractor, method=method)
    except err.PlistError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow plist.lib Error')
        raise er from e
    return plinfo

def _do_parse(url, extractor=None, method=None):
    if extractor = None:	# auto select extractor
        extractor = _get_extractor(url)
    extractor_id = b.split_extractor(extractor)[0]
    # get default method
    if method == None:
        method = conf.DEFAULT_METHOD[extractor_id]
    
    e = _import_extractor(extractor_id)
    # DEBUG log
    log.d('use extractor \"' + extractor + '\", method = \"' + method + '\" ')
    # do parse
    plinfo = _call_extractor(e, url, extractor=extractor, method=method)
    
    out = _add_more_info(plinfo)
    return out

def _get_extractor(url):
    raw_list = conf.URL_TO_EXTRACTOR
    for re_text, extractor in raw_list.items():
        if len(re.findall(re_text, url)) > 0:
            return extractor
    # not found
    raise err.NotSupportURLError('no extractor can parse this url', url)

def _import_extractor(extractor_id):
    try:
        to = '..e.' + extractor_id
        e = importlib.import_module(to, __name__)
        return e
    except Exception as e:
        er = err.ConfigError('can not import extractor \"' + extractor_id + '\" ')
        raise er from e

def _call_extractor(e, url, extractor=None, method=None):
    # call it
    try:
        plinfo = e.parse(url, extractor=extractor, method=method)
    except err.PlistError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow extractor Error')
        raise er from e
    return plinfo

def _add_more_info(plinfo):
    # NOTE add mark_uuid and port_version
    plinfo['mark_uuid'] = conf.PLINFO_MARK_UUID
    plinfo['port_version'] = conf.PLINFO_PORT_VERSION
    # add info_source
    plinfo['info_source'] = conf.plist_version
    # add count
    plinfo['count'] = len(plinfo['list'])
    # add last_update
    plinfo['last_update'] = b.print_iso_time()
    # done
    return plinfo

# entry exports
var = Var()
parse = _parse
# end entry.py


