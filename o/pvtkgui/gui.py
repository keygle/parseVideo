# gui.py, part for parse_video : a fork from parseVideo. 
# gui: o/pvtkgui/gui: parse_video Tk GUI, main gui file. 
# version 0.0.17.0 test201506072234
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
from tkinter.font import Font

# global vars

TEXT_MAIN_FONT_SIZE = 16	# 16px
MAIN_BUTTON_TEXT = '开始解析'
MAIN_WIN_TITLE = 'parse_video Tk GUI 1'
MAIN_FONT_NAME = '微软雅黑'
MENU_LABEL1 = '粘贴 URL'
MENU_LABEL2 = '复制全部 URL'
MENU_XUNLEI_DL_TEXT = '使用 迅雷 下载全部文件'

# functions

# class

# main window

class MainWin(object):
    
    def __init__(self):
        self.root = None	# root window
        
        self.text_entry = None	# main Entry, input URL
        self.button = None	# main Button, start parse
        self.text_main = None	# main Text area, show text
        
        self.text_entry_var = None
        self.hd_entry_var = None
        
        self.menu_url = None	# top part, url Entry menu
        self.menu_text = None	# body part, main Text menu
        
        self.callback_main_button = None	# main button on click calback function
        self.callback_copy_url = None
        self.callback_xunlei_dl = None
        
        # __init__ done
    
    # when main button be clicked, this will be callback
    def _main_button_on_click(self):
        # just call callback
        if self.callback_main_button != None:
            self.callback_main_button()
    
    # process main Entry key event
    def _on_return_key(self, event=None):
        # just callback as _main_button_on_click
        self._main_button_on_click()
    
    # press C key in main Text, to copy all URLs
    def _on_c_key(self, event=None):
        # DEBUG info
        print('DEBUG: _on_c_key F9')
        # just callback copy_url
        if self.callback_copy_url != None:
            self.callback_copy_url()
    
    # callback xunlei dl
    def _on_xunlei_dl(self):
        if self.callback_xunlei_dl != None:
            # DEBUG info
            print('DEBUG: try to start xunlei dl')
            
            self.callback_xunlei_dl()
    
    # press middle mouse botton, or click on paste menu in url Entry, to paste from clipboard
    def _on_url_entry_paste(self, event=None):
        # just paste from clipboard
        t = self.clip_get()
        # check type and null string
        if (type(t) == type('')) and (t != ''):
            self.set_entry_text(t)
        # DEBUG info
        print('DEBUG: _on_url_entry_paste')
    
    # hide menus
    def _hide_menus(self, event=None):
        self.menu_url.unpost()
        self.menu_text.unpost()
    
    # press mouse right button, to show paste menu in url Entry
    def _on_url_entry_menu(self, event=None):
        # hide menu before show
        self._hide_menus()
        # show menu
        m = self.menu_url
        m.post(event.x_root, event.y_root)
    
    # press mouse right button, to show copy urls menu is main Text
    def _on_main_text_menu(self, event=None):
        # hide menu before show
        self._hide_menus()
        # show menu
        m = self.menu_text
        m.post(event.x_root, event.y_root)
    
    # operation functions
    def get_entry_text(self):
        return self.text_entry_var.get()
    
    def set_entry_text(self, text):
        self.text_entry_var.set(text)
    
    def get_hd_text(self):
        return self.hd_entry_var.get()
    
    def set_hd_text(self, text):
        self.hd_entry_var.set(text)
    
    def get_main_text(self):
        return self.text_main.get(1.0, END)
    
    def clear_main_text(self):
        self.text_main.delete(1.0, END)
    
    def append_main_text(self, text=''):
        self.text_main.insert(END, text)
    
    def enable_main_text(self):
        self.text_main.config(state=NORMAL)
    
    def disable_main_text(self):
        self.text_main.config(state=DISABLED)
    
    def enable_main_button(self):
        self.button.config(state=NORMAL)
    
    def disable_main_button(self):
        self.button.config(state=DISABLED)
    
    # copy paste with clip board
    def clip_get(self):
        root = self.root
        try:
            t = root.clipboard_get()
        except Exception:
            t = None
        # done
        return t
    
    def clip_set(self, text):
        root = self.root
        root.clipboard_clear()
        root.clipboard_append(text)
    
    # start create and show main window
    def start(self):
        # create root window
        root = Tk()
        self.root = root
        # set main window title
        root.title(MAIN_WIN_TITLE)
        
        # create style for ttk
        style = Style()
        # set font
        style.configure('.', font=(MAIN_FONT_NAME, TEXT_MAIN_FONT_SIZE))
        style.configure('My.TEntry', padding=5)
        
        # create font for main Text and man Entry
        f = Font(root, size=TEXT_MAIN_FONT_SIZE)
        
        # create frame
        f0 = Frame(root)	# top part, url text Entry and main Button
        f1 = Frame(root)	# bottom part, main Text and scrollbars
        f0.pack(side=TOP, fill=X, expand=False)
        f1.pack(side=BOTTOM, fill=BOTH, expand=True)
        
        # create textvar for main Entry, and hd Entry
        v1 = StringVar()
        self.text_entry_var = v1
        v2 = StringVar()
        self.hd_entry_var = v2
        
        # create top part
        # main button
        b = Button(f0, command=self._main_button_on_click, text=MAIN_BUTTON_TEXT, style='TButton')
        # main entry
        e = Entry(f0, textvariable=v1, font=f, style='My.TEntry')
        # add Label and hd= support
        la = Label(f0, text='hd=', font=f)
        e2 = Entry(f0, textvariable=v2, font=f, style='My.TEntry', width=3)
        # pack it
        b.pack(side=RIGHT, fill=Y, expand=False)
        la.pack(side=LEFT, fill=Y, expand=False)
        e2.pack(side=LEFT, fill=Y, expand=False)
        e.pack(side=LEFT, fill=BOTH, expand=True)
        # save objs
        self.button = b
        self.text_entry = e
        
        # create menus
        m1 = Menu(root, tearoff=0)	# url Entry menu
        m2 = Menu(root, tearoff=0)	# main Text menu
        self.menu_url = m1
        self.menu_text = m2
        
        m1.add_command(label=MENU_LABEL1, command=self._on_url_entry_paste)
        m2.add_command(label=MENU_LABEL2, command=self._on_c_key)
        m2.add_command(label=MENU_XUNLEI_DL_TEXT, command=self._on_xunlei_dl)
        
        # set hide menus
        root.bind('<Button-1>', self._hide_menus)
        
        # bind key event for main Entry
        e.bind('<Return>', self._on_return_key)
        e2.bind('<Return>', self._on_return_key)
        # bind more event for main Entry
        e.bind('<Button-2>', self._on_url_entry_paste)	# mouse middle button, just paste url
        e.bind('<Button-3>', self._on_url_entry_menu)	# show url Entry menu, mouse right button
        
        # create bottom part
        # create scrollbar
        sx = Scrollbar(f1, orient=HORIZONTAL)
        sy = Scrollbar(f1, orient=VERTICAL)
        # main Text area
        t = Text(f1, wrap=NONE, font=f, padx=0, pady=0, relief=FLAT, bd=0, bg='#ddd', fg='#333')
        self.text_main = t
        # pack it
        sy.pack(side=RIGHT, fill=Y)
        sx.pack(side=BOTTOM, fill=X)
        t.pack(side=TOP, fill=BOTH, expand=True)
        # config Text and Scrollbar
        sx.config(command=t.xview)
        sy.config(command=t.yview)
        t.config(xscrollcommand=sx.set)
        t.config(yscrollcommand=sy.set)
        
        # bind more event to Text
        root.bind('<F9>', self._on_c_key)	# copy urls
        t.bind('<Button-3>', self._on_main_text_menu)	# show main Text menu
        
        # create main window done
    
    # start main loop
    def mainloop(self):
        # just start main loop
        mainloop()
    
    # end MainWin class

def debug1():
    t = w.get_entry_text()
    print('DEBUG: got entry text [' + t + ']')
    w.enable_main_text()
    w.append_main_text(t)
    w.disable_main_text()
    print('DEBUG: set main text')

def test1():
    global w
    w = MainWin()
    w.start()
    # set debug
    w.callback_main_button = debug1
    
    w.mainloop()
    # test done

# start test
if __name__ == '__main__':
    test1()

# end gui.py


