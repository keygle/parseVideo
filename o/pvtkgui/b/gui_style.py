# gui_style.py, part for parse_video : a fork from parseVideo. 
# gui_style: o/pvtkgui/gui_style: parse_video Tk GUI, style.  
# version 0.1.2.0 test201506231550
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

from ...gui import tk_base

# global vars
ui_text = {}	# main UI text

ui_text['xunlei_dl_dir'] = '迅雷 下载目录'
ui_text['change'] = '更改'
ui_text['start_analyse'] = '开始解析'
ui_text['stop_analyse'] = '停止解析'
ui_text['hd'] = ' hd='
ui_text['main_win_title'] = 'parse_video Tk GUI 2'	# main window title

# menu item text
ui_top_menu = {
    'paste_url' : '粘贴 URL', 
    'copy_url'  : '复制 全部文本', 
}

ui_body_menu = {
    'copy_selected' : '复制 选中文本', 
    'copy_all_url'  : '复制 全部 URL', 
    # NOTE there should be a separator
    'xunlei_dl_all_url'  : '使用 迅雷 下载全部 URL', 
    'xunlei_dl_rest_url' : '使用 迅雷 下载 [剩余] URL', 
    # NOTE there should be a separator
    'conf' : '配置', 
}

# sub menu
ui_body_menu2 = {
    'full_ui' : '完整界面', 
    'simple_ui' : '精简界面', 
    # NOTE there should be a separator
    'select_each' : '启用 逐个选择', 
}

HD_ENTRY_WIDTH = 3

# default font list
ui_font_list = [
    '微软雅黑', 
    # 'Monospace', 
    'Ubuntu Mono', 
    '黑体', 
]

ui_main_font_size = 16
ui_main_big_font_size = 20

ui_h2_font_size = 30

# ui_font list
ui_font = {}

# top part style
top_conf = {
    'hd_style' : 'HD.TLabel',
    'button_style' : 'Blue.Button.TLabel', 
    'hd_entry_style' : 'HD.TEntry', 
    'entry_style' : 'Main.TEntry', 
}

# main Text style
main_text_conf = {
    'color' : '#333', 
    'background_color' : '#bd9', 
    'cursor_color' : '#f52', 
}

# main Text default size
main_text_size = [
    80, 	# x-size, width
    20, 	# y-size, height
]

# main Text style type to tag name
MAIN_TEXT_STYLE_TO_TAG_LIST = {
    'info' : 'info', 
    'h2' : 'h2', 
    'gray' : 'gray', 
    'red' : 'red', 
    'red_bold' : 'red_bold', 
    'blue' : 'blue', 
    'blue_bold' : 'blue_bold', 
    'big' : 'big', 
    'big_blue' : 'big_blue', 
    'big_red' : 'big_red', 
    'white_blue' : 'white_blue', 
    'bold' : 'bold', 
    'a' : 'a', 
    'green' : 'green', 
    
    # for main parse result text
    'info_title' : 'big_bold', 
    'info_name' : 'bold', 
    'info_value' : 'red', 
}

def make_main_text_tag_style():
    return {
        'info' : {
    	    'color': '#00f', 
        }, 
        'h2' : {
            'font' : ui_font['h2'], 
            'color' : '#000', 
        }, 
        'gray' : {
            'color' : '#666', 
        }, 
        'red' : {
            'color' : '#f00', 
        }, 
        'blue' : {
            'color' : '#00f', 
        }, 
        'green' : {
            'color' : '#0f0', 
        }, 
        'blue_bold' : {
            'font' : ui_font['bold'], 
            'color' : '#00f', 
        }, 
        'white_blue' : {
            'background_color' : '#00f', 
            'color' : '#fff', 
        }, 
        'big' : {
            'font' : ui_font['big'], 
        }, 
        'big_blue' : {
            'font' : ui_font['big'], 
            'color' : '#00f', 
        }, 
        'big_red' : {
            'font' : ui_font['big'], 
            'color' : '#f00', 
        }, 
        'big_bold' : {
            'font' : ui_font['big'], 
            'color' : '#111', 
        }, 
        'bold' : {
            'font' : ui_font['bold'], 
            'color' : '#111', 
        }, 
        'red_bold' : {
            'font' : ui_font['bold'], 
            'color' : '#f00', 
        }, 
        'a' : {
            'font' : ui_font['italic_underline'], 
            'color' : '#00f', 
        }, 
        # NOTE sel should be the last tag
        'sel' : {
            'background_color' : '#3f3', 
            'color' : '#fff', 
        }, 
    }
    # done

# functions

# create main font
def create_main_font(root):
    main_font = tk_base.create_font(root, font_family=ui_font_list, size=ui_main_font_size, bold=False)
    main_font_bold = tk_base.create_font(root, font_family=ui_font_list, size=ui_main_font_size, bold=True)
    main_big_font_bold = tk_base.create_font(root, font_family=ui_font_list, size=ui_main_big_font_size, bold=True)
    
    main_h2_font = tk_base.create_font(root, font_family=ui_font_list, size=ui_h2_font_size, bold=True)
    italic_underline_font = tk_base.create_font(root, font_family=ui_font_list, size=ui_main_font_size, bold=False, italic=True, underline=True)
    
    # save font
    ui_font['normal'] = main_font
    ui_font['bold'] = main_font_bold
    ui_font['big'] = main_big_font_bold
    ui_font['h2'] = main_h2_font
    ui_font['italic_underline'] = italic_underline_font
    
    return main_font, main_font_bold, main_big_font_bold

# set ttk style
def set_ttk_style():
    style = Style()
    # set styles
    
    # set TButton
    style.configure('TButton', font=ui_font['normal'])
    
    # set HD.TLabel
    style.configure('HD.TLabel', foreground='#fff', background='#00f')
    
    # Blue.TButton
    style.configure('Blue.Button.TLabel', 
        background='#00f', 
        foreground='#fff', 
        relief='flat', 
        font=ui_font['bold'], 
        padding=(25, 6))
    style.map('Blue.Button.TLabel', 
        background=[('pressed', '#008'), ('active', '#44f')], 
        foreground=[('pressed', '#0f0'), ('active', '#ff0')])
    
    # Red.TButton
    style.configure('Red.Button.TLabel', 
        background='#f00', 
        foreground='#fff', 
        relief='flat', 
        font=ui_font['bold'], 
        padding=(25, 6))
    style.map('Red.Button.TLabel', 
        background=[('pressed', '#800'), ('active', '#f44')], 
        foreground=[('pressed', '#0f0'), ('active', '#ff0')])
    
    # HD.TEntry
    style.configure('HD.TEntry', foreground='#00f', background='#99c')
    
    # Main.TEntry
    # TODO
    
    # Red.TEntry
    style.configure('Red.TEntry', foreground='#f00')

# set main text style, set Text tag
def set_main_text_tag(t):
    tlist = make_main_text_tag_style()
    for i in tlist:
        t.set_tag_style(i, tlist[i])
    # set Text tag style, done

# end gui_style.py


