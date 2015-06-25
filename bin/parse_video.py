# -*- coding: utf-8 -*-
# parse_video.py, part for parse_video : a fork from parseVideo. 
# parse_video:bin/parse_video: parse_video main bin file. 
# version 0.1.29.0 test201506251705
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

# NOTE support --max --min --debug command line options. 
# NOTE support --fix-unicode output option. 
# NOTE support --fix-size option

# import

import sys
import json

from . import error_zh_cn

# NOTE should be set
entry = None
error = None

# set_import
def set_import(entry0, error0):
    global entry
    global error
    entry = entry0
    error = error0

# global config obj

PARSE_VIDEO_VERSION = 'parse_video version 0.2.10.0 test201506251705'

etc = {}
etc['flag_debug'] = False
etc['flag_fix_size'] = False
etc['flag_fix_unicode'] = False
etc['hd_min'] = None
etc['hd_max'] = None
etc['flag_v'] = False

# default mode, analyse url
etc['global_mode'] = 'mode_url'
etc['url_to'] = ''	# url to analyse

# functions

def print_stdout(text):
    # check fix_unicode flag
    if etc['flag_fix_unicode']:
        t = text.encode('utf-8')
        sys.stdout.buffer.write(t)
    else:	# just print it
        print(text)
    # done

# print functions
def print_version():
    print_stdout(PARSE_VIDEO_VERSION)
    print_free()

def print_free():
    print_stdout('''
    author sceext <sceext@foxmail.com> 2009EisF2015, 2015.05
 copyright 2015 sceext

 This is FREE SOFTWARE, released under GNU GPLv3+ 
 please see README.md and LICENSE for more information. 

    parse_video : a fork from parseVideo. 
    Copyright (C) 2015 sceext <sceext@foxmail.com> 

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
''')

def print_help():
    print_stdout('parse_video: HELP')
    print_stdout('''
Usage:
    evp [OPTIONS] <url>
    evp --version
    evp --help
Options:
    <url>           URL of the video play page, to be analysed 
                    and get information from. 
    
    --min <hd_min>  set min hd number of video info to get
    --max <hd_max>  set max hd number of video info to get
    
    --debug         output DEBUG information
    --fix-unicode   output pure ASCII json text
                    used on systems not support unicode well
    
    --version       show version of evparse
    --help          show this help information of evparse
  
  More help info please see <https://github.com/sceext2/parse_video> 
''')

def print_help_notice():
    print_stdout('parse_video: ERROR: command line format error. Please try \"' + sys.argv[0] + ' --help\" ')
    return 1

# start parse
def start_parse():
    # set parse
    if etc['hd_min'] != None:
        entry.etc['hd_min'] = etc['hd_min']
    if etc['hd_max'] != None:
        entry.etc['hd_max'] = etc['hd_max']
    # set lib
    entry.etc['flag_debug'] = etc['flag_debug']
    entry.etc['flag_fix_size'] = etc['flag_fix_size']
    entry.etc['flag_v'] = etc['flag_v']
    
    url_to = etc['url_to']
    try:
        evinfo = entry.parse(url_to)
        # just print info as json
        t = json.dumps(evinfo, indent=4, sort_keys=False, ensure_ascii=etc['flag_fix_unicode'])
        # just print it
        print_stdout(t)
    except error.NotSupportURLError as err:
        # check args length
        if len(err.args) == 2:
            msg, url = err.args
            print_stdout('parse_video: ' + error_zh_cn.ERR_TEXT_NOT_SUPPORT_URL + ' \"' + url + '\"')
        # check get vid error
        if len(err.args) == 3:
            url = err.args[1]
            # check error msg
            err_msg = err.args[2]
            if err_msg == 'get_vid':
                err_msg = error_zh_cn.ERR_TEXT_GET_VID
            elif err_msg == 'may be a VIP video':
                err_msg = error_zh_cn.ERR_TEXT_MAY_BE_VIP
            elif err_msg == 'load_page':
                err_msg = error_zh_cn.ERR_TEXT_LOAD_PAGE
            # just print it
            print_stdout('parse_video: ' + error_zh_cn.ERR_TEXT_NOT_SUPPORT_URL + ' (' + err_msg + ') \"' + url + '\"')
        return 2
    # done

# get args
def get_args():
    # get args
    args = sys.argv[1:]
    # check args length
    if len(args) < 1:
        etc['global_mode'] = 'mode_help_notice'
        return
    # process each arg
    rest = args
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        if one == '--help':
            etc['global_mode'] = 'mode_help'
        elif one == '--version':
            etc['global_mode'] = 'mode_version'
        elif one == '':
            etc['global_mode'] = 'mode_help_notice'
        elif one == '--debug':
            etc['flag_debug'] = True
        elif one == '--fix-unicode':
            etc['flag_fix_unicode'] = True
        elif one == '--fix-size':
            etc['flag_fix_size'] = True
        elif one == '--min':	# next arg should be hd_min
            next = rest[0]
            rest = rest[1:]
            etc['hd_min'] = int(next)
        elif one == '--max':	# next arg should be hd_max
            next = rest[0]
            rest = rest[1:]
            etc['hd_max'] = int(next)
        elif one == '--set-flag-v':
            etc['flag_v'] = True
        else:	# should be url_to
            etc['url_to'] = one
    # done

# main function
def main():
    # get args
    get_args()
    # check mode
    mode_list = {}
    mode_list['mode_url'] = start_parse
    mode_list['mode_version'] = print_version
    mode_list['mode_help'] = print_help
    mode_list['mode_help_notice'] = print_help_notice
    # get mode entry
    mode = etc['global_mode']
    mode_entry = mode_list[mode]
    # just do it
    return mode_entry()
    # done

# end parse_video.py


