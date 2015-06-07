# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.0.8.0 test201506071738
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

# global vars
MAIN_TEXT_INIT_TEXT = '''        请在 （ ↗ 上方 ↗ 右侧 的) 文本框 中 输入 视频播放页面 的 URL. 
                点击 "开始解析" 按钮 或 按 回车 键 开始 解析. 

    请使用 键盘 快捷键 Ctrl+V 粘贴, Ctrl+C 复制. 暂时不支持 右键 菜单 操作 ! 


 parse_video Tk GUI 1          parse_video 图形界面
    version 0.0.3.0 test201506071503

hd 值 说明
     左侧上方的文本框, hd= 数字, 用于选择 解析并输出 哪种 清晰度 的视频文件 URL. 
 这样做可以加快解析速度. 
     hd 值 请在解析结果 中 查看. 




更多帮助信息, 请见
  https://github.com/sceext2/parse_video/wiki/zh_cn-easy-guide

  如有更多问题, 需要讨论, 请
          加 qq 群 飞驴友视频下载交流群 141712855

copyright 2015 sceext <sceext@foxmail.com> 2015.06
'''

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
    # show main window
    w.start()
    # set init text
    w.set_main_text(MAIN_TEXT_INIT_TEXT)
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
    w.set_main_text(' 正在解析 URL \"' + url_to + '\" ... \n    请稍等 一小会儿 :-) \n')
    
    # DEBUG info
    print('DEBUG: starting parse_video')
    # just start parse_video
    run_sub.run_pv_thread(on_sub_finished, url_to, hd, write_config=write_config)

def write_config():
    write_config_file(etc['conf'])
    # done

# on copy URL, to copy urls in main_text to clip board
def on_copy_url():
    text = conf['main_text']
    w = conf['w']
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
    # write result
    out = stderr + '\n' + stdout + '\n'
    
    # save Text
    conf['main_text'] = out
    # set to main Text
    w.enable_main_text()
    w.set_main_text(out)
    
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

# end entry.py


