# -*- coding: utf-8 -*-
# p271v_conf.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# p271v_conf: parse_video/lib/iqiyi/o

# import
import os
import json

# global vars
CONFIG_FILE = '../private.271v_conf.json'

# function

def get_conf_path():
    raw = os.path.dirname(__file__)
    conf_path = os.path.join(raw, CONFIG_FILE)
    # done
    return conf_path

def load_conf():
    conf_path = get_conf_path()
    # read file
    with open(conf_path) as f:
        text = f.read()
    # parse as json
    conf = json.loads(text)
    # done
    return conf

# main export method
def set_remote_mixer(rm, conf):
    
    # set flags
    rm.flag_is_vip = True
    rm.flag_set_um = True
    
    # set config
    rm.uid = conf['uid']
    rm.puid = conf['uid']
    rm.cid = conf['cid']
    rm.token = conf['token']
    rm.qyid = conf['qyid']
    # done

# end p271v_conf.py


