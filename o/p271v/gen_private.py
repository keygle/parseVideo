#!/usr/bin/env python
# -*- coding: utf-8 -*-
# gen_private.py, part for parse_video : a fork from parseVideo. 
# gen_private: e/p271v: generate private config file for 271v. 
# version 0.1.2.1 test201506281352
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

import re
import os
import sys
import json
import datetime

# global vars
CONFIG_FILE = './gen_conf.json'

etc = {}
etc['conf'] = None	# config obj

etc['cookie_text'] = ''

# function

def get_iso_now():
    raw = datetime.datetime.utcnow().isoformat()
    raw += 'Z'
    return raw

def load_conf():
    # make config file path
    raw_path = os.path.dirname(__file__)
    conf_path = os.path.join(raw_path, CONFIG_FILE)
    conf_path = os.path.normpath(conf_path)
    # read config file
    with open(conf_path) as f:
        content = f.read()
    # parse as json
    conf = json.loads(content)
    # done
    etc['conf'] = conf

def get_args():
    args = sys.argv[1:]
    etc['cookie_text'] = args[0]

def parse_cookie_string(text):
    clist = text.split('; ')
    cinfo = {}
    for p in clist:
        raw = p.split('=')
        cinfo[raw[0]] = raw[1]
    # done
    return cinfo

def gen_cookie_string(clist):
    slist = []
    for c in clist:
        slist += [c + '=' + clist[c]]
    t = ('; ').join(slist)
    # done
    return t

def select_cookie(raw_list):
    # get config
    cookie_list = etc['conf']['cookie_list']
    # make first cookie list
    clist = {}
    for l in cookie_list:
        clist[l] = raw_list[l]
    # done
    return clist

def get_cookie_info(raw_list):
    ci_name = etc['conf']['cookie_info']	# cookie info name
    qyid_c = ci_name['qyid']
    uid_c = ci_name['uid']
    
    info = {}
    info['qyid'] = raw_list[qyid_c]
    info['uid'] = raw_list[uid_c]
    # done
    return info

def gen_private():
    # FIXME debug here
    # print('DEBUG: got cookie_text \"' + etc['cookie_text'] + '\"')
    
    # load config file
    print('INFO: load config file \"' + CONFIG_FILE + '\"')
    load_conf()
    
    print('INFO: parse cookie text')
    # parse url and cookie
    cookie_list = parse_cookie_string(etc['cookie_text'])
    
    # get cookie info
    cookie_info = get_cookie_info(cookie_list)
    
    print('INFO: make conf info')
    # make conf obj
    conf = etc['conf']['default_conf'].copy()	# load default conf obj
    # update info
    conf['uid'] = cookie_info['uid']
    conf['qyid'] = cookie_info['qyid']
    
    print('INFO: gen cookie')
    # set cookie
    cookie_string = gen_cookie_string(select_cookie(cookie_list))
    conf['header']['Cookie'] = cookie_string
    
    # add last_update
    conf['_last_update'] = get_iso_now()
    
    # write private conf file
    private_file = etc['conf']['private_file']
    
    print('INFO: write private file \"' + private_file + '\"')
    to_text = json.dumps(conf, indent=4, sort_keys=True)
    with open(private_file, 'w') as f:
        f.write(to_text)
    
    # done
    print('[ OK ] done')

def main():
    get_args()
    gen_private()

# start from main
if __name__ == '__main__':
    main()

# end gen_private.py



