# -*- coding: utf-8 -*-
# parse_video.py, parse_video/bin/
#
#    parse_video : get video info from some web sites. 
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
''' parse_video main bin file

OPTIONS: 

  -d, --debug
  -q, --quiet
      
  -i, --min <hd>
  -M, --max <hd>
      --i-min <index>
      --i-max <index>
      
  -e, --extractor <raw_extractor_str>
  -m, --method <raw_method_str>
      
      --help
      --version
      --license
      
  -o, --output <file>	# TODO not support now
      --more <file>	# TODO not support now

'''

import sys
import json

from lib.b import log
from lib import entry

# global data
etc = {}
etc['log_level'] = None	# default, or 'debug', 'quiet'

etc['hd_min'] = None
etc['hd_max'] = None
etc['i_min'] = None
etc['i_max'] = None

etc['extractor'] = ''
etc['method'] = ''

etc['url'] = ''
etc['flag_mode'] = None	# default mode, or 'help', 'version', 'license'
etc['output'] = '-'	# '-' means stdout
etc['more'] = None

# print help, version and license info. (--help, --version, --license)
def p_version():
    print('''\
parse_video version 0.5.0.0 

    parse_video  Copyright (C) 2015  sceext <sceext@foxmail.com>
    This program comes with ABSOLUTELY NO WARRANTY. This is free software, and 
    you are welcome to redistribute it under certain conditions. 

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. 
Please use "--license" or read LICENSE for more details. \
''')

def p_help():
    print('''\
Usage: parsev [OPTION]... URL
parse_video: get video info from some web sites. 

  -i, --min HD       set min hd number for video formats
  -M, --max HD       set max hd
      --i-min INDEX  set min index number for part video files
      --i-max INDEX  set max index
  
  -e, --extractor EXTRACTOR  set extractor (and extractor arguments)
  -m, --method METHOD        set method (and method arguments)
  
  -d, --debug  set log level to debug
  -q, --quiet  set log level to quiet
      
      --help     display this help and exit
      --version  output version information and exit
      --license  show license information and exit

More information online: <https://github.com/sceext2/parse_video> \
''')

def p_license():
    print('''\
    parse_video : get video info from some web sites. 
    Copyright (C) 2015 sceext <sceext@foxmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. \
''')

# print function
def p(raw):
    print(raw, file=sys.stderr, flush=True)

def p_cline_err():
    p('ERROR: bad command line format, please try \"--help\". ')

def main(args):
    try:
        p_args(args)
    except Exception:
        p_cline_err()
        raise
    # process main start mode
    mode = etc['flag_mode']
    if mode == 'help':
        p_help()
    elif mode == 'version':
        p_version()
    elif mode == 'license':
        p_license()
    else:	# default mode
        # check command line format Error
        if etc['url'] == '':
            p_cline_err()
        else:
            do_parse()
    # end main

def do_parse():
    if etc['log_level'] != None:
        log.set_log_level(etc['log_level'])
    # set lib.var
    entry.init()
    set_list = [
        'hd_min', 
        'hd_max', 
        'i_min', 
        'i_max', 
    ]
    for key in set_list:
        entry.var._[key] = etc[key]
    # TODO support --more option
    # do parse
    pvinfo = entry.parse(etc['url'], extractor=etc['extractor'], method=etc['method'])
    # TODO support --output option
    p_result(pvinfo)	# print result

def p_result(pvinfo, sort_keys=False, ensure_ascii=False, file=sys.stdout):
    text = json.dumps(pvinfo, indent=4, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
    print(text, file=file, flush=True)

# process command line args
def p_args(args):
    rest = args
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        # --help, --version, --license
        if one == '--help':
            etc['flag_mode'] = 'help'
        elif one == '--version':
            if etc['flag_mode'] != None:
                p('ERROR: already set mode to \"' + etc['flag_mode'] + '\", can not set to --version ')
            else:
                etc['flag_mode'] = 'version'
        elif one == '--license':
            etc['flag_mode'] = 'license'
        # --debug, --quiet
        elif one in ['--debug', '-d']:
            etc['log_level'] = 'debug'
        elif one in ['--quiet', '-q']:
            if etc['log_level'] != None:
                p('ERROR: already set log_level to \"' + etc['log_level'] + '\", can not set to --quiet ')
            else:
                etc['log_level'] = 'quiet'
        # --min, --max, --min-i, --max-i
        elif one in ['--min', '-i']:
            etc['hd_min'] = float(rest[0])
            rest = rest[1:]
        elif one in ['--max', '-M']:
            etc['hd_max'] = float(rest[0])
            rest = rest[1:]
        elif one == '--i-min':
            etc['i_min'] = float(rest[0])
            rest = rest[1:]
        elif one == '--i-max':
            etc['i_max'] = float(rest[0])
            rest = rest[1:]
        # --extractor, --method
        elif one in ['--extractor', '-e']:
            etc['extractor'] = rest[0]
            rest = rest[1:]
        elif one in ['--method', '-m']:
            etc['method'] = rest[0]
            rest = rest[1:]
        # --output, --more
        elif one in ['--output', '-o']:
            etc['output'] = rest[0]
            rest = rest[1:]
        elif one == '--more':
            etc['more'] = rest[0]
            rest = rest[1:]
        # URL
        else:	# NOTE set URL
            if etc['url'] != '':
                p('WARNING: already set URL to \"' + etc['url'] + '\", now set to \"' + one + '\" ')
            etc['url'] = one
    # done p_args

# end parse_video.py


