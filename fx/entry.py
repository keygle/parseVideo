# -*- coding: utf-8 -*-
# entry.py for lyp-FX-mkbag tool, sceext <sceext@foxmail.com> 
# version 0.0.1.0 test201509100058

import json

from . import make_bag, raw_parse

# main entry function
def main(etc = {}):
    pv_arg = etc['pv_arg']	# parse_video command line args
    output = etc['output']	# final output file
    
    raw_info = raw_parse.run_pv(args=pv_arg)
    bag_info = make_bag.make_bag(raw_info)
    
    # save as json file
    text = json.dumps(bag_info)
    with open(output, 'w') as f:
        f.write(text)
    
    # done

# end entry.py


