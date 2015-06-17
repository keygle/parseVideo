# gui.py, part for parse_video : a fork from parseVideo. 
# gui: o/pvtkgui/gui: parse_video Tk GUI, main window gui. 
# version 0.1.1.0 test201506171340
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
from ..gui import tk_base

# global vars

# functions

# class

# main window
class MainWin(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        self.root = None	# root window
        
        self.p_top = None	# top part
        self.p_body = None	# body part
        self.p_footer = None	# footer part
        
        self.tk_f = []	# TK frames, used as part parent
        
        # TODO
        pass
    
    # event to send, event list
    #	TODO
    
    # on sub el
    # def _on # TODO
    
    # operations
    
    # start main loop
    def mainloop(self):
        # just start main loop
        mainloop()
    
    # create main UI
    def start(self):
        # create font and set sytles
        # TODO
        # create UI
        self._create()
        self._set_ul()
        # TODO
    
    def _create(self):
        # create root window
        root = tix.Tk()
        self.root = root
        
        # create sub part
        top = PartTop()
        self.p_top = top
        body = PartBody()
        self.p_body = body
        footer = PartFooter()
        self.p_footer = footer
        
        # set sub styles
        # TODO
        
        # create frames, and pack each part
        f = Frame(root)
        self.tk_f.append(f)
        top.start(f)
        f.pack(side=TOP, fill=X, expand=False)
        
        f = Frame(root)
        self.tk_f.append(f)
        footer.start(f)
        f.pack(side=BOTTOM, fill=X, expand=False)
        
        f = Frame(root)
        self.tk_f.append(f)
        body.start(f)
        f.pack(side=TOP, fill=BOTH, expand=True)
        
        # create UI done
    
    def _set_el(self):
        pass
    
    # end MainWin class

# menu host, show menus
class MenuHost(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        # TODO
    
    # event to send, event list
    #	TODO
    
    # hide all menus
    def hide(self):
        pass
    
    # show one menu
    # supported menu type list
    #	entry	top part entry menu
    #	main	body part, text menu
    def show(self, menu_type):
        pass
    
    # end MenuHost class

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
        
        # TODO
    
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
    
    def start(self, parent):
        # save parent
        self.parent = parent
        # create UI
        self._create()
        self._set_el()
        # TODO
    
    def _create(self):
        hd = tk_base.EntryBox()
        self.p_hd = hd
        e = tk_base.EntryBox()
        self.p_e = e
        b = Button(self.parent, command=self._on_button, text=guis.ui_text['start_analyse'], style=self.button_style)
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
        hd.start(self.parent)
        e.start(self.parent)
        
        # create UI done
    
    def _set_el(self):
        pass	# TODO
    
    # end PartTop class

# body part
class PartBody(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        # NOTE font and style should be set
        self.text_color = guis.main_text_conf['color']
        self.text_background_color = guis.main_text_conf['background_color']
        
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
        tag_name = guis.MAIN_TEXT_STYLE_TO_TAG_LIST[style_type]
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
        # done
    
    def _create(self):
        t = tk_base.TextBox()
        self.text = t
        # set t
        t.text_color = self.text_color
        t.text_background_color = self.text_background_color
        t.text_font = self.text_font
        
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

# end gui.py


