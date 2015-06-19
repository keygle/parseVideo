# -*- coding: utf-8 -*-
# node_port.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# node_port: iqiyi, node_port to run javascript. 

# import
import os.path

import execjs

# global vars

BIN_JS_FILE = './Z7elzzup.js'

flag_debug = False

# functions

def import_js():
    # make js path
    this_path = __file__
    base_path = os.path.dirname(this_path)
    bin_path = os.path.join(base_path, BIN_JS_FILE)
    
    # read js file
    with open(bin_path) as f:
        s = f.read()
    # compile as js
    c = execjs.compile(s)
    
    # done
    return c

def mix(tvid, tm):
    # import js
    c = import_js()
    
    # just run it
    result = c.call('mix', str(tvid), int(tm))
    # done
    return result

# end node_port.py


