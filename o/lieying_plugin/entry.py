# -*- coding: utf-8 -*-
# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/lieying_plugin/entry: parse_video lieying_plugin main entry. 
# version 0.1.8.0 test201506291339
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.06. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
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

# import

import json
import re

from . import error
from . import run_sub
from . import tinfo

from . import version as version0

# global vars
PARSE_VIDEO_LIEYING_PLUGIN_NAME = ['parse_video_5lieying_plugin', ' version ']
LIEYING_PLUGIN_PARSE_TYPE = 'parse'

LIEYING_PLUGIN_SUPPORTED_URL_RE = [
    '^http://[a-z]+\.iqiyi\.com/.+\.html', 
]

THIS_PLUGIN_MARK_UUID = 'ebd9ac19-dec6-49bb-b96f-9a127dc4d0c3'
THIS_PLUGIN_SEM_VERSION = '0.5.0'

# base function

# function

def check_support_url(url_to):
    slist = LIEYING_PLUGIN_SUPPORTED_URL_RE
    for i in slist:
        if re.match(i, url_to):
            return False	# support
    # check done
    return True	# not support

def try_to_decode(stdout, stderr):
    try:
        stdout = stdout.decode('utf-8')
    except Exception as e:
        raise error.DecodeUtf8Error(e)
    try:
        stderr = stderr.decode('utf-8')
    except Exception as e:
        raise error.DecodeUtf8Error(e)
    # done
    return stdout, stderr

# get parse_video version
def get_version():
    # run ./parsev --version
    arg = ['--version', '--force-output-utf8']
    stdout, stderr = run_sub.run_pv(arg)
    # get version string
    out = stdout.decode('utf-8')
    line = out.split('\n')
    version = line[0].split(' ')[2]
    # done
    return version

# export functions

def lieying_plugin_get_name():
    # get now version
    ver = get_version()
    static_name = PARSE_VIDEO_LIEYING_PLUGIN_NAME
    this_name = static_name[0] + str(version0.VER) + static_name[1] + ver
    return this_name

def lieying_plugin_get_type():
    return LIEYING_PLUGIN_PARSE_TYPE

def lieying_plugin_get_filter():
    return LIEYING_PLUGIN_SUPPORTED_URL_RE

def lieying_plugin_parse_format(url_to):
    # check if url supported
    if check_support_url(url_to):
        # not support
        raise error.NotSupportURLError('check_re_list', url_to)
        return
    # run parsev to get info
    stdout, stderr = run_sub.run_one_pv(url_to)
    # decode output
    stdout, stderr = try_to_decode(stdout, stderr)
    # use json to parse stdout
    try:
        evinfo = json.loads(stdout)
    except Exception as e:
        # Error msg in stderr
        raise error.MsgError(stdout + '\n' + stderr)
        return
    # try to translate info
    out = tinfo.t2list(evinfo)
    out_text = json.dumps(out)
    # done
    return out_text

def lieying_plugin_parse_url(url_to, format_text):
    # just use parse_some_url
    return lieying_plugin_parse_some_url(url_to, format_text)

# parse_some_url(url_to, format_text, i_min, i_max)
def lieying_plugin_parse_some_url(url_to, format_text, i_min=None, i_max=None):
    # check if url supported
    if check_support_url(url_to):
        # not support
        raise error.NotSupportURLError('check_re_list', url_to)
        return
    # get hd
    hd = tinfo.get_hd_from_format_text(format_text)
    # run parsev to get info
    stdout, stderr = run_sub.run_one_pv(
    				url_to, 
    				hd=hd, 
    				i_min=i_min, 
    				i_max=i_max, 
    				flag_min_parse=True)
    
    # decode output
    stdout, stderr = try_to_decode(stdout, stderr)
    # use json to parse stdout
    try:
        evinfo = json.loads(stdout)
    except Exception as e:
        # Error msg in stderr
        raise error.MsgError(stdout + '\n' + stderr)
        return
    # try to translate info
    out = tinfo.t2one(evinfo, hd)
    out_text = json.dumps(out)
    # done
    return out_text

# parse_format2(), support for vlist
def lieying_plugin_parse_format2(url):
    from ..pvtkgui.vlist import entry as vlist
    
    # output data
    out = {}
    
    # check is vlist
    if vlist.check_is_list_url(url):
        # parse as vlist
        out['data'] = vlist.parse_video_list(url)
        out['type'] = 'list'
        
        # add more info
        out['total'] = -1
        out['total'] = len(out['data'])
        out['more'] = False
    else:	# parse as normal url
        info = lieying_plugin_parse_format(url)
        out['data'] = json.loads(info)
        out['type'] = 'formats'
    
    outt = json.dumps(out)
    # done
    return outt

# get_version
def lieying_plugin_get_version():
    # make version info obj
    info = {}
    
    info['uuid'] = THIS_PLUGIN_MARK_UUID
    info['version'] = THIS_PLUGIN_SEM_VERSION
    
    info['name'] = lieying_plugin_get_name()
    info['type'] = lieying_plugin_get_type()
    info['filter'] = lieying_plugin_get_filter()
    
    # add more info
    info['home'] = 'https://github.com/sceext2/parse_video/tree/output-easy'
    info['author'] = 'sceext <sceext@foxmail.com>'
    info['copyright'] = 'copyright 2015 sceext All rights reserved. '
    info['license'] = 'GNU GPLv3'
    
    # output
    out = json.dumps(info)
    return out

# end entry.py


