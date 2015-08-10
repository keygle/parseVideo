# -*- coding: utf-8 -*-
# node_port.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# node_port: bks1, node_port to run javascript. 

# import

import os.path

from ..raw.key import md5_hash

from . import salt

# global vars

flag_debug = False

# functions

def mix(tvid, tm):
    return mix2_host(tvid, tm)

def mix2_host(tvid, tm0):
    sc = mix2(tvid, tm0)
    
    result = {}
    result['tm'] = tm0
    result['sc'] = sc
    # done
    return result

def mix2(tvid, tm0):
    
    enc = get_enc_raw()
    enc += str(tm0) + str(tvid)
    # now enc is raw str before md5_hash
    sc = md5_hash(enc)
    return sc

# NOTE just return the enc key
def get_enc_raw():
    enc = salt.enc
    # done
    return enc

# NOTE just reserved code

# import execjs
# 
# BIN_JS_FILE = './node_utils.js'
# 
# def import_js():
#     # make js path
#     this_path = __file__
#     base_path = os.path.dirname(this_path)
#     bin_path = os.path.join(base_path, BIN_JS_FILE)
#     
#     # read js file
#     with open(bin_path) as f:
#         s = f.read()
#     # compile as js
#     c = execjs.compile(s)
#     
#     # done
#     return c
# 
# def mix1(tvid, tm):
#     # import js
#     c = import_js()
#     
#     # just run it
#     result = c.call('mix', str(tvid), int(tm))
#     # done
#     return result

# end node_port.py


