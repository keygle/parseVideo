# -*- coding: utf-8 -*-
# parse_video.py, part for parse_video : a fork from parseVideo. 
# parse_video:bin/parse_video: parse_video main bin file. 
# version 0.2.11.0 test201508102305
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.08. 
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

# supported command line options

# NOTE support --min --max
# NOTE support --min-i --max-i

# NOTE support --http-proxy

# NOTE support --debug
# NOTE support --fix-unicode output option. 
# NOTE support --fix-size option
# NOTE support --set-min-parse
# NOTE support --enable-parse-more-url

# NOTE support --set-flag-v
# NOTE support --force

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

PARSE_VIDEO_VERSION = 'parse_video version 0.3.6.1 test201508102305'

DEBUG_STDOUT_MARK = '<parse_video_debug_stdout_mark>'

etc = {}
etc['flag_debug'] = False

etc['hd_min'] = None
etc['hd_max'] = None
etc['i_min'] = None
etc['i_max'] = None

etc['http_proxy'] = None

etc['flag_fix_size'] = False
etc['flag_fix_unicode'] = False
etc['flag_min_parse'] = False
etc['flag_enable_parse_more_url'] = False

etc['flag_v'] = False
etc['flag_v_force'] = False

# default mode, analyse url
etc['global_mode'] = 'mode_url'
etc['url_to'] = ''	# url to analyse

# functions

def print_stdout(text):
    # check fix_unicode flag
    if etc['flag_fix_unicode']:
        t = text.encode('utf-8')
        sys.stdout.buffer.write(t)
        
        sys.stdout.flush()	# NOTE flush here
    else:	# just print it
        print(text)
    # done

# print functions
def print_version():
    print_stdout(PARSE_VIDEO_VERSION)
    print_free()

def print_free():
    print_stdout('''
    author sceext <sceext@foxmail.com> 2009EisF2015, 2015.07
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
    parsev [OPTIONS] <url>
    parsev --version
    parsev --help
  
Options:
    <url>            URL of the video play page, to be analysed 
                     and get information from. 
    
    --min <hd_min>   set min hd number of video info to get
    --max <hd_max>   set max hd number of video info to get
    
    --min-i <i_min>  set min index of files to parse
    --max-i <i_max>  set max index of files to parse
    
    --debug          output DEBUG information
    
    --http-proxy <http_proxy_string>
                     use the http_proxy to parse
    
    --set-min-parse  parse as less as possible to get fastest speed
    --fix-unicode    output pure ASCII json text
                     used on systems not support unicode well
    --fix-size       parse all possible size, or give url if possible
                     and set the fix_size flag at the same time
    --enable-parse-more-url
                     parse more url of one file if possible
    
    --set-flag-v     reserved option
    --force          force set
    
    --version        show version of parse_video
    --help           show this help information of parse_video
  
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
    
    entry.etc['i_min'] = etc['i_min']
    entry.etc['i_max'] = etc['i_max']
    
    # set lib
    entry.etc['flag_debug'] = etc['flag_debug']
    entry.etc['flag_fix_size'] = etc['flag_fix_size']
    entry.etc['flag_v'] = etc['flag_v']
    entry.etc['flag_v_force'] = etc['flag_v_force']
    entry.etc['flag_min_parse'] = etc['flag_min_parse']
    entry.etc['flag_enable_parse_more_url'] = etc['flag_enable_parse_more_url']
    
    entry.etc['http_proxy'] = etc['http_proxy']
    
    url_to = etc['url_to']
    try:
        evinfo = entry.parse(url_to)
        # just print info as json
        t = json.dumps(evinfo, indent=4, sort_keys=False, ensure_ascii=etc['flag_fix_unicode'])
        
        # check debug
        if etc['flag_debug']:
            print_stdout(DEBUG_STDOUT_MARK)
        
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
        elif one == '--min-i':
            next = rest[0]
            rest = rest[1:]
            etc['i_min'] = int(next)
        elif one == '--max-i':
            next = rest[0]
            rest = rest[1:]
            etc['i_max'] = int(next)
        elif one == '--set-flag-v':
            etc['flag_v'] = True
        elif one == '--set-min-parse':
            etc['flag_min_parse'] = True
        elif one == '--enable-parse-more-url':
            etc['flag_enable_parse_more_url'] = True
        elif one == '--force':
            etc['flag_v_force'] = True
            # TODO set other force flags
        elif one == '--http-proxy':
            next = rest[0]
            rest = rest[1:]
            # NOTE set http_proxy here
            etc['http_proxy'] = str(next)
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


