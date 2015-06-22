# -*- coding: utf-8 -*-
# run, part for parse_video : a fork from parseVideo. 
# run: lieying-plugin entry file. 
# version 0.0.2.0 test201506081632
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

import os
import sys

# make now path
now_path = os.path.dirname(__file__)
sys.path.insert(0, now_path)

from o.lieying_plugin import entry as entry0

# export functions for lieying plugin
GetName = entry0.lieying_plugin_get_name	# get_name()
GetType = entry0.lieying_plugin_get_type	# get_type()
GetFilter = entry0.lieying_plugin_get_filter	# get_filter()
ParseFormat = entry0.lieying_plugin_parse_format	# parse_format(url)
ParseUrl = entry0.lieying_plugin_parse_url	# parse_url(url, format_text)

# end run.py


