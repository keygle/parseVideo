# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.0.4.0 test201506062226
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

from . import gui
from . import run_sub

# global vars
MAIN_TEXT_INIT_TEXT = ''' 请在 （ ↑ 上方 ↑ 的) 文本框 中 输入 视频播放页面 的 URL. 
    点击 "开始解析" 按钮 或 按 回车 键 开始 解析. 

    请使用 键盘 快捷键 Ctrl+V 粘贴, Ctrl+C 复制. 暂时不支持 右键 菜单 操作 ! 


 parse_video Tk GUI 1          parse_video 图形界面
    version 0.0.2.0 test201506062226









更多帮助信息, 请见
  https://github.com/sceext2/parse_video/wiki/zh_cn-easy-guide

  如有更多问题, 需要讨论, 请
          加 qq 群 飞驴友视频下载交流群 141712855

copyright 2015 sceext <sceext@foxmail.com> 2015.06
'''

etc = {}
etc['w'] = None	# main window obj
etc['flag_doing'] = False	# global doing flag

# functions

# init
def init():
    # FIXME debug here
    print('DEBUG: parse_video Tk GUI start init')
    # create main window
    w = gui.MainWin()
    etc['w'] = w
    # set callback
    w.callback_main_button = on_main_button
    # show main window
    w.start()
    # set init text
    w.set_main_text(MAIN_TEXT_INIT_TEXT)
    # FIXME debug here
    print('DEBUG: main window created, starting main loop')
    w.mainloop()
    # init done

# on button click
def on_main_button():
    # FIXME debug here
    print('DEBUG: main button clicked')
    # check flag_doing
    if etc['flag_doing']:
        print('ERROR: doing, can not start parse')
        return
    # get url
    w = etc['w']
    url_to = w.get_entry_text()
    # FIXME deubg here
    print('DEBUG: got input url \"' + url_to + '\"')
    # set UI
    
    # set flag
    etc['flag_doing'] = True
    # disable main button
    w.disable_main_button()
    w.enable_main_text()
    
    # set text
    w.set_main_text(' 正在解析 URL \"' + url_to + '\" ... \n    请稍等 一小会儿 :-) \n')
    
    # FIXME debug info
    print('DEBUG: starting parse_video')
    # just start parse_video
    run_sub.run_pv_thread(on_sub_finished, url_to)

# on sub finished
def on_sub_finished(stdout, stderr):
    # FIXME debug here
    print('DEBUG: sub process parse_video ended')
    w = etc['w']
    
    # decode sub output as utf-8, try to handle errors
    try:
        stdout = str(stdout.decode('utf-8', ))
    except Exception as e:
        # FIXME DEBUG here
        print('DEBUG: decode stdout as utf-8 failed\n' + str(e))
        stdout = str(stdout.decode('utf-8', 'ignore'))
    try:
        stderr = str(stderr.decode('utf-8', ))
    except Exception as e:
        # FIXME DEBUG here
        print('DEBUG: decode stderr as utf-8 failed\n' + str(e))
        stderr = str(stderr.decode('utf-8', 'ignore'))
    # write result
    out = stderr + '\n' + stdout + '\n'
    
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


