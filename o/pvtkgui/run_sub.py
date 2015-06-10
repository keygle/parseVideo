# run_sub.py, part for parse_video : a fork from parseVideo. 
# run_sub: o/pvtkgui/run_sub: for parse_video Tk GUI, call and run parse_video. 
# version 0.1.2.0 test201506102133
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
import threading
import json

# global vars

BIN_PARSE_VIDEO = 'parsev'

# functions

# run sub process
def run_sub(arg, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

# run parse_video
def run_pv(url, hd, flag_debug=False):
    # get python bin file
    pybin = sys.executable
    # make args
    hd = str(hd)
    arg = [pybin, BIN_PARSE_VIDEO, '--force-output-utf8', '--min', hd, '--max', hd, url]
    # check flag_debug
    if flag_debug:
        arg.append('--debug')
    # DEBUG info
    arg_text = json.dumps(arg)
    print('DEBUG: run_sub: start parsev with args ' + arg_text)
    # start parse_video
    stdout, stderr = run_sub(arg)
    # done
    return stdout, stderr

def sub_thread(callback, url, hd, write_config=None, flag_debug=False):
    # DEBUG info
    print('DEBUG: run parse_video sub_thread start')
    # write config file first
    if write_config != None:
        write_config()
    # start parsev
    stdout, stderr = run_pv(url, hd, flag_debug=flag_debug)
    # DEBUG info
    print('DEBUG: run parse_video sub_thream end')
    callback(stdout, stderr)

# run parse_video in sub thread
def run_pv_thread(callback, url, hd, write_config=None, flag_debug=False):
    # just start it
    start_thread(sub_thread, arg=(callback, url, hd, write_config, flag_debug))

# start thread
def start_thread(target, arg=(), daemon=True):
    t = threading.Thread(target=target, args=arg, daemon=daemon)
    t.start()

# end run_sub.py


