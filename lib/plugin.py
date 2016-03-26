# -*- coding: utf-8 -*-
# plugin.py, parse_video/lib/, support lyyc_plugin port_version 0.2.0

from . import err, entry
from .b import log
from . import version

# exports functions

def lyyc_about():
    out = {	# raw output info obj
        'port_version' : '0.2.0', 
        'uuid' : 'cf01a87e-d4b1-4c49-bd87-b21392559cb9', 
        'id' : 'parse_video', 
        'type' : [
            'parse', 
        ], 
        'version' : version.parse_video_version, 
        
        'info' : {
            'name' : 'parse_video', 
            'note' : '负锐视频解析 \n parse_video for lyyc_plugin. ', 
            'author' : 'sceext <sceext@foxmail.com> ', 
            'copyright' : 'copyright 2015-2016 sceext ', 
            'license' : 'GNU GPL v3+ <http://www.gnu.org/licenses/> ', 
            'home' : 'https://github.com/sceext2/parse_video', 
        }, 
        
        'parse' : [
            '^http://www\.le\.com/.+\.html', 
            '^http://www\.mgtv\.com/.+\.html', 
            '^http://[a-z]+\.iqiyi\.com/.+\.html', 
            '^http://tv\.sohu\.com/.+\.shtml', 
            '^http://v\.pptv\.com/.+\.html', 
            '^http://v\.qq\.com/.+', 
            '^http://v\.youku\.com/v_show/id_[A-Za-z0-9]+\.html', 
            
            '^file:///.+\.m3u8$', 
            '^http://.+/letv-uts/.+/ver_.+\.m3u8?', 
        ], 
        
        'pack_version' : version.pack_version, 
    }
    return out

def lyyc_import(lyyc_phost_api):
    version.lyyc_phost_api = lyyc_phost_api

# TODO maybe support
#lyyc_install(upgrade=False)
#lyyc_config(update=False)
#lyyc_new_obj(obj_type='')

def lyyc_parse(url, **kk):
    k = {	# NOTE for lyyc_plugin.lyyc_parse(), port_version 0.2.0
        'hd_min' : None, 
        'hd_max' : None, 
        'i_min' : None, 
        'i_max' : None, 
        'extractor' : '', 	# NOTE set default values
        'method' : '', 
        'debug' : False, 
        'more' : None, 
    }	# update default values
    k.update(kk)
    # set log level
    if k['debug']:
        log.set_log_level('debug')
    else:	# set log level to default
        log.set_log_level()
    # set entry.var
    entry.init()
    entry.var._['hd_min'] = k['hd_min']
    entry.var._['hd_max'] = k['hd_max']
    entry.var._['i_min'] = k['i_min']
    entry.var._['i_max'] = k['i_max']
    entry.var._['more'] = k['more']
    # do parse
    try:
        pvinfo = entry.parse(url, extractor=k['extractor'], method=k['method'])
    except err.PVError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow lib.entry.parse Error')
        raise er from e
    return pvinfo

# end plugin.py


