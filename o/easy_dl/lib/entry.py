# -*- coding: utf-8 -*-
# entry.py, part for parse_video : a fork from parseVideo. 
# entry:o/easy_dl/lib
# version 0.0.0.1 test201507011445
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

from . import parsev
from . import make_name
from . import wget

from . import conf
from . import merge

# global vars

etc = {}

etc['hd'] = 0	# video hd, quality, used for parsev --min hd --max hd

etc['min'] = 0	# min index of files to download, used for parsev --min-i
etc['max'] = 0	# max index of files to download, used for parsev --max-i

etc['out_dir'] = ''	# output file path
etc['ext_opt'] = []	# ext_opt for parsev

# function

# end entry.py


