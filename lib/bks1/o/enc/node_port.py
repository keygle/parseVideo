# -*- coding: utf-8 -*-
# node_port.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# node_port: bks1, node_port to run javascript. 

# import

import os.path

# import execjs

from ..raw.key import md5_hash

# global vars

BIN_JS_FILE = './node_utils.js'

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
    sc = mix2(tvid, tm0)
    
    result = {}
    result['tm'] = tm0
    result['sc'] = sc
    # done
    return result

def mix2(tvid, tm0):
    # enc = '8e29ab5666d041c3a1ea76e06dabdffb'	# NOTE old salt for Vampire	# 2015-07-17
    enc   = '7c4d2505ad0544b88c7679c65d6748a1'	# NOTE new salt for Zombie	# 2015-07-30
    enc += str(tm0) + str(tvid)
    
    sc = md5_hash(enc)
    return sc

# end node_port.py


