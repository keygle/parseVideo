# _re.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509241250

import re

def re_get_list(re_list, text='', re_fix=None):
    out = {}
    for key, r in re_list.items():
        one = re.findall(r, text)
        out[key] = None
        if len(one) > 0:
            out[key] = one[0]
            if re_fix != None:
                out[key] = out[key][re_fix]
    return out

# end _re.py


