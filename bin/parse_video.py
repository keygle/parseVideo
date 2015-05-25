# -*- coding: utf-8 -*-
# parse_video.py, part for parse_video : a fork from parseVideo. 
# parse_video:bin/parse_video: parse_video main bin file. 
# version 0.1.8.0 test201505251519
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.05. 
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

# import

import sys
import json

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

PARSE_VIDEO_VERSION = 'parse_video version 0.2.2.0 test201505251519'

etc = {}
etc['flag_debug'] = False
etc['flag_fix_unicode'] = False
etc['hd_min'] = None
etc['hd_max'] = None

# default mode, analyse url
etc['global_mode'] = 'mode_url'
etc['url_to'] = ''	# url to analyse

# functions

# print functions
def print_version():
    print(PARSE_VIDEO_VERSION)
    print_free()

def print_free():
    print('''
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
    print('parse_video: HELP')
    print('''
Usage:
    evp [OPTIONS] <url>
    evp --version
    evp --help
Options:
    <url>           URL of the video play page, to be analysed 
                    and get information from. 
    
    --min <hd_min>  set min hd number of video info to get
    --max <hd_max>  set max hd number of video info to get
    
    --version       show version of evparse
    --help          show this help information of evparse
  
  More help info please see <https://github.com/sceext2/parse_video> 
''')

def print_help_notice():
    print('parse_video: ERROR: command line format error. Please try \"' + sys.argv[0] + ' --help\" ')
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
    url_to = etc['url_to']
    try:
        evinfo = entry.parse(url_to)
        # just print info as json
        t = json.dumps(evinfo, indent=4, sort_keys=False, ensure_ascii=etc['flag_fix_unicode'])
        print(t)
    except error.NotSupportURLError as err:
        msg, url = err.args
        print('parse_video: ERROR: not support this url \"' + url + '\"')
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
        elif one == '--min':	# next arg should be hd_min
            next = rest[0]
            rest = rest[1:]
            etc['hd_min'] = int(next)
        elif one == '--max':	# next arg should be hd_max
            next = rest[0]
            rest = rest[1:]
            etc['hd_max'] = int(next)
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


