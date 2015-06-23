# -*- coding: utf-8 -*-
# dl_host.py, part for parse_video : a fork from parseVideo. 
# dl_host: o/pvtkgui/dl_host: parse_video Tk GUI xunlei_dl function. 
# version 0.0.9.0 test201506232059
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

flag_ui_hide = False	# ui_type, hide msg

# supported finished video file ext name
supported_ext = [
    'mp4', 
    'flv', 
    'f4v', 
    'fhv', 
    'letv', 
]

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
def xunlei_dl(evinfo, flag_dl_rest=False, select_list=None):
    # check UI type
    global flag_ui_hide
    if conf.conf['ui_type'] == 'simple_ui':
        flag_ui_hide = True
    else:
        flag_ui_hide = False
    
    # set UI
    w.enable_main_text()
    if not flag_ui_hide:
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
        flist2, found_list = check_file_done(flist, dl_path)
        found_count = len(found_list)
        # check found count
        if found_count > 0:
            # DEBUG info
            out_flist = ('\n').join(found_list) + '\n'
            print('pvtkgui: dl_host: found done files \n' + out_flist)
            # update UI
            w.enable_main_text()
            raw_text = confd.ui_text_dl['found_done_file']
            if not flag_ui_hide:
                add_one_msg(raw_text[0] + str(found_count) + raw_text[1], tag='green')
            # replace flist
            flist = flist2
        # check dl rest done
    elif select_list != None:	# use xunlei_dl select_each selected items
        # check list length
        if len(select_list) != len(flist):
            # ERROR
            print('pvtkgui: dl_host: ERROR: select_list len ' + str(len(select_list)) + ' not match flist len ' + str(len(flist)) + ' ')
        else:	# make select list
            new_list = []
            for i in range(len(flist)):
                if select_list[i]:
                    new_list.append(flist[i])
            # make new list done
            flist = new_list
    # process flist done
    
    # do add task
    add_count = dl0.add_task(flist, dl_path)
    # update UI
    w.enable_main_text()
    raw_text = confd.ui_text_dl['ok_add_task']
    if not flag_ui_hide:
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

# check file done, check if file has been finished download
def check_file_done(flist, dl_path):
    # get done file list
    ed_list = get_file_list(dl_path)
    ed_list2 = []
    flist2 = []
    # check each file
    for f in flist:
        fpath = f['file']
        ext = fpath.rsplit('.', 1)
        # check exist
        if ext[0] in ed_list:
            ed_list2.append(fpath)
        else:
            flist2.append(f)
    # done
    return flist2, ed_list2

# get file list
def get_file_list(dl_path):
    # check dl_path
    if not os.path.isdir(dl_path):
        return []
    # check first dir
    ed_list = []
    
    flist, dlist = get_flat_file_list(dl_path)
    ed_list += flist
    
    # check sub dir
    for d in dlist:
        flist, dlist2 = get_flat_file_list(d)
        ed_list += flist
    
    # check and get file list done
    return ed_list

# get file list in one dir
def get_flat_file_list(dpath):
    raw_list = os.listdir(dpath)
    dlist = []
    flist = []
    for f in raw_list:
        fpath = os.path.join(dpath, f)
        if os.path.isdir(fpath):
            dlist.append(fpath)
        elif os.path.isfile(fpath):
            # check ext
            ext = f.rsplit('.', 1)
            if ext[1] in supported_ext:
                flist.append(ext[0])
    # done
    return flist, dlist

# end dl_host.py


