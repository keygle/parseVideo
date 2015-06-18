# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.1.6.0 test201506112233
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
from . import xunlei_dl

DL_XUNLEI_TEXT1 = '1. 正在向 迅雷 添加下载任务, 请稍候 ... '
DL_XUNLEI_ERR1 = '2. 错误: 没有安装 comtypes. 无法调用 迅雷 com 接口 ! '
DL_XUNLEI_TEXT2 = ['2. 成功: 已经添加 ', ' 个下载任务至 迅雷. ']
DL_XUNLEI_ERR2 = '2. 错误: 无法创建 迅雷 com 接口. (ThunderAgent.Agent, ThunderAgent.Agent64) \n  请确认 迅雷 已经正确安装. '

DL_XUNLEI_AUTO_INSTALL1 = '3. 提示: 正在自动安装 迅雷 下载 支持组件, 请稍候 ... '
DL_XUNLEI_AUTO_INSTALL2 = '4. 成功: 已经完成安装 comtypes. 再试试吧~~~ 现在 使用 迅雷 下载 应该没有问题了. ^_^ :-)'

AUTO_RETRY_TEXT1 = ['提示: 当前指定的 视频清晰度 无法达到, 正在 自动 解析 ', '清晰度的 视频 ... \n    目标 hd=']
AUTO_RETRY_TEXT2 = ['最高', '下一种', '最低']

# functions

# on copy URL, to copy urls in main_text to clip board
def on_copy_url():
    text = etc['main_text']
    w = etc['w']
    to = get_url_list(text)
    # check result
    if to != None:
        w.clip_set(to)
    # done

def get_url_list(text):
    line = text.split('\n')
    out = []
    for l in line:
        if l.find('http://') == 0:
            out.append(l)
    out.append('')
    # output
    if len(out) > 1:	# found urls
        return ('\n').join(out)
    else:	# not found url
        return None

# on sub finished
def on_sub_finished(stdout, stderr):
    
    # check result, auto retry
    if evinfo != None:
        # check url numbers
        ulist = []
        for v in evinfo['video']:
            for f in v['file']:
                ulist.append(f)
        if len(ulist) < 1:
            # DEBUG info
            print('DEBUG: entry.py: auto retry, last_hd=' + str(etc['last_hd']))
            # should start auto retry
            auto_retry(evinfo, etc['last_hd'])
            return
    
    # get result OK, not need retry
    
    # write result OK, set UI
    
    # enable main button
    w.enable_main_button()
    # set flag_doing
    etc['flag_doing'] = False
    # done

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

# use xunlei do download all files
def on_xunlei_dl():
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


