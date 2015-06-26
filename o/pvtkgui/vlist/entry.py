# entry.py, part for parse_video : a fork from parseVideo. 
# entry: o/pvtkgui/vlist: support video list for pvtkgui. 
# version 0.0.0.2 test201506270133
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

# global vars

SUPPORTED_LIST_URL_RE = [
    '^http://www.iqiyi.com/a_.+\.html', 	# for 271
]

URL_TO_SITE_LIST = {
    '^http://www.iqiyi.com/a_.+\.html' : list271, 
}

# base functions

def http_get(url):
    pass

def get_site_module(url):
    pass

# function

# check a input url is a list url
def check_is_list_url(url):
    pass

# do parse video list
def parse_video_list(url):
    pass

# parse list thread
def thread_parse_list():
    pass	# TODO

# on parse video list done, update main window
def update_main_win():
    pass	# TODO

# end entry.py



