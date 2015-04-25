# -*- coding: utf-8 -*-
# base.py, part for parse_video
# base: base part of parse_video. 
# author sceext <sceext@foxmail.com> 2015.04 
# copyright 2015 sceext 
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : parse videos from many websites. 
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

# import modules
from . import child_process

# global config

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0'

CURL_BIN = 'curl'

# classes

# functions

# just make cget arg and return it
def _cget_make_arg(url, user_agent, referer):
    # check user_agent
    if user_agent == None:
        user_agent = USER_AGENT
    # do make it
    if referer != None:
        curl_args = [CURL_BIN, '--user-agent', user_agent, '--referer', referer, url]
    else:
        curl_args = [CURL_BIN, '--user-agent', user_agent, url]
    # done
    return curl_args

# cget, http get by curl
def cget(url, user_agent=USER_AGENT, referer=None):
    
    # make curl args
    curl_args = _cget_make_arg(url, user_agent, referer)
    # just call curl
    stdout, stderr = child_process.get_output(curl_args)
    
    # done
    return stdout

# use sub process pool to cget, cget many urls at the same time
def cget_pool(url_list, user_agent=None, referer=None, pool_size=4):
    
    # make args_list
    args_list = []
    for i in url_list:
        args = _cget_make_arg(i, user_agent, referer)
        args_list.append(args)
    # start pool
    tmp = child_process.get_output_pool(args_list, pool_size)
    # make stdout output
    output = []
    for i in tmp:
        output.append(i[0])
    # done
    return output

# end base.py


