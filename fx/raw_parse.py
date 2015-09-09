# -*- coding: utf-8 -*-
# raw_parse.py for lyp-FX-mkbag tool, sceext <sceext@foxmail.com> 
# get raw parse result from parse_video
# version 0.0.1.0 test201509092314

import sys, json
import subprocess

from . import conf

def run_pv(args=[]):
    arg = [conf.pv_bin] + args
    
    PIPE = subprocess.PIPE
    p = subprocess.Popen(arg, stdout=PIPE, stderr=sys.stderr, shell=False)
    stdout, stderr = p.communicate()
    
    raw_text = stdout.decode('utf-8')
    raw_info = json.loads(raw_text)
    
    return raw_info

# end raw_parse.py


