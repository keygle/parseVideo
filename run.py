# -*- coding: utf-8 -*-
# run, part for parse_video : a fork from parseVideo. 
# run: lieying-plugin entry file. 
# version 0.2.2.0 test201507122114
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

import os
import sys

# make now path
now_path = os.path.dirname(__file__)
sys.path.insert(0, now_path)

from o.lieying_plugin import entry as entry0

# export functions for lieying plugin
GetVersion = entry0.lieying_plugin_get_version		# get_version()
# StartConfig = entry0.lieying_plugin_start_config	# start_config()

Parse = entry0.lieying_plugin_parse			# parse(input_text)
ParseURL = entry0.lieying_plugin_parse_url		# parse_url(url, label, i_min=None, i_max=None)

# end run.py


