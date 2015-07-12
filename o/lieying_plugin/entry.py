# -*- coding: utf-8 -*-
# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/lieying_plugin/entry: parse_video lieying_plugin main entry. 
# version 0.1.26.0 test201507122115
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.07. 
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

from ..tool import s1

from ..pvtkgui.vlist import entry as vlist

# global vars

# for lieying_plugin port version 0.2.0-test.3

LIEYING_PLUGIN_PORT_VERSION = '0.2.0-test.3'
LIEYING_PLUGIN_TYPE = 'parse'
LIEYING_PLUGIN_UUID = 'ebd9ac19-dec6-49bb-b96f-9a127dc4d0c3'

THIS_PLUGIN_SEM_VERSION = '0.13.0'

LIEYING_PLUGIN_FILTER = [
    '^http://[a-z]+\.' + s1.get_s1()[0] + '\.com/.+\.html', 
]

PARSE_VIDEO_LIEYING_PLUGIN_NAME = [
    'parse_video_' + '9' + 'lieying_plugin', 
    ' (plugin version ', 
    ', kernel version ', 
    ') license ', 
    ' ', 
]

THIS_LICENSE = 'GNU GPLv3+'
THIS_AUTHOR = 'sceext <sceext@foxmail.com>'
THIS_COPYRIGHT = 'copyright 2015 sceext'
THIS_HOME = 'https://github.com/sceext2/parse_video/tree/output-easy'
THIS_NOTE = 'A parse plugin for lieying with parse support of parse_video. '

# base function

# function

def check_support_url(url_to):
    slist = LIEYING_PLUGIN_FILTER
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
def get_parse_video_version():
    # run ./parsev --version
    arg = ['--version', '--force-output-utf8']
    stdout, stderr = run_sub.run_pv(arg)
    # get version string
    out = stdout.decode('utf-8')
    line = out.split('\n')
    version = line[0].split(' ')[2]
    # done
    return version

# make plugin name string
def make_plugin_name():
    
    # get parse_video version
    ver = get_parse_video_version()
    
    static_name = PARSE_VIDEO_LIEYING_PLUGIN_NAME
    
    this_name = ''
    this_name += static_name[0] + str(version0.VER) 
    this_name += static_name[1] + THIS_PLUGIN_SEM_VERSION 
    this_name += static_name[2] + ver 
    this_name += static_name[3] + THIS_LICENSE 
    this_name += static_name[4]
    
    return this_name

# parse one video
def parse_one(url):
    # run parsev to get info
    stdout, stderr = run_sub.run_one_pv(url)
    
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
    
    # done
    return out

# parse more video
def parse_more(url):
    
    # output data
    out = {}
    
    vlist_info = vlist.parse_video_list(url)
    out['data'] = vlist_info['list']
    out['type'] = 'list'
    
    # add album_name title, and add site_name
    out['title'] = vlist_info['title'] + '_' + vlist_info['site_name']
    
    # make tinfo
    ti = {}
    ti['title'] = ''
    ti['title_sub'] = ''
    ti['title_no'] = -1
    ti['site_name'] = vlist_info['site_name']
    
    # add name
    for i in range(len(out['data'])):
        one = out['data'][i]
        ti['title'] = vlist_info['title'] + one['no']
        ti['title_sub'] = one['title']
        ti['title_no'] = i + 1
        ti['title_short'] = ''
        ti['quality'] = ''
        
        fname, main_name = tinfo.make_title(ti)
        one['name'] = main_name
    # process vlist, add sub_title
    for one in out['data']:
        one['no'] += '_' + one['title']
        
        # NOTE fix one['title'] to subtitle
        one['subtitle'] = one['title']
        one.pop('title')
    
    # add more info
    out['total'] = -1
    out['total'] = len(out['data'])
    out['more'] = False
    
    # done
    return out


# export functions

# GetVersion()
def lieying_plugin_get_version():
    out = {}	# output info
    
    out['port_version'] = LIEYING_PLUGIN_PORT_VERSION
    out['type'] = LIEYING_PLUGIN_TYPE
    out['uuid'] = LIEYING_PLUGIN_UUID
    out['version'] = THIS_PLUGIN_SEM_VERSION
    out['name'] = make_plugin_name()
    
    out['filter'] = LIEYING_PLUGIN_FILTER
    
    out['author'] = THIS_AUTHOR
    out['copyright'] = THIS_COPYRIGHT
    out['license'] = THIS_LICENSE
    out['home'] = THIS_HOME
    out['note'] = THIS_NOTE
    
    text = json.dumps(out)
    return text

# StartConfig()
def lieying_plugin_start_config():
    raise Exception('parse_video_lieying_plugin: ERROR: not support config now ! ')

# Parse()
def lieying_plugin_parse(input_text):
    # check if url supported
    if check_support_url(input_text):
        # not support
        raise error.NotSupportURLError('check_re_list', input_text)
        return
    
    # check for parse_one and parse_more
    
    # check is vlist
    if vlist.check_is_list_url(input_text):
        out = parse_more(input_text)
    else:
        out = parse_one(input_text)
    
    # done
    text = json.dumps(out)
    return text

# ParseURL()
def lieying_plugin_parse_url(url, label, i_min=None, i_max=None):
    # check if url supported
    if check_support_url(url):
        # not support
        raise error.NotSupportURLError('check_re_list', url)
        return
    # get hd
    hd = tinfo.get_hd_from_format_text(label)
    # run parsev to get info
    stdout, stderr = run_sub.run_one_pv(
    				url, 
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
    
    text = json.dumps(out)
    # done
    return text

# end entry.py


