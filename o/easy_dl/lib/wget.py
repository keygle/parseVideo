# -*- coding: utf-8 -*-
# wget.py, part for parse_video : a fork from parseVideo. 
# wget:o/easy_dl/lib
# version 0.0.1.0 test201507011511
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.07. 
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

import subprocess

# global vars

etc = {}

etc['bin_wget'] = 'wget'
etc['flag_debug'] = False

# function

# wget entry function
def dl(url, out_file):
    arg = make_wget_arg(url, out_file)
    
    # DEBUG info
    if etc['flag_debug']:
        print('easy_dl: DEBUG: start wget with ' + str(arg) + ' ')
    
    exit_code = run_sub(arg)
    
    # DEBUG info
    if etc['flag_debug']:
        print('easy_dl: DEBUG: wget exit_code ' + str(exit_code) + ' ')
    
    return exit_code

# base function

def run_sub(arg, shell=False):
    p = subprocess.Popen(arg, shell=shell)
    exit_code = p.wait()
    
    return exit_code

def make_wget_arg(url, out_file):
    arg = []
    
    arg += ['-c', '-O', out_file, url]
    arg = [etc['bin_wget']] + arg
    
    return arg

# end wget.py



