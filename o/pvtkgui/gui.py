# gui.py, part for parse_video : a fork from parseVideo. 
# gui: o/pvtkgui/gui: parse_video Tk GUI, main gui file. 
# version 0.0.2.0 test201506061747
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
from tkinter.font import Font

# global vars

TEXT_MAIN_FONT_SIZE = 16	# 16px
MAIN_BUTTON_TEXT = 'Start prase'

# functions

# class

# main window

class MainWin(object):
    
    def __init__(self):
        self.root = None	# root window
        
        self.text_entry = None	# main Entry, input URL
        self.button = None	# main Button, start parse
        self.text_main = None	# main Text area, show text
        
        self.callback_main_button = None	# main button on click calback function
        
        pass
    
    # when main button be clicked, this will be callback
    def _main_button_on_click(self):
        pass
    
    # start create and show main window
    def start(self):
        # create root window
        root = Tk()
        self.root = root
        
        # create font
        f = Font(root, size=TEXT_MAIN_FONT_SIZE)
        
        # create frame
        f0 = Frame(root)	# top part, url text Entry and main Button
        f1 = Frame(root)	# bottom part, main Text and scrollbars
        f0.pack(side=TOP, fill=X, expand=False)
        f1.pack(side=BOTTOM, fill=BOTH, expand=True)
        
        # create top part
        # main button
        b = Button(f0, font=f, command=self._main_button_on_click, text=MAIN_BUTTON_TEXT)
        # main entry
        e = Entry(f0, font=f)
        # pack it
        b.pack(side=RIGHT, fill=NONE, expand=False)
        e.pack(side=LEFT, fill=X, expand=True)
        # save objs
        self.button = b
        self.text_entry = e
        
        # create bottom part
        # create scrollbar
        sx = Scrollbar(f1, orient=HORIZONTAL)
        sy = Scrollbar(f1, orient=VERTICAL)
        # main Text area
        t = Text(f1, wrap=NONE, font=f)
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
        
        # create main window done
    
    # start main loop
    def mainloop(self):
        # just start main loop
        mainloop()
    
    # end MainWin class

def test1():
    w = MainWin()
    w.start()
    w.mainloop()
    # test done

# start test
if __name__ == '__main__':
    test1()

# end gui.py


