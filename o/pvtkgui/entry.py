# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/entry: parse_video Tk GUI main entry. 
# version 0.0.2.0 test201506062137
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
MAIN_TEXT_INIT_TEXT = '''Please input URL ↑ here ↑ 

 parse_video Tk GUI 1

test

More help information, please see 
<https://github.com/sceext2/parse_video/wiki/zh_cn-easy-guide>

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
    w.set_main_text('Now doing parse URL \"' + url_to + '\" ... \n        Please wait a moment. ')
    
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


