#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0debug_pvtkgui.py, for parse_video pvtkgui, parse_video Tk GUI

# import
import os
import sys

# add root path
raw_path = os.path.dirname(__file__)
raw_path = os.path.join(raw_path, '../../')

sys.path.append(raw_path)

from o.pvtkgui.b import gui

# functions
def test():
    # create main window
    w = gui.MainWin()
    
    w.start()
    
    # just start mainloop
    w.mainloop()
    
    # test done

# auto start debug
if __name__ == '__main__':
    test()

# end 0debug_pvtkgui.py


