# gui_style.py, part for parse_video : a fork from parseVideo. 
# gui_style: o/pvtkgui/gui_style: parse_video Tk GUI, style.  
# version 0.0.2.0 test201506171404
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

from tkinter import *
from tkinter.ttk import *

import tkinter as TK
import tkinter.ttk as ttk
import tkinter.font as TKfont

# global vars
ui_text = {}	# main UI text

ui_text['xunlei_dl_dir'] = '迅雷 下载目录'
ui_text['change'] = '更改'
ui_text['start_analyse'] = '开始解析'
ui_text['stop_analyse'] = '停止解析'
ui_text['hd'] = 'hd='

HD_ENTRY_WIDTH = 3

# default font list
ui_font_list = [
    '微软雅黑', 
    # 'Monospace', 
    'Ubuntu Mono', 
    '黑体', 
]

# top part style
top_conf = {
    'hd_style' : 'TLabel', 	# TODO
    'button_style' : 'TButton', 
    'hd_entry_style' : 'TEntry', 
    'entry_style' : 'TEntry', 
}

# main Text style
main_text_conf = {	# TODO
    'color' : '#333', 
    'background_color' : '#999', 
}

# main Text default size
main_text_size = [
    80, 	# x-size, width
    20, 	# y-size, height
]

# main Text style type to tag name
MAIN_TEXT_STYLE_TO_TAG_LIST = {
    # '' : '', 	# TODO
}

# functions

# create main font
def create_main_font():
    pass

# set ttk style
def set_ttk_style():
    pass

# set main text style, set Text tag
def set_main_text_tag(t):
    pass	# TODO

# end gui_style.py


