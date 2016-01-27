# restruct.py, parse_video/o/plist/lib/

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
def restruct_plinfo(plinfo):
    # key orders list
    plinfo_list = [	# plinfo
        'mark_uuid', 
        'port_version', 
        'error', 
        'info_source', 
        'extractor', 
        'extractor_name', 
        'method', 
        'info', 
        'count', 
        'list', 
        'last_update', 
    ]
    info_list = [	# plinfo.info
        'title', 
        'title_sub', 
        'title_short', 
        'title_no', 
        'site', 
        'site_name', 
        'list_url', 
        'url', 
    ]
    list_list = [	# plinfo.list[]
        # TODO
    ]
    # restruct plinfo
    out = _restruct_key(plinfo, plinfo_list)
    out['info'] = _restruct_key(out['info'], info_list)	# restruct info
    for i in range(len(out['list'])):	# restruct each list
        out['list'][i] = _restruct_key(out['list'][i], list_list)
        # TODO
    return out	# restruct plinfo done

# end restruct.py


