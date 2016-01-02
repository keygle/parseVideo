# -*- coding: utf-8 -*-
# plugin.py, parse_video/lib/, support lyyc_plugin port_version 0.1.0

# TODO support more functions for lyyc_plugin

from . import err, entry
from .b import log

# exports functions

def lyyc_about():
    out = {	# raw output info obj
        'port_version' : '0.1.0', 
        'type' : 'parse', 
        'uuid' : 'cf01a87e-d4b1-4c49-bd87-b21392559cb9', 
        'version' : '0.5.3.0', 
        'name' : 'parse_video', 
        'note' : 'parse_video for lyyc_plugin. ', 
        
        'parse' : [
            '^http://[a-z]+\.iqiyi\.com/.+\.html', 
            '^http://www\.letv\.com/.+\.html', 
            '^http://www\.hunantv\.com/.+\.html', 
            '^http://tv\.sohu\.com/.+\.shtml', 
            '^http://v\.pptv\.com/.+\.html', 
        ], 
        
        'author' : 'sceext <sceext@foxmail.com> ', 
        'copyright' : 'copyright 2015-2016 sceext ', 
        'license' : 'GNU GPL v3+ <http://www.gnu.org/licenses/> ', 
        'home' : 'https://github.com/sceext2/parse_video', 
    }
    return out

def lyyc_import(lyyc_phost_api):
    pass	# NOTE nothing to do here

# TODO more functions here

def lyyc_parse(url, hd_min=None, hd_max=None, i_min=None, i_max=None, 
        more=None, debug=False):
    # get extractor and method from more
    extractor = ''
    method = ''
    if more != None:
        if 'extractor' in more:
            extractor = more['extractor']
        if 'method' in more:
            method = more['method']
    # set log level
    if debug:
        log.set_log_level('debug')
    else:	# set log level to default
        log.set_log_level()
    # set entry.var
    entry.init()
    entry.var._['hd_min'] = hd_min
    entry.var._['hd_max'] = hd_max
    entry.var._['i_min'] = i_min
    entry.var._['i_max'] = i_max
    entry.var._['more'] = more
    # do parse
    try:
        pvinfo = entry.parse(url, extractor=extractor, method=method)
    except err.PVError:
        raise
    except Exception as e:
        er = err.UnknowError('unknow lib.entry.parse Error')
        raise er from e
    return pvinfo

# end plugin.py


