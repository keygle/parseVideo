# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.0.12.0 test201506072331
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

from . import gui
from . import run_sub
from . import xunlei_dl

make_rename_list_ = None
output_text_ = None

# set import
def set_import(make_rename_list=None, output_text=None):
    global make_rename_list_
    global output_text_
    make_rename_list_ = make_rename_list
    output_text_ = output_text
    # set sub import
    xunlei_dl.set_import(make_rename_list=make_rename_list, output_text=output_text)
    # set import done

# global vars
MAIN_TEXT_INIT_TEXT = '''        请在 （ ↗ 上方 ↗ 右侧 的) 文本框 中 输入 视频播放页面 的 URL. 
                点击 "开始解析" 按钮 或 按 回车 键 开始 解析. 


 parse_video Tk GUI 1          parse_video 图形界面
    version 0.0.4.0 test201506071747


+ hd 值 说明
       左侧上方的文本框, hd= 数字, 用于选择 解析并输出 哪种 清晰度 的视频文件 URL. 
   这样做可以加快解析速度. 
       hd 值 请在解析结果 中 查看. 

+ 操作说明
  
  鼠标 中键 点击 URL 输入文本框 (上方右侧), 可以直接从剪切板粘贴 URL. 
  
  按 F9 键 或 右键菜单, 可以直接复制 解析结果 中的全部 URL 到剪切板. 不复制其它文本. 






更多帮助信息, 请见
  https://github.com/sceext2/parse_video/wiki/zh_cn-easy-guide

  如有更多问题, 需要讨论, 请
          加 qq 群 飞驴友视频下载交流群 141712855

copyright 2015 sceext <sceext@foxmail.com> 2015.06
'''

DL_XUNLEI_TEXT1 = '1. 正在向 迅雷 添加下载任务, 请稍候 ... '
DL_XUNLEI_ERR1 = '2. 错误: 没有安装 comtypes. 无法调用 迅雷 com 接口 ! '
DL_XUNLEI_TEXT2 = ['2. 成功: 已经添加 ', ' 个下载任务至 迅雷. ']
DL_XUNLEI_ERR2 = '2. 错误: 无法创建 迅雷 com 接口. (ThunderAgent.Agent, ThunderAgent.Agent64) \n  请确认 迅雷 已经正确安装. '

# parse_video Tk GUI, pvtkgui config file path
CONFIG_FILE = './etc/pvtkgui.conf.json'
DEFAULT_HD = 2

etc = {}
etc['w'] = None	# main window obj
etc['flag_doing'] = False	# global doing flag
etc['conf'] = None	# pvtkgui config obj
etc['main_text'] = ''	# main text showed in main Text GUI window

# base funciton
def make_default_config_obj():
    conf = {}
    conf['hd'] = DEFAULT_HD
    # done
    return conf

def check_config_file(conf):
    if not 'hd' in conf:
        raise Exception('config file error, no hd in conf')
    hd = int(conf['hd'])
    if hd > 100:
        raise Exception('config file error, hd value too big')
    # check done
    return conf

def load_config_file():
    # try to read config file
    t = ''
    with open(CONFIG_FILE, 'r') as f:
        t = f.read()
    # parse as json
    try:
        conf = json.loads(t)
        conf = check_config_file(conf)
    except Exception as e:
        # DEBUG info
        print('DEBUG: load config file \"' + CONFIG_FILE + '\" failed, use default config instead. ')
        try:
            print(e)
        except Exception:
            pass
        # use default config instead
        conf = make_default_config_obj()
    # done
    return conf

def write_config_file(conf_obj):
    # make json text
    t = json.dumps(conf_obj)
    # write conf file
    with open(CONFIG_FILE, 'w') as f:
        f.write(t)
    # DEBUG info
    print('DEBUG: save config file to \"' + CONFIG_FILE + '\"')
    # done

def parse_hd_text(hd_text):
    try:
        hd = int(hd_text)
    except Exception:
        hd = DEFAULT_HD
    # done
    return hd

# functions

# init
def init():
    # DEBUG info
    print('DEBUG: parse_video Tk GUI start init')
    # create main window
    w = gui.MainWin()
    etc['w'] = w
    # set callback
    w.callback_main_button = on_main_button
    w.callback_copy_url = on_copy_url
    w.callback_xunlei_dl = on_xunlei_dl
    # show main window
    w.start()
    # set init text
    w.clear_main_text()
    w.append_main_text(MAIN_TEXT_INIT_TEXT)
    # DEBUG info
    print('DEBUG: main window created, starting main loop')
    # load default config file
    etc['conf'] = load_config_file()
    # DEBUG info
    print('DEBUG: load config file ')
    # set hd to ui
    hd = str(etc['conf']['hd'])
    w.set_hd_text(hd)
    # DEBUG info
    print('DEBUG: set hd=' + hd)
    
    # start main loop
    w.mainloop()
    # init done

# on button click
def on_main_button():
    # DEBUG info
    print('DEBUG: main button clicked')
    # check flag_doing
    if etc['flag_doing']:
        print('ERROR: doing, can not start parse')
        return
    # get url
    w = etc['w']
    url_to = w.get_entry_text()
    # DEBUG info
    print('DEBUG: got input url \"' + url_to + '\"')
    # get hd
    hd_text = w.get_hd_text()
    # DEBUG info
    print('DEBUG: got hd_text \"' + hd_text + '\"')
    # update etc conf
    hd = parse_hd_text(hd_text)
    etc['conf']['hd'] = hd
    # DEBUG info
    print('DEBUG: got hd=' + str(hd))
    # set UI
    
    # set flag
    etc['flag_doing'] = True
    # disable main button
    w.disable_main_button()
    w.enable_main_text()
    # set hd
    w.set_hd_text(str(hd))
    
    # set text
    w.clear_main_text()
    w.append_main_text(' 正在解析 URL \"' + url_to + '\" ... \n    请稍等 一小会儿 :-) \n')
    
    # DEBUG info
    print('DEBUG: starting parse_video')
    # just start parse_video
    run_sub.run_pv_thread(on_sub_finished, url_to, hd, write_config=write_config)

def write_config():
    write_config_file(etc['conf'])
    # done

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
    # DEBUG info
    print('DEBUG: sub process parse_video ended')
    w = etc['w']
    
    # decode sub output as utf-8, try to handle errors
    try:
        stdout = str(stdout.decode('utf-8', ))
    except Exception as e:
        # DEBUG info
        print('DEBUG: decode stdout as utf-8 failed\n' + str(e))
        stdout = str(stdout.decode('utf-8', 'ignore'))
    try:
        stderr = str(stderr.decode('utf-8', ))
    except Exception as e:
        # DEBUG info
        print('DEBUG: decode stderr as utf-8 failed\n' + str(e))
        stderr = str(stderr.decode('utf-8', 'ignore'))
    # try to parse stdout as json
    flag_sub_ok = False
    try:
        evinfo = json.loads(stdout)
        flag_sub_ok = True
    except Exception:
        # make error output
        out = stderr + '\n' + stdout + '\n'
    # check sub_ok
    if flag_sub_ok:
        # make output text
        out = output_text_.make_easy_text(evinfo)
    # write result
    
    # save evinfo
    etc['evinfo'] = evinfo
    
    # save Text
    etc['main_text'] = out
    # set to main Text
    w.enable_main_text()
    w.clear_main_text()
    w.append_main_text(out)
    
    # check error
    if stderr == '':
        # no error, not let user change destroy result
        w.disable_main_text()
    
    # write result OK, set UI
    
    # enable main button
    w.enable_main_button()
    # set flag_doing
    etc['flag_doing'] = False
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
    except xunlei_dl.CreateComObjError:
        # set UI
        w.enable_main_text()
        w.insert_main_text(DL_XUNLEI_ERR2 + '\n')
    # done

# end entry.py


