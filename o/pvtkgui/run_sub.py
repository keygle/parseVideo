# run_sub.py, part for parse_video : a fork from parseVideo. 
# run_sub: o/pvtkgui/run_sub: for parse_video Tk GUI, call and run parse_video. 
# version 0.0.3.0 test201506062105
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

# global vars

BIN_PARSE_VIDEO = 'parsev'

# functions

# run sub process
def run_sub(arg, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

# run parse_video
def run_pv(url):
    # get python bin file
    pybin = sys.executable
    # make args
    arg = [pybin, BIN_PARSE_VIDEO, '--output-easy', '--min', '10', url]
    # start parse_video
    stdout, stderr = run_sub(arg)
    # done
    return stdout, stderr

def sub_thread(callback, url):
    # FIXME debug info
    print('DEBUG: run parse_video sub_thread start')
    stdout, stderr = run_pv(url)
    print('DEBUG: run parse_video sub_thream end')
    callback(stdout, stderr)

# run parse_video in sub thread
def run_pv_thread(callback, url):
    # create thread
    t = threading.Thread(target=sub_thread, args=(callback, url))
    # just start it
    t.start()

# end run_sub.py


