#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1.py, for parse_video win vesion
# used on windows, with python3

# import
import sys
import json

from o.pvtkgui import entry
from bin import make_rename_list as make_rename_list0
from bin import output_text as output_text0

# set import
entry.set_import(make_rename_list=make_rename_list0, output_text=output_text0)

# global vars
etc = {}
etc['flag_debug'] = False

# functions
def get_args():
    arg = sys.argv[:]
    rest = arg
    # DEBUG info
    print('DEBUG: 1.pyw: got args ' + json.dumps(rest))
    # check each arg
    while len(rest) > 0:
    	one = rest[0]
    	rest = rest[1:]
    	# check one
    	if one == '--debug':
    	    etc['flag_debug'] = True
    	else:
    	    pass
    # get args done

# main function
def main():
    # get args
    get_args()
    # set entry
    entry.flag_debug = etc['flag_debug']
    # check flag_debug
    if etc['flag_debug']:
        # DEBUG info
        print('DEBUG: 1.pyw: got --debug flag')
    # just start entry
    entry.init()
    # TODO FIXME debug here
    return 0

# start from main
if __name__ == '__main__':
    exit(main())

# end 1.py


