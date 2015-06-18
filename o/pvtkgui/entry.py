# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.1.10.0 test201506181239
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
import time
import re

from . import gui
from . import run_sub
# from . import xunlei_dl
from . import conf
from . import conf_default as confd

# global vars

# parse_video Tk GUI, pvtkgui config file path
CONFIG_FILE = './etc/pvtkgui.conf.json'

# NOTE should be set by out
flag_debug = False

etc = {}
etc['w'] = None	# main window obj

etc['analyse_thread'] = None	# analyse sub thread obj
etc['flag_doing'] = False	# global doing flag

# base funciton

def add_main_text_style(tlist):
    w = etc['w']
    # add each part
    for item in tlist:
        w.add_main_text(text=item[1], tag=item[0])
    # add main text style done

# functions

def init():
    # init main window
    init_main_win()
    # load config
    init_config()
    # start watch thread
    init_watch()
    
    # init done, start main loop
    start_mainloop()

def start_mainloop():
    # DEBUG info
    print('pvtkgui: entry: starting mainloop')
    # start main loop
    w = etc['w']
    w.mainloop()
    # DEBUG info
    print('pvtkgui: entry: mainloop stoped')

# init MainWin
def init_main_win():
    # DEBUG info
    print('pvtkgui: entry: parse_video Tk GUI start init')
    # create main window
    w = gui.MainWin()
    etc['w'] = w
    # set callback
    w.callback = on_main_win
    # show main window
    w.start()
    # set main window init text
    w.enable_main_text()
    w.clear_main_text()
    add_main_text_style(confd.main_win_init_text)
    # DEBUG info
    print('pvtkgui: entry: main window created')
    # main win init done

# init config
def init_config():
    # load config file
    conf.load_config(confd.CONFIG_FILE)
    # update UI
    w = etc['w']
    w.set_hd_text(str(conf.conf['hd']))
    w.set_xunlei_path_text(str(conf.conf['xunlei_dl_path']))
    # done

# start watch sub thread
def init_watch():
    # just start watch thread
    run_sub.start_thread(watch_thread)

# on MainWin event callback
def on_main_win(event, data):
    pass

# watch sub thread
def watch_thread(arg=True):
    # DEBUG info
    print('pvtkgui: entry: watch thread start')
    # init
    w = etc['w']
    
    info = {}
    info['old_clip'] = ''
    info['old_url'] = ''
    
    # loop watch
    while arg:
        # sleep before check
        time.sleep(confd.watch_thread_sleep_time_s)
        
        # watch clip
        watch_clip(w, info)
        
        # watch url
        watch_url(w, info)
        # watch done
    # one loop done

# watch clip
def watch_clip(w, info):
    # get clip text
    t = w.clip_get()
    if t == None:
        return
    
    # check changed
    if t == info['old_clip']:
        return
    
    info['old_clip'] = t
    # check match re
    rlist = confd.SUPPORT_URL_RE
    flag_match = False
    for r in rlist:
        if re.match(r, t):
            flag_match = True
            break
    # if match, set it
    if flag_match:
        w.set_url_text(t)
    # watch clip done

# watch url
def watch_url(w, info):
    # get url text
    t = w.get_url_text()
    # check changed
    if t == info['old_url']:
        return
    # check match re
    rlist = confd.SUPPORT_URL_RE
    flag_match = False
    for r in rlist:
        if re.match(r, t):
            flag_match = True
            break
    # iif match, set status to ok
    if flag_match:
        w.set_url_status('ok')
    else:	# set not ok
        w.set_url_status('none')
    # watch url done

# start analyse
def start_analyse():
    pass

# stop analyse
def stop_analyse():
    pass

# call xunlei to dl
def xunlei_dl():
    pass

# TODO
# auto retry, when analyse not get the hd= video, auto try to get max hd video info
def auto_retry(evinfo, hd_last):
    # get hd
    if len(evinfo['video']) < 1:
        # DEBUG info
        print('DEBUG: no video in evinfo, len 0')
        return
    # get hd list
    hd_list = []
    for v in evinfo['video']:
        hd_list.append(v['hd'])
    # sort hd
    hd_list.sort(reverse=True)
    if len(hd_list) < 1:
        print('DEBUG: ERROR: hd_list length 0')
        return
    if hd_last in hd_list:
        print('DEBUG: ERROR: hd_last in hd_list')
        return
    # check max hd
    if hd_last > hd_list[0]:
        # should use max hd
        hd_new = hd_list[0]
        type_text = AUTO_RETRY_TEXT2[0]
    elif hd_last < hd_list[-1]:
        # should use min hd
        hd_new = hd_list[-1]
        type_text = AUTO_RETRY_TEXT2[2]
    else:	# should select one hd
        for i in range(len(hd_list)):
            if (hd_last < hd_list[i]) and (hd_last > hd_list[i + 1]):
                hd_new = hd_list[i + 1]
                type_text = AUTO_RETRY_TEXT2[1]
                break
    # auto select hd, done
    
    # get url
    url_to = evinfo['info']['url']
    # set auto retry text
    w = etc['w']
    w.enable_main_text()
    w.insert_main_text(AUTO_RETRY_TEXT1[0] + type_text + AUTO_RETRY_TEXT1[1] + str(hd_new) + '\n')
    
    # just start re analyse
    run_sub.run_pv_thread(on_sub_finished, url_to, hd_new)
    # done

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

# end entry.py


