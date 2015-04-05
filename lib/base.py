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

# classes

# functions

# cget, http get by curl
def cget(url, user_agent=USER_AGENT, referer=None):
    
    # make curl args
    if referer != None:
        curl_args = ['curl', '--user-agent', user_agent, '--referer', referer, url]
    else:
        curl_args = ['curl', '--user-agent', user_agent, url]
    # just call curl
    stdout, stderr = child_process.get_output(curl_args)
    
    # done
    return stdout


# end base.py


