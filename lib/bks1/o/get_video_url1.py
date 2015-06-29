# -*- coding: utf-8 -*-
# get_video_url1.py, part for parse_video : a fork from parseVideo. 
# get_video_url1: from parseVideo, bks1.class.php

# import

import random
import sys

from . import config
from . import key

# NOTE should be set
base = None
flash = None
def set_import(base0, flash0):
    global base
    global flash
    base = base0
    flash = flash0

# global vars
GET_SERVER_TIME_RETRY = 5
GET_SERVER_TIME_DEBUG = True

# get random time
def get_ran_time(t_min=0, t_max=1):
    r = random.random()
    t = t_min + (t_max - t_min) * r
    return round(t)

# functions
def get_server_time0():
    time_url = config.FIRST_DISPATCH_URL + '?tn=' + str(random.random())
    try:
        info = base.get_json_info(time_url)
    except Exception as err:
        raise Exception('DEBUG: bks1, get_server_time http error', err)
    server_time = info['t']
    return server_time

# auto retry to get server_time 0
def get_server_time():
    retry = 0
    while retry < GET_SERVER_TIME_RETRY:
        try:
            server_time = get_server_time0()
            if GET_SERVER_TIME_DEBUG and retry > 0:
                print('DEBUG: get_server_time ok at retry ' + str(retry), file = sys.stderr)
            return server_time
        except Exception as err:
            if retry < GET_SERVER_TIME_RETRY:
                retry += 1
                continue
            else:
                raise Exception('DEBUG: get_server_time retry time', retry, err)
    # done

# new random time
def get_time_now():
    return get_ran_time(1000, 2000)

# old reserved
def get_time_now0():
    time_now = flash.getTimer()
    return time_now

def get_one_final_url(raw_link, more, flag_use_raw_du=False):
    # get data from more
    bid = more['bid']
    uid = more['uid']
    tvid = more['tvid']
    server_time = more['server_time']
    time_now = more['time_now']
    # make this_link
    this_link = raw_link
    if bid in [4, 5, 10]:
        this_link = key.getVrsEncodeCode(raw_link)
    # make this_key
    sp = this_link.split('/')
    fileid = sp[-1].split('.')[0]
    this_key = key.getDispatchKey(server_time, fileid)
    # generate video part file url
    this_link += '?ran=' + str(time_now)
    this_link += '&qyid=' + uid
    this_link += '&qypid=' + tvid + '_11'
    # TODO reserved
    this_link += '&retry=1'
    
    # process du
    raw_du = more['du']
    du = raw_du.rsplit('/', 1)
    # make final url
    if flag_use_raw_du:
        final_url = raw_du + this_link
    else:
        final_url = du[0] + '/' + this_key + '/' + du[1] + this_link
    # done
    return final_url

# 271v get_one_final_url
def p271v_get_one_final_url(raw_link, more, key_info):
    
    bid = more['bid']
    # make url
    if bid in [4, 5, 10]:
        raw_link = key.getVrsEncodeCode(raw_link)
    this_link = more['du'] + raw_link
    # replace
    this_link.replace('.flv', '.hml', 1)
    
    # TODO may be not stable
    
    # add options
    _a = ''	# append string
    _a += '?t=' + key_info['t']
    _a += '&cid=' + key_info['cid']
    _a += '&vid=' + key_info['vid']
    _a += '&QY00001=' + key_info['QY00001']
    _a += '&qyid=' + more['uid']
    _a += '&qypid=' + more['tvid'] + '_11'
    _a += '&ran=' + str(more['time_now'])
    
    this_link += _a
    
    # done
    return this_link

# end get_video_url1.py


