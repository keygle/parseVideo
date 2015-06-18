# -*- coding: utf-8 -*-
# dl_host.py, part for parse_video : a fork from parseVideo. 
# dl_host: o/pvtkgui/dl_host: parse_video Tk GUI xunlei_dl function. 
# version 0.0.4.0 test201506182356
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

import os

from .b import conf
from .b import conf_default as confd
from .b import run_sub

from . import xunlei_dl as dl0

# global vars
w = None	# main window obj
w_count = 0	# insert main window message count

# functions

# show one msg before main window text
def add_one_msg(text='', tag=None):
    global w_count
    w_count += 1
    # insert text
    w.add_main_text(text='\n', flag='start', tag=None)
    w.add_main_text(text=text, flag='start', tag=tag)
    no_text = str(w_count) + ': '
    w.add_main_text(text=no_text, flag='start', tag='gray')
    # add msg done

# xunlei_dl main function
def xunlei_dl(evinfo, flag_dl_rest=False):
    # set UI
    w.enable_main_text()
    add_one_msg(confd.ui_text_dl['add_xunlei_dl_task'], tag='blue')
    
    # try to create agent
    try:
        dl0.create_agent()
    except dl0.ComTypesError:
        w.enable_main_text()
        add_one_msg(confd.ui_text_dl['err_comtypes'], tag='red')
        # auto install comtypes
        run_sub.start_thread(auto_install_comtypes)
        # done
        return
    except dl0.CreateComObjError:
        w.enable_main_text()
        add_one_msg(confd.ui_text_dl['err_create_com'], tag='red')
        # nothing to do
        return
    
    # update xunlei_dl_path config
    dl_path = w.get_xunlei_path_text()
    conf.set_xunlei_dl_path(dl_path)
    # write config file
    conf.write_config()
    # check dl path
    dl_path = check_dl_path(conf.conf['xunlei_dl_path'])
    
    # make file list
    flist = dl0.make_task_list(evinfo)
    
    # check dl rest
    if flag_dl_rest and (dl_path != None):
        flist2 = []
        found_count = 0
        for f in flist:
            # check file exist
            fpath = os.path.join(dl_path, f['file'])
            if os.path.isfile(fpath):
                # found one file
                # TODO check file size
                found_count += 1
            else:	# should be download
                flist2.append(f)
        # check found
        if found_count > 0:
            # update UI
            w.enable_main_text()
            raw_text = confd.ui_text_dl['found_done_file']
            add_one_msg(raw_text[0] + str(found_count) + raw_text[1], tag='green')
            # replace flist
            flist = flist2
    # check dl rest done
    
    # do add task
    add_count = dl0.add_task(flist, dl_path)
    # update UI
    w.enable_main_text()
    raw_text = confd.ui_text_dl['ok_add_task']
    add_one_msg(raw_text[0] + str(add_count) + raw_text[1], tag='blue')
    
    # call xunlei, done

def check_dl_path(dl_path):
    # check is dir
    if os.path.isdir(dl_path):
        # ok, everything is fine
        return dl_path
    # update UI
    w.enable_main_text()
    add_one_msg(confd.ui_text_dl['try_create_dl_path'], tag='green')
    # try to create path
    flag_ok = True
    try:
        # DEBUG info
        print('pvtkgui: dl_host: create dir \"' + str(dl_path) + '\"')
        os.mkdir(dl_path)
    except Exception:
        flag_ok = False
    # re-check dir
    if os.path.isdir(dl_path):
        # ok, everything is fine
        return dl_path
    
    # path error, update UI
    w.enable_main_text()
    add_one_msg(confd.ui_text_dl['dl_path_error'], tag='red')
    # done
    return None

# auto install comtypes
def auto_install_comtypes():
    # DEBUG info
    print('pvtkgui: dl_host: auto install comtypes thread started ')
    # set UI before start install
    w.enable_main_text()
    add_one_msg(confd.ui_text_dl['info_install'], tag='blue')
    
    # start install
    dl0.install_comtypes()
    # DEBUG info
    print('pvtkgui: dl_host: install comtypes done')
    # install done, update UI
    w.enable_main_text()
    add_one_msg(confd.ui_text_dl['info_install_ok'], tag='green')
    # auto install done

# end dl_host.py


