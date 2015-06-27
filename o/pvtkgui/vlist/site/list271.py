# -*- coding: utf-8 -*-
# list271.py, part for parse_video : a fork from parseVideo. 
# list271: o/pvtkgui/vlist/site: support video list for 271 for parse_video Tk GUI. 
# version 0.0.2.0 test201506270040
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

# NOTE should be set
htmldom = None	# python htmldom parse html module

# global vars

# functions

def get_list_info(raw_html_text):
    # parse html_text with htmldom
    dom = htmldom.HtmlDom()
    root = dom.createDom(raw_html_text)
    
    # get block
    blocks = root.find('ul.site-piclist[data-albumlist-elem=cont]')
    block = blocks[0]
    
    # get some list
    a_list = block.find('a.site-piclist_pic_link')
    url_list = []
    title_list = []
    for a in a_list:
        url_list.append(a.attr('href'))
        title_list.append(a.attr('title'))
    
    ns = block.find('p.site-piclist_info_title>a')
    
    # NOTE fix ns here
    ns = ns[::2]
    
    n_list = []
    for n in ns:
        n_list.append(n.text())
    
    # make output info obj
    info = []
    for i in range(len(url_list)):
        one = {}
        info.append(one)
        
        one['url'] = url_list[i]
        one['title'] = title_list[i]
        one['n'] = n_list[i]
    
    # done
    return info

# end list271.py


