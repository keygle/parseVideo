# call_sub.py, part for parse_video : a fork from parseVideo. 
# call_sub: o/pvtkgui/vlist: do call parse_video Tk GUI to parse URL. 
# version 0.0.1.0 test201506271458
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

import sys
import subprocess

# global vals

PVTKGUI_BIN = '1.pyw'

# function

def get_python_bin():
    # TODO may be not stable
    py_bin = sys.executable
    return py_bin

def call(url_to):
    py_bin = get_python_bin()
    # make args
    arg = [py_bin, PVTKGUI_BIN, '--url', url_to]
    # DEBUG info
    print('pvtkgui: DEBUG: vlist.call_sub: start with shell \"' + str(arg) + ' \"')
    
    # just run it
    p = subprocess.Popen(arg, shell=True)
    
    # done

# end call_sub.py


