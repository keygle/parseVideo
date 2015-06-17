# tk_base.py, part for parse_video : a fork from parseVideo. 
# tk_base: o/gui/tk_base: parse_video Tk GUI, tk base part. 
# version 0.0.7.0 test201506171550
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

# functions

def create_font(root, font_family=None, size=16, bold=False, italic=False, underline=False):
    # get font family
    ffamily = None
    if font_family != None:
        # get font list
        flist = TKfont.families(root)
        # check each font name
        for f in font_family:
            if f in flist:
                ffamily = f
                break
    # set default values
    font_weight = TKfont.NORMAL
    font_slant = TKfont.ROMAN
    font_underline = 0
    # check font flags
    if bold:
        font_weight = TKfont.BOLD
    if italic:
        font_slant = TKfont.ITALIC
    if underline:
        font_underline = 1
    # just create font
    if ffamily == None:
        font = TKfont.Font(root, size=size, weight=font_weight, slant=font_slant, underline=font_underline)
    else:
        font = TKfont.Font(root, size=size, family=ffamily, weight=font_weight, slant=font_slant, underline=font_underline)
    # done
    return font

# base class
class TkBaseObj(object):
    
    def __init__(self):
        self.parent = None
        
        self.callback = None
    
    def start(self, parent):
        pass
    
    # create tkinter UI obj
    def _create(self):
        pass
    
    # bind event, set callback
    def _set_el(self):
        pass
    
    def _send(self, event, data):
        if self.callback != None:
            self.callback(event, data)
    
    # end TkBaseObj class

# class

# EntryBox, Entry and text var, with a optional Label
class EntryBox(TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        # config vars
        self.label_text = None
        self.entry_width = None
        
        # tkinter obj
        self.tk_label = None
        self.tk_entry = None
        self.tk_textvar = None
        
        # NOTE font and style should be set
        self.label_font = None
        self.entry_font = None
        self.entry_style = 'TEntry'
        self.label_style = 'TLabel'
    
    def start(self, parent):
        # save parent
        self.parent = parent
        
        # create UI
        self._create()
        self._set_el()
        # done
    
    # operations
    def get_text(self):
        return self.tk_textvar.get()
    
    def set_text(self, text=''):
        self.tk_textvar.set(text)
    
    def set_entry_style(self, style='TEntry'):
        self.tk_entry.config(style=style)
    
    # event to send, event list
    #	key_enter	press Enter Key
    #	mouse_right	click right mouse button
    #	mouse_middle	click middle mouse button
    
    # on sub events
    def _on_key_enter(self, event=None):
        # just send it
        self._send('key_enter', event)
    
    def _on_mouse_right(self, event=None):
        self._send('mouse_right', event)
    
    def _on_mouse_middle(self, event=None):
        self._send('mouse_middle', event)
    
    # create UI with tkinter
    def _create(self):
        # create string var
        v = StringVar()
        self.tk_textvar = v
        
        # create Entry
        if self.entry_width != None:
            e = Entry(self.parent, textvariable=v, font=self.entry_font, style=self.entry_style, width=self.entry_width)
        else:
            e = Entry(self.parent, textvariable=v, font=self.entry_font, style=self.entry_style)
        self.tk_entry = e
        
        # check create Label
        if self.label_text != None:
            l = Label(self.parent, text=self.label_text, font=self.label_font, style=self.label_style)
            self.tk_label = l
        
        # pack obj
        flag_pack_entry = LEFT
        if self.tk_label != None:
            self.tk_label.pack(side=LEFT, fill=Y, expand=False)
            flag_pack_entry = RIGHT
        # check expand entry
        flag_expand_entry = True
        flag_fill_entry = BOTH
        if self.entry_width != None:
            flag_expand_entry = False
            flag_fill_entry = Y
        
        self.tk_entry.pack(side=flag_pack_entry, fill=flag_fill_entry, expand=flag_expand_entry)
        
        # create UI done
    
    def _set_el(self):
        # bind events
        e = self.tk_entry
        
        e.bind('<Return>', self._on_key_enter)
        e.bind('<Button-3>', self._on_mouse_right)
        e.bind('<Button-2>', self._on_mouse_middle)
        
        # done
    
    # end EntryBox class

# TextBox, Text and scrollbar
class TextBox(TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        # config vars
        self.text_color = '#333'
        self.text_background_color = '#999'
        self.text_size = [80, 24]
        self.cursor_color = '#f00'
        
        # NOTE font should be set
        self.text_font = None
        
        # tkinter obj
        self.tk_text = None	# Text
        self.tk_sx = None	# x scrollbar
        self.tk_sy = None	# y scrollbar
    
    def start(self, parent):
        # save parent
        self.parent = parent
        # create UI
        self._create()
        self._set_el()
    
    # operations
    
    # disable Text
    def disable(self):
        self.tk_text.config(state=DISABLED)
    
    # enable Text
    def enable(self):
        self.tk_text.config(state=NORMAL)
    
    # get text in Text
    # supported flag
    #	all		get all text
    #	selected	get selected text
    def get_text(self, flag='all'):
        text = None
        if flag == 'all':
            text = self.tk_text.get('1.0', END)
        elif flag == 'selected':
            text = self.tk_text.get(SEL_FIRST, SEL_LAST)
        # done
        return text
    
    # add text in Text
    # supported flag
    #	end	append text
    #	start	insert text before
    def add_text(self, text='', flag='end', tag=None):
        pos = END
        if flag == 'start':
            pos = '1.0'
        # just insert text
        self._insert_text(text, pos=pos, tag=tag)
    
    def _insert_text(self, text, pos=END, tag=None):
        # check tag
        if tag != None:
            self.tk_text.insert(pos, text, tag)
        else:
            self.tk_text.insert(pos, text)
        # insert text done
    
    # delete all text
    def clear(self):
        self.tk_text.delete('1.0', END)
    
    # set tag, set text style
    def set_tag_style(self, tag_name, style_list):
        t = self.tk_text
        # set each style
        l = style_list
        for s in l:
            if s == 'font':
                t.tag_config(tag_name, font=l[s])
            elif s == 'background_color':
                t.tag_config(tag_name, background=l[s])
            elif s == 'color':
                t.tag_config(tag_name, foreground=l[s])
            elif s == 'padding_top':
                t.tag_config(tag_name, spacing1=l[s])
            elif s == 'padding_bottom':
                t.tag_config(tag_name, spacing3=l[s])
            elif s == 'line_padding':
                t.tag_config(tag_name, spacing2=l[s])
            else:
                pass
        # done
    
    # event to send, event list
    #	mouse_right	click right mouse button
    
    # on sub el
    
    def _on_mouse_right(self, event=None):
        self._send('mouse_right', event)
    
    def _create(self):
        
        # create scrollbars
        sx = Scrollbar(self.parent, orient=HORIZONTAL)
        sy = Scrollbar(self.parent, orient=VERTICAL)
        self.tk_sx = sx
        self.tk_sy = sy
        
        # create Text
        t = Text(self.parent, 
            wrap=NONE, 
            font=self.text_font, 
            padx=0, 
            pady=0, 
            relief=FLAT, 
            bd=0, 
            bg=self.text_background_color, 
            fg=self.text_color, 
            width=self.text_size[0], 
            height=self.text_size[1], 
            insertbackground=self.cursor_color)
        self.tk_text = t
        
        # pack it
        sy.pack(side=RIGHT, fill=Y, expand=False)
        sx.pack(side=BOTTOM, fill=X, expand=False)
        t.pack(side=TOP, fill=BOTH, expand=True)
        
        # connect scrollbars and Text
        sx.config(command=t.xview)
        sy.config(command=t.yview)
        t.config(xscrollcommand=sx.set)
        t.config(yscrollcommand=sy.set)
        
        # done
    
    def _set_el(self):
        t = self.tk_text
        
        t.bind('<Button-3>', self._on_mouse_right)
    
    # end TextBox class

# end tk_base.py


