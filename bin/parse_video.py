# -*- coding: utf-8 -*-
# parse_video.py, parse_video/bin/
''' parse_video main bin file

Usage: ./parsev [OPTIONS] <url>

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
      
  -o, --output <file>	# TODO not support now

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
etc['flag_mode'] = None	# default mode, or 'help', 'version'
etc['output'] = '-'	# '-' means stdout

# print help and version info
def p_help():
    p('ERROR: --help function not finished. ')
    # TODO

def p_version():
    print('parse_video version 0.5.0.0 ')
    # TODO

# print function
def p(raw):
    print(raw, file=sys.stderr, flush=True)

def main(args):
    p_args(args)
    # process main start mode
    mode = etc['flag_mode']
    if mode == 'help':
        p_help()
    elif mode == 'version':
        p_version()
    else:	# default mode
        # check command line format Error
        if etc['url'] == '':
            p('ERROR: bad command line format, please try \"--help\". ')
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
        # --help, --version
        if one == '--help':
            etc['flag_mode'] = 'help'
        elif one == '--version':
            if etc['flag_mode'] != None:
                p('ERROR: already set mode to \"' + etc['flag_mode'] + '\", can not set to --version ')
            else:
                etc['flag_mode'] = 'version'
        # --debug, --quiet
        elif one in ['--debug', '-d']:
            etc['log_level'] = 'debug'
        elif one in ['--quiet', '-q']:
            if etc['log_level'] != None:
                p('ERROR: already set log_level to \"' + etc['log_level'] + '\", can not set to --quiet ')
            else:
                etc['log_level'] = 'quiet'
        # --min, --max, --min-i, --max-i
        # TODO more Error process
        elif one in ['--min', '-i']:
            etc['hd_min'] = float(rest[0])
            rest = rest[1:]
        elif one in ['--max', '-M']:
            etc['hd_max'] = float(rest[0])
            rest = rest[1:]
        elif one == '--min-i':
            etc['i_min'] = float(rest[0])
            rest = rest[1:]
        elif one == '--max-i':
            etc['i_max'] = float(rest[0])
            rest = rest[1:]
        # --extractor, --method
        elif one in ['--extractor', '-e']:
            etc['extractor'] = rest[0]
            rest = rest[1:]
        elif one in ['--method', '-m']:
            etc['method'] = rest[0]
            rest = rest[1:]
        # --output
        elif one in ['--output', '-o']:
            etc['output'] = rest[0]
            rest = rest[1:]
        # <url>
        else:	# NOTE set URL
            if etc['url'] != '':
                p('WARNING: already set URL to \"' + etc['url'] + '\", now set to \"' + one + '\" ')
            etc['url'] = one
    # done p_args

# end parse_video.py


