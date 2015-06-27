# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/vlist: support video list for pvtkgui. 
# version 0.0.1.0 test201506271353
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

import re

from urllib import request

from . import make_easy_text
from . import call_sub

from .site import list271

from ..b import conf_default as confd

from ...tool.parse_html import htmldom

# global vars

SUPPORTED_LIST_URL_RE = [
    '^http://www.iqiyi.com/a_.+\.html', 	# for 271
]

URL_TO_SITE_LIST = {
    '^http://www.iqiyi.com/a_.+\.html' : list271, 
}

# base functions

def http_get(url):
    
    # make header
    header = {}
    header['Connection'] = 'close'
    
    req = request.Request(url, headers=header)
    res = request.urlopen(req)
    
    data = res.read()
    # just decode as utf-8
    t = data.decode('utf-8', 'ignore')
    # done
    return t

def get_site_module(url):
    m = None
    ulist = URL_TO_SITE_LIST
    for r in ulist:
        if re.match(r, url):
            m = ulist[r]
            break
    # done
    return m

# function

# check a input url is a list url
def check_is_list_url(url):
    rlist = SUPPORTED_LIST_URL_RE
    for r in rlist:
        if re.match(r, url):
            return True
    return False

# do parse video list
def parse_video_list(url):
    
    # DEBUG info
    print('pvtkgui: DEBUG: vlist.entry: load page \"' + url + '\"')
    
    # load html
    html_text = http_get(url)
    
    list_entry = get_site_module(url)
    # set import first
    list_entry.htmldom = htmldom
    
    # DEBUG info
    print('pvtkgui: DEBUG: vlist.entry: parse info')
    
    # parse html and get info
    info = list_entry.get_list_info(html_text)
    
    # done
    return info

# on parse video list done, update main window
def update_main_win(info, w):
    
    # DEBUG info
    print('pvtkgui: DEBUG: vlist.entry: start update main win text')
    
    # make output_style
    t = make_easy_text.output_style(info)
    
    # do update main window
    w.enable_main_text()
    w.clear_main_text()
    
    # add main text
    button_text = confd.ui_text['vlist_button_text']
    
    # add each item
    data_i = 0
    for item in t:
        # check tag
        tag = item[0]
        if tag == 'video_list_item_button':
            # add space before
            w.add_main_text(text=' ', tag=None)
            # add button
            w.bh_add_item(text=button_text, data=data_i)
            data_i += 1	# NOTE update data_i
            # add space after
            w.add_main_text(text=' ', tag=None)
        else:	# add as normal
            w.add_main_text(text=item[1], tag=tag)
    # add main text done
    print('pvtkgui: DEBUG: vlist.entry: update main win text done')

# on main text button clicked
def on_sub_button(data=None):
    pass

# end entry.py



