# url_to_e.py, parse_video/lib/e :: URL to extractor
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509271605

'''
auto select extractor from URL with re filter in config file
'''

import re

from .. import var

def get_list(url=None):
    if not url:
        return []
    # process each filter items
    fl = var._['url_to_e_filter']	# filter list
    out = []
    for r in fl:
        if len(re.findall(r, url)) > 0:
            e_id = fl[r]	# extractor_id
            if not e_id in out:
                out.append(e_id)
    return out

# end url_to_e.py


