# run_sub.py, part for parse_video : a fork from parseVideo. 
# run_sub: o/pvtkgui/run_sub: for parse_video Tk GUI, call and run parse_video. 
# version 0.1.8.0 test201506281302
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

from .. import support_evparse

from ..vlist import entry as vlist

from ...easy import set_flag_v

# global vars

BIN_PARSE_VIDEO = 'parsev'

sub_process_parsev_obj = None

# functions

# run sub process
def run_sub(arg, shell=False, save_callback=None):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # check save p callback
    if save_callback != None:
        save_callback(p)
    # just start subprocess
    return p.communicate()

# save parsev p obj, for terminate sub process
def save_parsev_p(p):
    global sub_process_parsev_obj
    sub_process_parsev_obj = p

# terminate parsev
def terminate_parsev():
    p = sub_process_parsev_obj
    if p == None:
        return True
    # just terminate it
    p.terminate()

# run parse_video
def run_pv(url, hd, flag_debug=False):
    # get python bin file
    pybin = sys.executable
    
    # check support evparse
    if support_evparse.check_support_evp(url):
        # make evp args
        arg = support_evparse.get_evp_arg(url, hd=hd, flag_debug=flag_debug)
        # add py bin
        arg = [pybin] + arg
    else:	# use parse_video
        # make args
        hd = str(hd)
        
        arg = ['--fix-unicode', '--fix-size', '--min', hd, '--max', hd]
        # check flag_debug
        if flag_debug:
            arg += ['--debug']
        
        if set_flag_v.set_flag_v:
            arg += ['--set-flag-v']
        
        arg = [pybin, BIN_PARSE_VIDEO] + arg + [url]
    # make args done
    
    # DEBUG info
    arg_text = json.dumps(arg)
    print('pvtkgui: run_sub: start parsev with args ' + arg_text)
    # start parse_video
    stdout, stderr = run_sub(arg, save_callback=save_parsev_p)
    # clean saved p
    save_parsev_p(None)
    # done
    return stdout, stderr

def sub_thread(callback, url, hd, write_config=None, flag_debug=False, w=None):
    # DEBUG info
    print('pvtkgui: run_sub: run parse_video sub_thread start')
    # write config file first
    if write_config != None:
        write_config()
    
    # check vlist
    if vlist.check_is_list_url(url):
        # parse as vlist
        info = vlist.parse_video_list(url)
        # update main window
        vlist.update_main_win(info, w)
        
        # with flag_only
        callback(None, None, flag_only=True)
        # done
        return
    
    # start parsev
    stdout, stderr = run_pv(url, hd, flag_debug=flag_debug)
    # DEBUG info
    print('pvtkgui: run_sub: run parse_video sub_thread end')
    callback(stdout, stderr)

# run parse_video in sub thread
def run_pv_thread(callback, url, hd, write_config=None, flag_debug=False, w=None):
    # just start it
    start_thread(sub_thread, arg=(callback, url, hd, write_config, flag_debug, w))

# start thread
def start_thread(target, arg=(), daemon=True):
    t = threading.Thread(target=target, args=arg, daemon=daemon)
    t.start()

# end run_sub.py


