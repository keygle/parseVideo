# gui.py, part for parse_video : a fork from parseVideo. 
# gui: o/pvtkgui/gui: parse_video Tk GUI, main gui file. 
# version 0.0.1.0 test201506061728
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

# functions

def test1():
    root = Tk()
    
    f = Font(root, size=16)
    
    sx = Scrollbar(root, orient=HORIZONTAL)
    sy = Scrollbar(root, orient=VERTICAL)
    t = Text(root, wrap='none', font=f)
    
    sy.pack(side=RIGHT, fill=Y)
    sx.pack(side=BOTTOM, fill=X)
    t.pack(side=TOP, fill=BOTH, expand=True)
    
    sx.config(command=t.xview)
    sy.config(command=t.yview)
    t.config(xscrollcommand=sx.set)
    t.config(yscrollcommand=sy.set)
    
    mainloop()
    
    pass

# start test
if __name__ == '__main__':
    test1()

# end gui.py


