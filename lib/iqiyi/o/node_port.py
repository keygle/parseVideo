# -*- coding: utf-8 -*-
# node_port.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# node_port: iqiyi, node_port for DMEmagelzzup 

# import
import subprocess
import json
import os.path

# global vars
BIN_NODE = 'node'
BIN_NODE_PORT = 'node_port.js'

# base functions1
def run_sub(arg, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

def get_node_port_path(fpath):
    now_file = os.path.abspath(__file__)
    now_dir = os.path.dirname(now_file)
    bin_file = os.path.join(now_dir, fpath)
    bin_file = os.path.normpath(bin_file)
    # done
    return bin_file

# functions
def mix(tvid, tm):
    # make args
    port_bin = get_node_port_path(BIN_NODE_PORT)
    arg = [BIN_NODE, port_bin, str(tvid), str(tm)]
    
    # run node
    stdout, stderr = run_sub(arg)
    # parse result as json
    out = stdout.decode('utf-8')
    
    info = json.loads(out)
    # done
    return info

# end node_port.py


