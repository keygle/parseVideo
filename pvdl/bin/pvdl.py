# -*- coding: utf-8 -*-
# pvdl.py, parse_video/pvdl/bin/
#
#    pvdl : A reference implemention of a downloader which uses parse_video. 
#    Copyright (C) 2016 sceext <sceext@foxmail.com>
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
''' pvdl main bin file

OPTIONS not in --help: 


TODO support options (new functions)
  --list  LIST file

TODO
'''

from lib import entry

VERSION_STR = 'pvdl version 0.0.1.0 test201601191216'

# global data
etc = {}
# TODO

# print functions

def print_help():
    print('''\
Usage: pvdl [OPTION]... URL
pvdl: A reference implemention of a downloader which uses parse_video. 

      --hd HD        set hd to select
  -o, --output DIR   save downloaded file to DIR
      --retry TIMES  set retry times
      
      --enable FEATURE   enable pvdl features
      --disable FEATURE  disable pvdl features
      
      --  directly pass options to parse_video
  
  -d, --debug  set log level to debug
      
      --help     display this help and exit
      --version  output version information and exit
      --license  show license information and exit

More information online: <https://github.com/sceext2/parse_video> \
''')

def print_version():
    pass

def print_license():
    pass


# TODO

# end pvdl.py


