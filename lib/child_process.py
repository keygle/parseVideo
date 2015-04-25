# -*- coding: utf-8 -*-
# child_process.py, part for evdh : EisF Video Download Helper, sceext <sceext@foxmail.com> 2009EisF2015, 2015.04 
# child_process: like child_process module in node.js, used to create child processes. 
# version 0.0.5.0 test201504251437 (public version)
# author sceext <sceext@foxmail.com> 2015.04 
# copyright 2015 sceext 
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    evdh : EisF Video Download Helper, auto download videos on web pages. 
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

# require import modules
import subprocess
import multiprocessing

# functions

def run(args, shell=False):
    
    exit_code = subprocess.call(args, shell=shell);
    return exit_code

def get_output(args, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(args, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

# use multiprocessing, run many process at the same time
def get_output_pool(args_list, pool_size=4):
    
    pool = multiprocessing.Pool(processes=pool_size, initializer=pool_start_process)
    pool_output = pool.map(pool_do_sub, args_list)
    
    pool.close()
    pool.join()
    
    # done
    return pool_output

def pool_do_sub(args):
    out = get_output(args)
    return out

def pool_start_process():	# for debug
    pass

# end child_process.py


