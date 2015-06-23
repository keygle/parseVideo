# gui2.py, part for parse_video : a fork from parseVideo. 
# gui2: o/pvtkgui/gui: parse_video Tk GUI, main window sub part. 
# version 0.1.2.0 test201506231753
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
import tkinter.tix as tix

from . import gui_style as guis
from ...gui import tk_base

# global vars

# functions

# class

# top part
class PartTop(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        # NOTE font and style should be set
        self.hd_font = None
        self.hd_entry_font = None
        self.hd_style = guis.top_conf['hd_style']
        self.hd_entry_style = guis.top_conf['hd_entry_style']
        self.button_style = guis.top_conf['button_style']
        
        self.entry_font = None
        self.entry_style = guis.top_conf['entry_style']
        
        self.p_hd = None	# hd part
        self.p_e = None		# main URL entry
        self.p_b = None		# main button
        
        self.tk_f = []	# tkinter frames
    
    # operations
    def get_hd_text(self):
        return self.p_hd.get_text()
    
    def set_hd_text(self, text=''):
        self.p_hd.set_text(text=text)
    
    def get_url_text(self):
        return self.p_e.get_text()
    
    def set_url_text(self, text=''):
        self.p_e.set_text(text=text)
    
    def set_url_text_style(self, style='TEntry'):
        self.p_e.set_entry_style(style=style)
    
    def set_button_text(self, text=''):
        self.p_b.config(text=text)
    
    def set_button_style(self, style='TButton'):
        self.p_b.config(style=style)
    
    # to send event list
    #	start_stop	start or stop analyse
    #	show_menu	show top part URL entry menu
    #	paste		should paste text in URL entry
    
    # on sub el
    def _on_button(self, event=None):
        self._send('start_stop', event)
    
    def _on_hd_entry(self, event, data):
        if event == 'key_enter':
            self._send('start_stop', data)
        # process sub el done
    
    def _on_url_entry(self, event, data):
        if event == 'key_enter':
            self._send('start_stop', data)
        elif event == 'mouse_right':
            self._send('show_menu', data)
        elif event == 'mouse_middle':
            self._send('paste', data)
        # process sub el done
    
    def start(self, parent):
        # save parent
        self.parent = parent
        # create UI
        self._create()
        self._set_el()
    
    def _create(self):
        hd = tk_base.EntryBox()
        self.p_hd = hd
        e = tk_base.EntryBox()
        self.p_e = e
        b = Label(self.parent, text=guis.ui_text['start_analyse'], style=self.button_style)
        self.p_b = b
        # set EntryBox
        hd.label_text = guis.ui_text['hd']
        hd.entry_width = guis.HD_ENTRY_WIDTH
        hd.label_font = self.hd_font
        hd.entry_font = self.hd_entry_font
        hd.label_style = self.hd_style
        hd.entry_style = self.hd_entry_style
        
        e.entry_font = self.entry_font
        e.entry_style = self.entry_style
        
        # pack it
        b.pack(side=RIGHT, fill=Y, expand=False)
        
        # create frames
        f = Frame(self.parent)
        self.tk_f.append(f)
        hd.start(f)
        f.pack(side=LEFT, fill=Y, expand=False)
        
        e.start(self.parent)
        
        # create UI done
    
    def _set_el(self):
        hd = self.p_hd
        e = self.p_e
        
        hd.callback = self._on_hd_entry
        e.callback = self._on_url_entry
        
        b = self.p_b
        b.bind('<Button-1>', self._on_button)
    
    # end PartTop class

# body part
class PartBody(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        # NOTE font and style should be set
        self.text_color = guis.main_text_conf['color']
        self.text_background_color = guis.main_text_conf['background_color']
        self.text_size = guis.main_text_size
        self.text_cursor_color = guis.main_text_conf['cursor_color']
        
        self.text_font = None
        
        self.text = None	# tk_base.TextBox
    
    # to send event list
    #	show_main_menu
    
    # operations
    
    def enable(self):
        self.text.enable()
    
    def disable(self):
        self.text.disable()
    
    def get_text(self, flag='selected'):
        return self.text.get_text(flag=flag)
    
    def add_text(self, text='', flag='end', style_type=None):
        # get tag name
        if style_type == None:
            tag_name = None
        else:
            # NOTE check has style_type
            style_list = guis.MAIN_TEXT_STYLE_TO_TAG_LIST
            if style_type in style_list:
                tag_name = style_list[style_type]
            else:
                tag_name = None
                # DEBUG info
                print('pvtkgui: gui2: ERROR: no tag_name in tag style list [' + str(style_type) + ']')
        # just add it
        self.text.add_text(text=text, flag=flag, tag=tag_name)
    
    def clear(self):
        self.text.clear()
    
    # on sub el
    
    def _on_text(self, event, data):
        # check event type
        if event == 'mouse_right':
            self._send('show_main_menu', data)
    
    def start(self, parent):
        # save parent
        self.parent = parent
        # create UI
        self._create()
        # set main text tag style
        guis.set_main_text_tag(self.text)
        # set el
        self._set_el()
        # done
    
    def _create(self):
        t = tk_base.TextBox()
        self.text = t
        # set t
        t.text_color = self.text_color
        t.text_background_color = self.text_background_color
        t.text_font = self.text_font
        t.text_size = self.text_size
        t.cursor_color = self.text_cursor_color
        
        # start pack
        t.start(self.parent)
        
        # create UI done
    
    def _set_el(self):
        t = self.text
        t.callback = self._on_text
    
    # end PartBody class

# footer part
class PartFooter(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        # NOTE font and style should be set
        self.label_font = None
        self.entry_font = None
        self.label_style = 'TLabel'
        self.entry_style = 'TEntry'
        self.button_style = 'TButton'
        
        self.entry = None	# tk_base.EntryBox
        self.button = None	# change Button
    
    # operations
    def get_text(self):
        return self.entry.get_text()
    
    def set_text(self, text=''):
        self.entry.set_text(text)
    
    # to send event list
    #	change		main button click
    
    # on sub el
    def _on_button(self, event=None):
        self._send('change', event)
    
    def start(self, parent):
        # save parent
        self.parent = parent
        # create UI
        self._create()
        # done
    
    def _create(self):
        # create UI
        e = tk_base.EntryBox()
        b = Button(self.parent, command=self._on_button, text=guis.ui_text['change'], style=self.button_style)
        self.entry = e
        self.button = b
        # set EntryBox
        e.label_text = guis.ui_text['xunlei_dl_dir']
        e.label_font = self.label_font
        e.entry_font = self.entry_font
        e.label_style = self.label_style
        e.entry_style = self.entry_style
        
        # pack button
        b.pack(side=RIGHT, fill=Y, expand=False)
        # pack entry
        e.start(self.parent)
        
        # create UI done
    
    def _set_el(self):
        pass	# nothing to do
    
    # end PartFooter class

# end gui2.py


