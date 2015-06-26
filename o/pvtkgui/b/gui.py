# gui.py, part for parse_video : a fork from parseVideo. 
# gui: o/pvtkgui/gui: parse_video Tk GUI, main window gui. 
# version 0.2.11.0 test201506270110
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
import tkinter.filedialog as TKfile

from . import gui_style as guis
from ...gui import tk_base
from . import gui2
from ...easy import set_key

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
        
        self.p_m = None	# MenuHost part
        self.p_b_host = None	# ButtonHost part
        
        self.s_h = None	# SelectHost
        
        # footer show flag
        self.flag_footer_show = False
    
    # operations
    
    def get_hd_text(self):
        return self.p_top.get_hd_text()
    
    def set_hd_text(self, text=''):
        self.p_top.set_hd_text(text=text)
    
    def get_url_text(self):
        return self.p_top.get_url_text()
    
    def set_url_text(self, text=''):
        self.p_top.set_url_text(text=text)
    
    def set_button_status(self, status='start'):
        if status == 'stop':
            self.p_top.set_button_style('Red.Button.TLabel')
            self.p_top.set_button_text(guis.ui_text['stop_analyse'])
        else:	# set as start
            self.p_top.set_button_style('Blue.Button.TLabel')
            self.p_top.set_button_text(guis.ui_text['start_analyse'])
        # set button status done
    
    def set_url_status(self, status='none'):
        if status == 'ok':
            # set red style
            self.p_top.set_url_text_style('Red.TEntry')
        else:	# set as none normal status
            self.p_top.set_url_text_style('Main.TEntry')
        # set url status done
    
    def disable_main_text(self):
        self.p_body.disable()
    
    def enable_main_text(self):
        self.p_body.enable()
    
    def clear_main_text(self):
        self.p_body.clear()
    
    def get_main_text(self, flag='selected'):
        return self.p_body.get_text(flag=flag)
    
    def add_main_text(self, text='', flag='end', tag=None):
        self.p_body.add_text(text=text, flag=flag, style_type=tag)
    
    # SelectHost operation
    def sh_reset(self):
        self.s_h.reset()
    
    def sh_add_item(self):
        b = self.s_h.add_item()
        # just add it to Text
        self.p_body.add_obj(b)
    
    def sh_get_list(self):
        return self.s_h.get_list()
    
    # ButtonHost operation
    def bh_add_item(self, text='', data=None):
        # create one button
        b = self.p_b_host.create_one(text=text, data=data)
        # add it to main text
        self.p_body.add_obj(b)
        # done
    
    # part footer, xunlei dl path
    def get_xunlei_path_text(self):
        return self.p_footer.get_text()
    
    def set_xunlei_path_text(self, text=''):
        self.p_footer.set_text(text=text)
    
    def get_ui_type(self):
        return self.p_m.get_ui_type()
    
    def set_ui_type(self, text=''):
        self.p_m.set_ui_type(text)
    
    def get_select_each(self):
        return self.p_m.get_select_each()
    
    def set_select_each(self, flag=False):
        self.p_m.set_select_each(flag)
    
    def hide_footer(self):
        f = self.tk_f[1]
        f.pack_forget()
        self.flag_footer_show = False
    
    def show_footer(self):
        # check flag
        if self.flag_footer_show:
            return
        
        # show footer
        f = self.tk_f[1]
        f.pack(side=BOTTOM, fill=X, expand=False)
        self.flag_footer_show = True
    
    # select_each menu items
    def disable_select_each(self):
        self.p_m.disable_select_each()
    
    def enable_select_each(self):
        self.p_m.enable_select_each()
    
    # clipboard operations
    def clip_get(self):
        root = self.root
        try:
            t = root.clipboard_get()
        except Exception:
            t = None
        # check t is text
        if type(t) != type(''):
            t = None
        return t
    
    def clip_set(self, text=''):
        root = self.root
        root.clipboard_clear()
        root.clipboard_append(text)
    
    # select dir window
    def select_dir(self, old_path=None, title=''):
        result = TKfile.askdirectory(parent=self.root, title=title, initialdir=old_path)
        if (type(result) == type('')) and (result != ''):
            return result
        return None
    
    # event to send, event list
    #	start_stop	top part, start_stop button
    #
    #	xunlei_dl_path_change	footer part, change xunlei dl path button
    #
    #	top_paste	top part, paste URL
    #	top_copy
    #
    #	body_copy_selected
    #	body_copy_all_url
    #
    #	xunlei_dl_all_url
    #	xunlei_dl_rest_url
    #
    #	xunlei_dl_select_url
    #	copy_select_url
    #
    #	button_host
    
    def _send(self, event, data):
        # DEBUG info
        print('pvtkgui: gui: MainWin send event [' + str(event) + '] ' + str(data))
        # use super to send
        super()._send(event, data)
    
    # on sub el
    
    def _on_hide_menu(self, event=None):
        # just hide menu
        self.p_m.hide()
    
    def _on_part_top(self, event, data):
        if event == 'start_stop':
            # just send it
            self._send('start_stop', data)
        elif event == 'show_menu':
            # show top menu
            self.p_m.show('top', data)
        elif event == 'paste':
            self._send('top_paste', data)
        # process sub event done
    
    def _on_part_body(self, event, data):
        if event == 'show_main_menu':
            # show body part menu
            self.p_m.show('body', data)
        # process sub event done
    
    def _on_part_footer(self, event, data):
        if event == 'change':
            self._send('xunlei_dl_path_change', data)
        # process sub event done
    
    def _on_part_menu(self, event, data):
        if event == 'paste_url':
            self._send('top_paste', data)
        elif event == 'copy_url':
            self._send('top_copy', data)
        
        elif event == 'copy_selected':
            self._send('body_copy_selected', data)
        elif event == 'copy_all_url':
            self._send('body_copy_all_url', data)
        
        elif event == 'xunlei_dl_all_url':
            self._send('xunlei_dl_all_url', data)
        elif event == 'xunlei_dl_rest_url':
            self._send('xunlei_dl_rest_url', data)
        
        elif event == 'xunlei_dl_select_url':
            self._send('xunlei_dl_select_url', data)
        elif event == 'copy_select_url':
            self._send('copy_select_url', data)
        
        elif event == 'change_ui_type':
            self._send('change_ui_type', data)
        elif event == 'change_select_each':
            self._send('change_select_each', data)
        # process sub event done
    
    def _on_key_copy(self, event=None):
        self._send('body_copy_all_url', event)
    
    def _on_key_paste(self, event=None):
        self._send('top_paste', event)
    
    def _on_key_start_parse(self, event=None):
        self._send('start_stop', event)
    
    def _on_button_host(self, data=None, event=None):
        self._send('button_host', data)
    
    # start main loop
    def mainloop(self):
        # just start main loop
        mainloop()
    
    # create main UI
    def start(self):
        # create UI
        self._create()
        self._set_el()
    
    def _create(self):
        # create root window
        root = tix.Tk()
        self.root = root
        
        # create sub part
        top = gui2.PartTop()
        self.p_top = top
        body = gui2.PartBody()
        self.p_body = body
        footer = gui2.PartFooter()
        self.p_footer = footer
        
        # create main font
        main_font, main_font_bold, main_big_font_bold = guis.create_main_font(root)
        # set main style
        guis.set_ttk_style()
        
        # set sub styles
        top.hd_font = main_font
        top.hd_entry_font = main_big_font_bold
        top.entry_font = main_font_bold
        
        body.text_font = main_font
        
        footer.label_font = main_font
        footer.entry_font = main_font
        
        # create frames, and pack each part
        f = Frame(root)
        self.tk_f.append(f)
        top.start(f)
        f.pack(side=TOP, fill=X, expand=False)
        
        f = Frame(root)
        self.tk_f.append(f)
        footer.start(f)
        # NOTE not show footer here
        
        f = Frame(root)
        self.tk_f.append(f)
        body.start(f)
        f.pack(side=TOP, fill=BOTH, expand=True, padx=(0, 0))
        
        # create MenuHost
        m = MenuHost()
        self.p_m = m
        m.start(root)
        
        # set main window title
        root.title(guis.ui_text['main_win_title'])
        
        # create SelectHost
        s_h = gui2.SelectHost()
        self.s_h = s_h
        
        # set parent, NOTE get Text parent here
        s_h.parent = self.p_body.text.tk_text
        # init reset it
        s_h.reset()
        # create SelectHost done
        
        # create ButtonHost
        p_b_host = gui2.ButtonHost()
        self.p_b_host = p_b_host
        # set it
        p_b_host.parent = s_h.parent
        p_b_host.callback = self._on_button_host
        
        # create UI done
    
    def _set_el(self):
        root = self.root
        top = self.p_top
        body = self.p_body
        footer = self.p_footer
        m = self.p_m
        # add callback for sub part
        top.callback = self._on_part_top
        body.callback = self._on_part_body
        footer.callback = self._on_part_footer
        m.callback = self._on_part_menu
        
        # add callback for hide menu
        root.bind('<Button-1>', self._on_hide_menu)
        
        # set keys to bind events
        root.bind(set_key.KEY_COPY_URLS, self._on_key_copy)
        root.bind(set_key.KEY_PASTE_URL, self._on_key_paste)
        root.bind(set_key.KEY_START_PARSE, self._on_key_start_parse)
        
        # for ESC key to stop parse
        root.bind('<Escape>', self._on_key_start_parse)
        
        # set el done
    
    # end MainWin class

# menu host, show menus
class MenuHost(tk_base.TkBaseObj):
    
    def __init__(self):
        super().__init__()
        
        self.m1 = None	# top menu
        self.m2 = None	# body menu
        self.m3 = None	# sub menu of body
        
        self.v_ui_type = None		# stringvar ui_type
        self.v_select_each = None	# stringvar select_each
        
        self.select_each_index = []	# menu index of select_each menu items
    
    def start(self, parent):
        # save parent
        self.parent = parent
        # create menu
        self._create()
        # create UI done
    
    # event to send, event list
    #	paste_url	top entry paste url
    #	copy_url	top entry copy url
    #
    #	copy_selected	body text, copy selected text
    #	copy_all_url
    #	xunlei_dl_all_url
    #	xunlei_dl_rest_url
    #
    #	xunlei_dl_select_url
    #	copy_select_url
    #
    #	change_ui_type
    #	change_select_each
    
    # on sub el
    
    def _on_paste_url(self, event=None):
        # just send event
        self._send('paste_url', event)
    
    def _on_copy_url(self, event=None):
        self._send('copy_url', event)
    
    def _on_copy_selected(self, event=None):
        self._send('copy_selected', event)
    
    def _on_copy_all_url(self, event=None):
        self._send('copy_all_url', event)
    
    def _on_xunlei_dl_all_url(self, event=None):
        self._send('xunlei_dl_all_url', event)
    
    def _on_xunlei_dl_rest_url(self, event=None):
        self._send('xunlei_dl_rest_url', event)
    
    def _on_xunlei_dl_select_url(self, event=None):
        self._send('xunlei_dl_select_url', event)
    
    def _on_copy_select_url(self, event=None):
        self._send('copy_select_url', event)
    
    def _on_change_ui_type(self, event=None):
        self._send('change_ui_type', event)
    
    def _on_change_select_each(self, event=None):
        self._send('change_select_each', event)
    
    # get ui_type
    def get_ui_type(self):
        return self.v_ui_type.get()
    
    def set_ui_type(self, text=''):
        self.v_ui_type.set(text)
    
    def get_select_each(self):
        raw = self.v_select_each.get()
        if raw == '1':
            return True
        else:
            return False
    
    def set_select_each(self, flag=False):
        raw = '0'
        if flag:
            raw = '1'
        self.v_select_each.set(raw)
    
    def disable_select_each(self):
        ilist = self.select_each_index
        m = self.m2
        for i in ilist:
            m.entryconfig(i, state=DISABLED)
    
    def enable_select_each(self):
        ilist = self.select_each_index
        m = self.m2
        for i in ilist:
            m.entryconfig(i, state=NORMAL)
    
    # hide all menus
    def hide(self):
        self.m1.unpost()
        self.m2.unpost()
    
    # show one menu
    # supported menu type list
    #	entry	top part entry menu
    #	main	body part, text menu
    def show(self, menu_type, event):
        # hide menu first
        self.hide()
        # check which menu
        if menu_type == 'top':
            # show top menu
            m = self.m1
        elif menu_type == 'body':
            # show body menu
            m = self.m2
        else:
            raise Exception('menu type error')
        # show menu
        m.post(event.x_root, event.y_root)
        # show menu done
    
    def _create(self):
        m1 = Menu(self.parent, tearoff=0)
        m2 = Menu(self.parent, tearoff=0)
        m3 = Menu(m2, tearoff=0)
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        
        m1t = guis.ui_top_menu	# menu 1 text
        m2t = guis.ui_body_menu
        m3t = guis.ui_body_menu2
        
        # add command
        m1.add_command(label=m1t['paste_url'], command=self._on_paste_url)
        m1.add_command(label=m1t['copy_url'], command=self._on_copy_url)
        
        m2.add_command(label=m2t['copy_selected'], command=self._on_copy_selected)
        m2.add_command(label=m2t['copy_all_url'], command=self._on_copy_all_url)
        m2.add_separator()
        m2.add_command(label=m2t['xunlei_dl_all_url'], command=self._on_xunlei_dl_all_url)
        m2.add_command(label=m2t['xunlei_dl_rest_url'], command=self._on_xunlei_dl_rest_url)
        
        m2.add_separator()
        m2.add_command(label=m2t['xunlei_dl_select_url'], command=self._on_xunlei_dl_select_url)
        m2.add_command(label=m2t['copy_select_url'], command=self._on_copy_select_url)
        # NOTE add select_each item index
        self.select_each_index += [6, 7]	# NOTE fix BUG here
        
        m2.add_separator()
        m2.add_cascade(menu=m3, label=m2t['conf'])
        
        # create StringVar
        v1 = StringVar(self.parent)
        self.v_ui_type = v1
        v2 = StringVar(self.parent)
        self.v_select_each = v2
        
        # create sub menu
        m3.add_radiobutton(label=m3t['full_ui'], variable=v1, value='full_ui', command=self._on_change_ui_type)
        m3.add_radiobutton(label=m3t['simple_ui'], variable=v1, value='simple_ui', command=self._on_change_ui_type)
        m3.add_separator()
        m3.add_checkbutton(label=m3t['select_each'], variable=v2, command=self._on_change_select_each)
        
        # create menu done
    
    # end MenuHost class

# end gui.py


