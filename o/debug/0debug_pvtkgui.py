#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 0debug_pvtkgui.py, for parse_video pvtkgui, parse_video Tk GUI

# import

import sys
sys.path.append('.')

from o.pvtkgui import gui

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


