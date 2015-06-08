# gui.py, part for parse_video : a fork from parseVideo. 
# gui: o/ffmpeg_tkgui/gui: parse_video Tk GUI, main gui file. 
# version 0.0.1.0 test201506081747
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
MAIN_WIN_TITLE = 'parse_video Tk GUI 1'
MAIN_FONT_NAME = '微软雅黑'

# functions

# class

# main window

class MainWin(object):
    
    def __init__(self):
        self.root = None	# root window
        
        # TODO
        
        # __init__ done
    
    # start create and show main window
    def start(self):
        # create root window
        root = Tk()
        self.root = root
        # set main window title
        root.title(MAIN_WIN_TITLE)
        
        # TODO
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
        # create main window done
    
    # start main loop
    def mainloop(self):
        # just start main loop
        mainloop()
    
    # end MainWin class

# end gui.py


