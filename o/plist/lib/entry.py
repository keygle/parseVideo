# -*- coding: utf-8 -*-
# entry.py, parse_video/o/plist/lib/

import re
import importlib

from . import err, b, conf, log

# TODO support set extractor (not auto select)
# TODO support output json restruct
# TODO support more method

# plist/lib, entry function
def parse(url):
    # DEBUG log
    log.d('parse URL \"' + url + '\" ')
    try:
        plinfo = _do_parse(url)
    except err.PlistError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow plist.lib Error')
        raise er from e
    return plinfo

def _do_parse(url):
    # auto select extractor
    extractor_id = _get_extractor(url)
    
    extractor = _import_extractor(extractor_id)
    # DEBUG log
    log.d('use extractor \"' + extractor_id + '\" ')
    # do parse
    plinfo = _call_extractor(extractor, url)
    
    out = _add_more_info(plinfo)
    return out

def _get_extractor(url):
    raw_list = conf.URL_TO_EXTRACTOR
    for re_text, extractor_id in raw_list.items():
        if len(re.findall(re_text, url)) > 0:
            return extractor_id
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

def _call_extractor(extractor, url):
    # TODO maybe support set extractor before parse
    # call it
    try:
        plinfo = extractor.parse(url)
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

# end entry.py


