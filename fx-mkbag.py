#!/usr/bin/env python
# -*- coding: utf-8 -*-
# fx-mkbag.py for lyp-FX-mkbag tool, sceext <sceext@foxmail.com> 
# main bin entry file
# version 0.0.2.0 test201509100105
#
# supported command line options
#	--fx-output <file>	write bag file result to the output file
# NOTE will pass all unknow options to parse_video

import sys

from fx import entry

# global config data
etc = {}
etc['pv_arg'] = []	# parse_video options
etc['output'] = ''	# target output file

# main function
def main(arg):
    # process args
    rest = arg
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        if one == '--fx-output':
            etc['output'] = rest[0]
            rest = rest[1:]
        else:	# unknow option, pass it to parse_video
            etc['pv_arg'].append(one)
    # start from main entry
    entry.main(etc = etc)

# start from main
if __name__ == '__main__':
    main(sys.argv[1:])

# end fx-mkbag.py


