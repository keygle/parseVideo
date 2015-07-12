# -*- coding: utf-8 -*-
# make_name.py, part for parse_video : a fork from parseVideo. 
# make_name:o/easy_dl/lib
# version 0.0.1.0 test201507011559
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

# function

def make_raw_name(pinfo):
    pi = pinfo['info']
    
    raw = {}
    
    raw['title'] = pi['title'] + '_' + pi['quality'] + '_' + pi['site_name']
    
    raw['ext'] = '.' + pi['format']
    
    # done
    return raw

def make_i_name(raw_info, i=0):
    n = raw_info['title'] + '_' + make_num_l(i) + raw_info['ext']
    return n

# base function

def make_num_l(n, l=4):
    t = str(n)
    while len(t) < l:
        t = '0' + t
    return t

# end make_name.py



