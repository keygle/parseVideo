# -*- coding: utf-8 -*-
# run_sub.py, part for parse_video : a fork from parseVideo. 
# run_sub: o/lieying_plugin/run_sub: call and run parsev as sub process. 
# version 0.0.5.0 test201506261338
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
import os

# global vars
BIN_PARSEV = '../../parsev'

# functions

def run_sub(arg, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

def run_pv(arg, flag_debug=False):
    # get python bin file and parsev path
    pybin = sys.executable
    if not flag_debug:
        pybin = try_pythonw_on_win(pybin)
    pvpath = make_bin_parsev_path()
    # make final arg
    farg = [pybin, pvpath]
    farg += arg
    # just run sub process
    return run_sub(farg)

# use pythonw.exe on windows instead of python.exe
def try_pythonw_on_win(pybin, check='python.exe', replace='pythonw.exe'):
    # check just 'python'
    if pybin == 'python':
        return 'pythonw'
    # check bin file path
    pybin_file = os.path.basename(pybin)
    pypath = os.path.dirname(pybin)
    # check python.exe
    if pybin_file == check:
        pybin_file = replace
    # make final path
    out = os.path.join(pypath, pybin_file)
    # check pythonw.exe exist
    if os.path.isfile(out):
        return out	# use pythonw.exe
    return pybin	# still use python.exe

def make_bin_parsev_path():
    now_file = os.path.abspath(__file__)
    now_dir = os.path.dirname(now_file)
    bin_file = os.path.join(now_dir, BIN_PARSEV)
    bin_file = os.path.normpath(bin_file)
    # done
    return bin_file

def run_one_pv(url, hd=None, i_min=None, i_max=None, flag_debug=False):
    # make args
    if hd == None:
        arg = ['--min', '1', '--max', '0']	# will output null result
    else:
        arg = ['--min', str(hd), '--max', str(hd)]	# only output this hd
    
    # add --min-i and --max-i
    if i_min != None:
        arg += ['--min-i', str(i_min)]
    if i_max != None:
        arg += ['--max-i', str(i_max)]
    
    # add fix ouput utf8
    arg += ['--fix-unicode']
    # add url
    arg += [url]
    # done, just run it
    return run_pv(arg, flag_debug=flag_debug)

# end run_sub.py


