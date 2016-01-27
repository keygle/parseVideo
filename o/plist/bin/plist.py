#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# plist.py, parse_video/o/plist/bin/
# TODO
#
''' plist main bin file

OPTIONS not in --help:

TODO

'''

import json

from lib import err, b, conf, log
from lib import entry, gen_list_file

VERSION_STR = 'plist version 0.0.1.0 test201601271232'

# global data
etc = {}
etc['start_mode'] = 'normal'	# ['normal', '--help', '--version']


# print functions

def p_help():
    print('''\
Usage: plist [OPTION]... URL
plist: (parse list) video list support for pvdl. 

  -o, --output DIR  set list file output dir
  
  -d, --debug  set log level to debug
  
      --help     display this help and exit
      --version  output version information and exit

More information online: <https://github.com/sceext2/parse_video> \
''')

def p_version():
    print(VERSION_STR + '''
    TODO
''')

def p_cline_err():
    log.e('bad command line format, please try \"--help\". ')

# NOTE main
def main(args):
    try:
        p_args(args)
    except Exception:
        p_cline_err()
        raise
    # check start mode
    mode_list = {
        'normal' : start_normal, 
        '--help' : p_help, 
        '--version' : p_version, 
    }
    worker = mode_list[etc['start_mode']]
    worker()
    # end main

# process command line args
def p_args(args):
    # TODO more Error process
    rest = args.copy()
    while len(rest) > 0:
        one, rest = rest[0], rest[1:]
        # --help, --version
        if one in ['--help', '--version']:
            # TODO check --help mode
            etc['start_mode'] = one
        # -o, --output
        elif one in ['-o', '--output']:
            out_dir, rest = rest[0], rest[1:]
            conf.output_dir = out_dir
        # -d, --debug
        elif one in ['-d', '--debug']:
            pass	# TODO support DEBUG mode
        else:	# set URL
            if conf.raw_url != '':
                log.w('already set URL to \"' + conf.raw_url + '\", now set to \"' + one + '\" ')
            conf.raw_url = one
    # end p_args

def start_normal():
    # check raw_url
    if conf.raw_url == '':
        log.w('input empty URL ! ')
        p_cline_err()
        return
    # set plist_version
    conf.plist_version = VERSION_STR
    # use lib to do parse
    # TODO
    # TODO print result to stdout as json
    # TODO support not write list file
    # TODO write list file
    # end start_normal

# end plist.py


