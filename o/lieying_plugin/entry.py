# -*- coding: utf-8 -*-
# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/lieying_plugin/entry: parse_video lieying_plugin main entry. 
# version 0.0.3.0 test201506071139
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

# global vars
PARSE_VIDEO_LIEYING_PLUGIN_NAME = 'parse_video_1_lieying_plugin1'
LIEYING_PLUGIN_PARSE_TYPE = 'parse'
LIEYING_PLUGIN_SUPPORTED_URL_RE = [
    '^http://[a-z]+\.iqiyi\.com/.+\.html', 
]

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

# export functions

def lieying_plugin_get_name():
    return PARSE_VIDEO_LIEYING_PLUGIN_NAME

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
    # check if url supported
    if check_support_url(url_to):
        # not support
        raise error.NotSupportURLError('check_re_list', url_to)
        return
    # get hd
    hd = tinfo.get_hd_from_format_text(format_text)
    # run parsev to get info
    stdout, stderr = run_sub.run_one_pv(url_to, hd=hd)
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

# end entry.py


