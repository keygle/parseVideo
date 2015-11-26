# restruct.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509272002

'''
parse_video/lib/restruct.py
    restruct evinfo with OrderedDict for pretty json print
'''

from collections import OrderedDict

# global data for evinfo struct
EVINFO_VERSION = 'evdh info_source info_version 0.3.0.0 test201509272000'

# base struct functions

def restruct_key(old, key_list=[], rest_sort_reverse=False):
    '''
    restruct a dict to OrderedDict
    order is in key_list
    rest keys not in key_list is sort by rest_sort_reverse
    '''
    raw = old.copy()
    out = OrderedDict()
    for key in key_list:
        if key in raw:
            out[key] = raw.pop(key)
    # add rest keys, and sort key names
    rest_key = []
    for rest in raw:
        rest_key.append(rest)
    if rest_sort_reverse != None:
        rest_key.sort(reverse=rest_sort_reverse)
    for key in rest_key:
        out[key] = raw.pop(key)
    return out

# main restruct function

def restruct_evinfo(raw_evinfo):
    # key list used for restruct
    evinfo_list = [	# key list for main evinfo
        'info', 
        'video', 
    ]
    info_list = [	# key list for evinfo.info
        'error', 
        'info_version', 
        'info_source', 
        'extractor', 
        'extractor_name', 
        'title', 
        'title_short', 
        'title_no', 
        'title_sub', 
        'site', 
        'site_name', 
        'url', 
    ]
    video_list = [	# key list for one video
        'hd', 
        'quality', 
        'size_px', 
        'size_byte', 
        'time_s', 
        'format', 
        'count', 
        'file', 
    ]
    file_list = [	# key list for one file
        'size', 
        'time_s', 
        'url', 
    ]
    # start restruct
    raw = raw_evinfo
    # restruct evinfo
    evinfo = restruct_key(raw, evinfo_list)
    # restruct info
    evinfo['info'] = restruct_key(raw['info'], info_list)
    # restruct videos
    evinfo['video'] = []
    for v in raw['video']:
        one = restruct_key(v, video_list)
        # restruct files
        one['file'] = []
        for f in v['file']:
            onef = restruct_key(f, file_list)
            one['file'].append(onef)
        evinfo['video'].append(one)
    # sort videos by hd
    evinfo['video'].sort(key=lambda x:x['hd'], reverse=True)
    # restruct evinfo done
    return evinfo

# end restruct.py


