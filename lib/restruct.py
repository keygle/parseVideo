# restruct.py, parse_video/lib/

from collections import OrderedDict

# base restruct function
def _restruct_key(old, key_list=[], rest_sort_reverse=False):
    '''
    restruct a dict to OrderedDict
    order is in key_list
    
    rest keys is keys in old but not in key_list
    rest keys is sort by rest_sort_reverse
    if rest_sort_reverse == None, rest keys will not be sort
    '''
    raw = old.copy()	# not modify old dict
    out = OrderedDict()
    for key in key_list:
        if key in raw:	# ignore not exist keys
            out[key] = raw.pop(key)
    # get rest key list and sort keys by key name
    rest_key = [i for i in raw]
    if rest_sort_reverse != None:
        rest_key.sort(reverse=rest_sort_reverse)
    # add rest keys
    for key in rest_key:
        out[key] = raw.pop(key)
    return out

# main restruct function
def restruct_pvinfo(pvinfo):
    # key orders list
    pvinfo_list = [	# pvinfo
        'mark_uuid', 
        'port_version', 
        'error', 
        'info_source', 
        'extractor', 
        'extractor_name', 
        'method', 
        'info', 
        'video', 
        'last_update', 
    ]
    info_list = [	# pvinfo.info
        'title', 
        'title_sub', 
        'title_short', 
        'title_no', 
        'site', 
        'site_name', 
        'url', 
    ]
    video_list = [	# pvinfo.video[]
        'hd', 
        'quality', 
        'size_px', 
        'size_byte', 
        'time_s', 
        'format', 
        'count', 
        'file', 
    ]
    file_list = [	# pvinfo.video[].file[]
        'type', 
        'size', 
        'time_s', 
        'url', 
        'header', 
        'expire', 
        'checksum', 
    ]
    # restruct pvinfo
    out = _restruct_key(pvinfo, pvinfo_list)
    out['info'] = _restruct_key(out['info'], info_list)	# restruct info
    for i in range(len(out['video'])):	# restruct videos
        out['video'][i] = _restruct_key(out['video'][i], video_list)
        v = out['video'][i]
        for j in range(len(v['file'])):	# restruct files
            v['file'][j] = _restruct_key(v['file'][j], file_list)
            f = v['file'][j]
            if 'checksum' in f:	# check and restruct checksum
                f['checksum'] = _restruct_key(f['checksum'])
    # sort videos by hd
    out['video'].sort(key=lambda x:x['hd'], reverse=True)
    return out	# restruct pvinfo done

# end restruct.py


