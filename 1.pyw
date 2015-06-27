#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1.py, for parse_video win vesion
# used on windows, with python3

# import
import sys
import json

from o.pvtkgui import entry

# global vars
etc = {}
etc['flag_debug'] = False
etc['url'] = ''

# functions
def get_args():
    arg = sys.argv[:]
    rest = arg
    # DEBUG info
    print('pvtkgui: DEBUG: 1.pyw: got args ' + json.dumps(rest))
    # check each arg
    while len(rest) > 0:
    	one = rest[0]
    	rest = rest[1:]
    	# check one
    	if one == '--debug':
    	    etc['flag_debug'] = True
    	elif one == '--url':
    	    next = rest[0]
    	    rest = rest[1:]
    	    etc['url'] = next
    	else:	# unknow arg
    	    # debug info
    	    print('pvtkgui: DEBUG: 1.pyw: unknow arg \"' + one + '\"')
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
        print('pvtkgui: DEBUG: 1.pyw: got --debug flag')
    
    # set entry
    entry.etc['url_to'] = etc['url']
    
    # just start entry
    entry.init()
    return 0

# start from main
if __name__ == '__main__':
    exit(main())

# end 1.py


