# -*- coding: utf-8 -*-
# make_bag.py for lyp-FX-mkbag
# gen bag file content, make info format and do some translate
# version 0.0.4.0 test201509101352

import datetime

from . import fx_bag_def as bagdef

# main entry file
def make_bag(raw):
    # create a bag info file struct
    info = init_bag_struct()
    # translate info and add it
    video_info = translate_one_video_info(raw)
    info = add_only_one_video_info(info, one_video_info = video_info)
    # add more info
    info = add_more_bag_info(info)
    
    return info

# bag info file struct functions

def init_bag_struct():
    info = {}
    # add header info
    info['file_type_uuid'] = bagdef.bag_file_type_uuid
    info['file_type'] = bagdef.bag_file_type
    info['bag_version'] = bagdef.bag_version
    
    info['body'] = {}
    info['body']['data'] = []
    
    return info

# bag info type is 'video'
def add_only_one_video_info(info, one_video_info={}):
    info['body']['info_type'] = 'video'
    info['body']['data'].append(one_video_info)
    return info

def add_more_bag_info(info):
    now_time = datetime.datetime.utcnow().isoformat() + 'Z'
    info['last_update'] = now_time
    
    return info

# translate parse_video output to fx-bag functions
def translate_one_video_info(raw):
    out = {}
    # add info part
    out['info'] = {}
    info = out['info']
    
    key_list = [
        'title', 
        'title_short', 
        'title_no', 
        'title_sub', 
        'site', 
        'site_name', 
        'url', 
    ]
    
    for k in key_list:
        info[k] = raw['info'][k]
    # NOTE add site_uuid
    info['site_uuid'] = bagdef.site['bks1']
    
    # add videos info
    out['video'] = []
    video = out['video']
    
    v_key_list = [
        'hd', 
        'quality', 
        'size_px', 
        'size_byte', 
        'time_s', 
        'format', 
        'count', 
    ]
    f_key_list = [
        'size', 
        'time_s', 
        # NOTE add a md5 data for one file
    ]
    
    for v in raw['video']:
        onev = {}
        for k in v_key_list:
            onev[k] = v[k]
        
        onev['file'] = []
        file_list = onev['file']
        for f in v['file']:
            onef = {}
            for k in f_key_list:
                onef[k] = f[k]
            # process raw URL and add md5
            url, md5 = translate_one_final_url(f['url'])
            onef['url'] = url
            onef['checksum'] = {}
            onef['checksum']['md5'] = md5
            
            file_list.append(onef)
        video.append(onev)
    
    return out

def translate_one_final_url(raw_url):
    # check empty url
    if raw_url == '':
        return '', ''
    
    # process normal url
    before, m = raw_url.split('/videos/', 1)
    m = '/' + m
    
    m, after = m.split('?', 1)
    md5 = m.rsplit('/', 1)[1].rsplit('.', 1)[0]
    
    # get key
    raw_parts = after.split('&')
    parts = {}
    for r in raw_parts:
        name, value = r.split('=', 1)
        parts[name] = value
    key = parts['key']
    
    url = [m, key]
    return url, md5

# end make_bag.py


