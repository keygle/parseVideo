# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.1.13.0 test201506181544
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

from .b import gui
from .b import run_sub
# from . import xunlei_dl
from .b import conf
from .b import conf_default as confd

from ..output import easy_text

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
    w = etc['w']
    # check which event
    if event == 'start_stop':
        # check flag
        if etc['flag_doing']:
            stop_parse()
        else:
            start_parse()
    elif event == 'xunlei_dl_path_change':
        # just start a thread to select dir
        start_change_dl_path_thread()
    
    elif event == 'top_paste':
        t = w.clip_get()
        if (t != None) and (t != ''):
            # just paste first line
            line = t.split('\n')
            w.set_url_text(line[0])
    elif event == 'top_copy':
        t = w.get_url_text()
        if t != '':
            w.clip_set(t)
    elif event == 'body_copy_selected':
        t = w.get_main_text()
        if (type(t) == type('')) and (t != ''):
            w.clip_set(t)
    
    elif event == 'body_copy_all_url':
        pass
    
    elif event == 'xunlei_dl_all_url':
        pass
    
    elif event == 'xunlei_dl_rest_url':
        pass
    
    else:
        # DEBUG info
        print('pvtkgui: entry: unknow event [' + str(event) + ']')
    # process event done

# stop parse
def stop_parse():
    # set flag
    etc['flag_doing'] = False
    # update UI
    w = etc['w']
    w.set_button_status('start')
    # DEBUG info
    print('pvtkgui: entry: try to terminate parsev sub process')
    # just kill parsev subprocess
    run_sub.terminate_parsev()
    # set UI text
    w.enable_main_text()
    w.add_main_text(confd.ui_text['user_stop_parse'], flag='start', tag='red_bold')
    # stop parse done

# start parse
def start_parse():
    # set flag
    etc['flag_doing'] = True
    # update UI
    w = etc['w']
    w.set_button_status('stop')
    
    # set UI text
    w.enable_main_text()
    w.clear_main_text()
    add_main_text_style(confd.ui_text_doing_parse)
    
    # get config hd and url
    url_to = w.get_url_text()
    # DEBUG info
    print('pvtkgui: entry: got input url \"' + url_to + '\"')
    # get hd
    hd_text = w.get_hd_text()
    # set config
    conf.set_hd(hd_text)
    # update UI
    hd = conf.conf['hd']
    w.set_hd_text(str(hd))
    
    # save last_hd, NOTE
    etc['last_hd'] = hd
    
    # just start sub process
    run_sub.run_pv_thread(on_parsev_done, url_to, hd, write_config=conf.write_config, flag_debug=flag_debug)

# on parsev subprocess finished
def on_parsev_done(stdout, stderr):
    # set flag
    etc['flag_doing'] = False
    # DEBUG info
    print('pvtkgui: entry: parsev done')
    w = etc['w']
    
    # decode stdout as utf-8, and parse as json
    try:
        stdout = str(stdout.decode('utf-8'))
    except Exception as e:
        # DEBUG info
        print('pvtkgui: entry: decode stdout as utf-8 failed \n' + str(e))
        stdout = str(stdout.decode('utf-8', 'ignore'))
    try:
        stderr = str(stderr.decode('utf-8'))
    except Exception as e:
        print('pvtkgui: entry: decode stderr as utf-8 failed \n' + str(e))
        stderr = str(stderr.decode('utf-8', 'ignore'))
    # try to parse stdout
    flag_sub_ok = False
    evinfo = None
    try:
        evinfo = json.loads(stdout)
        flag_sub_ok = True
    except Exception:
        # make error output
        out = stderr + '\n' + stdout + '\n'
    # check sub ok
    if flag_sub_ok:
        w.enable_main_text()
        w.clear_main_text()
        
        output = easy_text.output_style(evinfo)
        add_main_text_style(output)
        
        w.disable_main_text()
    else: # NOTE should write error info
        w.enable_main_text()
        w.clear_main_text()
        add_main_text_style(confd.ui_text_parse_failed)
        w.add_main_text(out, tag='red')
    # write result
    
    # save evinfo
    if not flag_sub_ok:
        try:
            etc.pop('evinfo')
        except Exception:
            pass
    else:
        etc['evinfo'] = evinfo
    
    # TODO check result and auto retry
    
    # update UI
    w.set_button_status('start')
    # done

# start xunlei dl path change thread
def start_change_dl_path_thread():
    run_sub.start_thread(change_dl_path_thread)

def change_dl_path_thread():
    w = etc['w']
    old_dir = w.get_xunlei_path_text()
    # open select dialog
    new_dir = w.select_dir(old_path=old_dir, title=confd.ui_text['change_dl_path_title'])
    # check result
    if (type(new_dir) == type('')) and (new_dir != ''):
        # just set it to main UI
        w.set_xunlei_path_text(new_dir)
        # TODO write config file
    # change dl path done

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


