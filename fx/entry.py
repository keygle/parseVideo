# -*- coding: utf-8 -*-
# entry.py for lyp-FX-mkbag tool, sceext <sceext@foxmail.com> 
# version 0.0.2.0 test201509100107

import json

from . import make_bag, raw_parse

# main entry function
def main(etc = {}):
    pv_arg = etc['pv_arg']	# parse_video command line args
    output = etc['output']	# final output file
    
    raw_info = raw_parse.run_pv(args=pv_arg)
    bag_info = make_bag.make_bag(raw_info)
    
    # save as json file
    text = json.dumps(bag_info, indent=4, sort_keys=True, ensure_ascii=False)
    with open(output, 'w') as f:
        f.write(text)
    
    # done

# end entry.py


