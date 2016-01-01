# -*- coding: utf-8 -*-
# entry.py, parse_video/lib/, entry for parse_video.lib
#
#    parse_video : get video info from some web sites. 
#    Copyright (C) 2015-2016 sceext <sceext@foxmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re
import math
import datetime
from collections import OrderedDict
import importlib

from . import err, b
from .b import log

from . import var, conf

# init var data
def init():
    var.push()
    var._ = var.init()
    var._var_init_flag = True

# parse_video.lib parse entry function, return lyyc_parsev struct
def parse(url, extractor='', method=''):
    if not var._var_init_flag:
        init()
    # DEBUG log here
    log.d('parse, url = \"' + url + '\", extractor = \"' + extractor + '\", method = \"' + method + '\" ')
    try:
        pvinfo = _do_parse(url, raw_extractor=extractor, raw_method=method)
    except err.PVError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow parse_video.lib Error')
        raise er from e
    finally:	# clean var data
        var.pop()
        var._var_init_flag = False
    return pvinfo

def _do_parse(raw_url, raw_extractor='', raw_method=''):
    # get extractor_id
    if raw_extractor == '':
        raw_extractor = _url_to_extractor(raw_url)
    extractor_id = b.split_raw_extractor(raw_extractor)[0]
    var._['_extractor_id'] = extractor_id
    # import extractor
    e = _import_extractor(extractor_id)
    # check default method
    if raw_method == '':
        raw_method = conf.DEFAULT_METHOD[extractor_id]
    # DEBUG log
    log.d('use extractor \"' + extractor_id + '\", raw_extractor = \"' + raw_extractor + '\" ')
    # call extractor to parse
    pvinfo = _call_extractor_parse(e, raw_url, raw_arg=raw_extractor, raw_method=raw_method)
    
    # add more data and info to pvinfo struct data
    out = _add_more_pvinfo(pvinfo)
    # check restruct
    if not var._['flag_no_restruct']:
        out = _restruct_pvinfo(out)
    return out

# NOTE get first useable extractor
def _url_to_extractor(raw_url):
    raw_list = conf.URL_TO_EXTRACTOR
    for re_text, extractor_id in raw_list.items():
        if len(re.findall(re_text, raw_url)) > 0:
            return extractor_id
    # not found
    raise err.NotSupportURLError('no extractor can parse this url', raw_url)

def _import_extractor(extractor_id):
    try:
        to = '..e.' + extractor_id + '.entry'
        e = importlib.import_module(to, __name__)
        return e
    except Exception as e:
        er = err.ConfigError('can not import extractor \"' + extractor_id + '\" ')
        raise er from e

def _call_extractor_parse(extractor, raw_url, raw_arg='', raw_method=''):
    # set extractor data
    extractor.init()
    set_list = [
        'hd_min', 
        'hd_max', 
        'i_min', 
        'i_max', 
        'more', 
    ]
    for key in set_list:
        extractor.var._[key] = var._[key]
    # call it
    try:
        pvinfo = extractor.parse(raw_url, raw_arg=raw_arg, raw_method=raw_method)
    except err.PVError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow extractor Error', var._['_extractor_id'])
        raise er from e
    return pvinfo

def _add_more_pvinfo(pvinfo, add_mark_uuid=False):
    out = pvinfo
    # add main info
    if add_mark_uuid:
        out['mark_uuid'] = var.PVINFO_MARK_UUID
    out['port_version'] = var.PVINFO_PORT_VERSION
    
    out['info_source'] = var.PVINFO_INFO_SOURCE
    # add video quality
    for v in out['video']:
        hd = math.floor(v['hd'])
        q = var.HD_TO_QUALITY.get(hd, '')
        # keep old quality
        if 'quality' in v:
            v['quality'] = q + '-' + v['quality']
        else:
            v['quality'] = q
    # add last_update
    out['last_update'] = _gen_last_update()
    return out

def _gen_last_update():
    now = datetime.datetime.today().utcnow().isoformat()
    last_update = now + 'Z'
    return last_update

def _restruct_pvinfo(pvinfo):
    return _do_restruct_pvinfo(pvinfo)

# base restruct function
def _restruct_key(old, key_list=[], rest_sort_reverse=False):
    '''
    restruct a dict to OrderedDict
    order is in key_list
    
    rest keys is keys in old but not in key_list
    rest keys is sort by rest_sort_reverse
    if rest_sort_reverse == None, rest keys will not be sort
    '''
    raw = old.copy()	# not modify old dict
    out = OrderedDict()
    for key in key_list:
        if key in raw:	# ignore not exist keys
            out[key] = raw.pop(key)
    # get rest key list and sort keys by key name
    rest_key = [i for i in raw]
    if rest_sort_reverse != None:
        rest_key.sort(reverse=rest_sort_reverse)
    # add rest keys
    for key in rest_key:
        out[key] = raw.pop(key)
    return out

# main restruct function
def _do_restruct_pvinfo(pvinfo):
    # key orders list
    pvinfo_list = [	# pvinfo
        'mark_uuid', 
        'port_version', 
        'error', 
        'info_source', 
        'extractor', 
        'extractor_name', 
        'method', 
        'info', 
        'video', 
        'last_update', 
    ]
    info_list = [	# pvinfo.info
        'title', 
        'title_sub', 
        'title_short', 
        'title_no', 
        'site', 
        'site_name', 
        'url', 
    ]
    video_list = [	# pvinfo.video[]
        'hd', 
        'quality', 
        'size_px', 
        'size_byte', 
        'time_s', 
        'format', 
        'count', 
        'file', 
    ]
    file_list = [	# pvinfo.video[].file[]
        'type', 
        'size', 
        'time_s', 
        'url', 
        'header', 
        'expire', 
    ]
    # restruct pvinfo
    out = _restruct_key(pvinfo, pvinfo_list)
    out['info'] = _restruct_key(out['info'], info_list)	# restruct info
    for i in range(len(out['video'])):	# restruct videos
        out['video'][i] = _restruct_key(out['video'][i], video_list)
        v = out['video'][i]
        for j in range(len(v['file'])):	# restruct files
            v['file'][j] = _restruct_key(v['file'][j], file_list)
    # sort videos by hd
    out['video'].sort(key=lambda x:x['hd'], reverse=True)
    return out	# restruct pvinfo done

# end entry.py


