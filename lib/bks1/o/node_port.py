# -*- coding: utf-8 -*-
# node_port.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# node_port: bks1, node_port to run javascript. 

# import

import os.path

# import execjs

from .key import md5_hash

# global vars

BIN_JS_FILE = './Z7elzzup.js'

flag_debug = False

# functions

def mix(tvid, tm):
    return mix2_host(tvid, tm)

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

def mix1(tvid, tm):
    # import js
    c = import_js()
    
    # just run it
    result = c.call('mix', str(tvid), int(tm))
    # done
    return result

def mix2_host(tvid, tm0):
    tm, sc, src = mix2(tvid, tm0)
    
    result = {}
    result['tm'] = tm
    result['sc'] = sc
    result['src'] = src
    # done
    return result

def mix2(tvid, tm0):
    enc = ''
    enc += '7b11c5408ff342318da3e7c97b92e890'
    tm = str(tm0)
    src = 'hsalf'
    enc += str(tm)
    enc += str(tvid)
    sc = md5_hash(enc)
    return tm, sc, src

# end node_port.py


