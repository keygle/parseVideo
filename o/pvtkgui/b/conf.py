# conf.py, part for parse_video : a fork from parseVideo. 
# conf: o/pvtkgui/conf: parse_video Tk GUI, config file support. 
# version 0.1.3.0 test201506231606
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
import os

from . import conf_default as confd

# global vars
conf = {}	# main conf obj
conf['hd'] = 2
conf['xunlei_dl_path'] = ''
conf['ui_type'] = ''
conf['flag_select_each'] = False

support_ui_type = [
    'full_ui', 
    'simple_ui', 
]

# functions

def load_config(conf_file):
    # try to read config file
    t = ''
    try:
        with open(conf_file, 'r') as f:
            t = f.read()
    except Exception:
        # DEBUG info
        print('pvtkgui: conf: read config file \"' + conf_file + '\" failed')
    # parse as json
    try:
        info = json.loads(t)
    except Exception:
        # DEBUG info
        print('pvtkgui: conf: parse config file as json failed')
        info = confd.conf
    # check and set config info
    check_config_file(info)
    # load conf done

# write config file
def write_config():
    # just save it
    write_config_file(conf, confd.CONFIG_FILE)

def set_hd(hd_text):
    # DEBUG info
    print('pvtkgui: conf: got hd_text \"' + str(hd_text) + '\"')
    # parse hd_text
    hd = parse_hd_text(hd_text)
    # DEBUG info
    print('pvtkgui: conf: got hd=' + str(hd) + ' ')
    # just save it
    conf['hd'] = hd

def set_xunlei_dl_path(dl_path, w=None):
    dpath = check_xunlei_dl_path(dl_path, w)
    # just set it
    conf['xunlei_dl_path'] = dpath

def set_ui_type(text=''):
    if not text in support_ui_type:
        text = confd.conf['ui_type']
    # set it
    conf['ui_type'] = text

def set_select_each(flag=False):
    raw = False
    if flag:
        raw = True
    conf['flag_select_each'] = raw

# base functions

# check and set config info
def check_config_file(info, w=None):
    if type(info) != type({}):
        info = confd.conf
    # set hd
    if 'hd' in info:
        set_hd(info['hd'])
    else:
        set_hd(confd.conf['hd'])
    # set xunlei dl path
    if 'xunlei_dl_path' in info:
        set_xunlei_dl_path(info['xunlei_dl_path'], w)
    else:
        set_xunlei_dl_path(confd.conf['xunlei_dl_path'], w)
    
    # set ui_type
    if 'ui_type' in info:
        set_ui_type(info['ui_type'])
    else:
        set_ui_type(confd.conf['ui_type'])
    # set select_each
    if 'flag_select_each' in info:
        set_select_each(info['flag_select_each'])
    else:
        set_select_each(confd.conf['flag_select_each'])
    
    # check and set done

def parse_hd_text(hd_text):
    try:
        hd = int(hd_text)
    except Exception:
        hd = confd.conf['hd']
    return hd

def check_xunlei_dl_path(dl_path, w):
    # TODO nothing to do now
    return dl_path

def write_config_file(conf_obj, conf_file):
    # make json text
    t = json.dumps(conf_obj, sort_keys=True)
    # write conf file
    with open(conf_file, 'w') as f:
        f.write(t)
    # DEBUG info
    print('pvtkgui: conf: write config file \"' + conf_file + '\"')
    # done

# end conf.py


