# make_easy_text.py, part for parse_video : a fork from parseVideo. 
# make_easy_text: o/pvtkgui/vlist: make easy_text for pvtkgui support video list. 
# version 0.0.1.0 test201506270123
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

from ...output import easy_text

# global vars

# functions

def output_style(info):
    
    t = []	# output text
    l = []	# one line text
    
    t += [[None, '\n\n']]
    
    item_i = 0
    # add each item
    for one in info:
        l = []
        
        # add item_i
        item_i += 1
        l += [[None, easy_text.make_num_len(item_i)]]
        
        # add button
        l += [['video_list_item_button', '']]
        
        # add n
        l += [['big_red', one['n']], [None, '	']]
        
        # add title
        l += [['bold', one['title']], [None, '		']]
        
        # add url
        l += [['a', one['url']]]
        
        # add one line done
        t += l + [[None, '\n']]
    
    # done
    t += [[None, '\n']]
    return t

# end make_easy_text.py


