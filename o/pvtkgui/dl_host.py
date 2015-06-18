# -*- coding: utf-8 -*-
# dl_host.py, part for parse_video : a fork from parseVideo. 
# dl_host: o/pvtkgui/dl_host: parse_video Tk GUI xunlei_dl function. 
# version 0.0.1.0 test201506182128
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

from .b import conf
from .b import conf_default as confd

# global vars
w = None	# main window obj
w_count = 0	# insert main window message count

# functions

# show one msg before main window text
def add_one_msg(text='', tag=None):
    pass	# TODO

# xunlei_dl main function
def xunlei_dl(evinfo, flag_dl_rest=False):
    pass	# TODO

# TODO FIXME reserved old
# use xunlei to download all files, or rest files
def xunlei_dl(flag_rest=False):
    # check evinfo
    if (not 'evinfo' in etc) or (etc['evinfo'] == None):
        # DEBUG info
        print('DEBUG: parse not successful finished. can not add dl tasks to xunlei')
        return
    # set UI
    evinfo = etc['evinfo']
    w = etc['w']
    w.enable_main_text()
    w.insert_main_text('\n')
    w.insert_main_text(DL_XUNLEI_TEXT1 + '\n')
    w.disable_main_text()
    
    # try to add tasks to xunlei
    try:
        task_added_n = xunlei_dl.add_task(evinfo)
        # set UI
        w.enable_main_text()
        w.insert_main_text(DL_XUNLEI_TEXT2[0] + str(task_added_n) + DL_XUNLEI_TEXT2[1] + '\n')
    except xunlei_dl.ComTypesError:
        # set UI
        w.enable_main_text()
        w.insert_main_text(DL_XUNLEI_ERR1 + '\n')
        # start auto install comtypes to support xunlei dl
        # DEBUG info
        print('DEBUG: starting auto install thread ... ')
        run_sub.start_thread(auto_install_comtypes)
        # process done
    except xunlei_dl.CreateComObjError:
        # set UI
        w.enable_main_text()
        w.insert_main_text(DL_XUNLEI_ERR2 + '\n')
    # done

# auto install comtypes
def auto_install_comtypes():
    # TODO
    # DEBUG info
    print('DEBUG: auto install comtypes thread started ')
    # set UI before start install
    w = etc['w']
    w.insert_main_text(DL_XUNLEI_AUTO_INSTALL1 + '\n')
    # start install
    xunlei_dl.install_comtypes()
    # DEBUG info
    print('DEBUG: install comtypes done')
    # install done, update UI
    w.enable_main_text()
    w.insert_main_text(DL_XUNLEI_AUTO_INSTALL2 + '\n')
    # auto install done

# end dl_host.py


