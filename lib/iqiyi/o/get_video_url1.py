# -*- coding: utf-8 -*-
# get_video_url1.py, part for parse_video : a fork from parseVideo. 
# get_video_url1: from parseVideo, iqiyi.class.php

# import

import random

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
BEFORE_FINAL_URL = 'http://data.video.qiyi.com/'

# functions
def get_server_time():
    time_url = config.FIRST_DISPATCH_URL + '?tn=' + str(random.random())
    info = base.get_json_info(time_url)
    server_time = info['t']
    return server_time

def get_time_now():
    time_now = flash.getTimer()
    return time_now

def get_one_final_url(raw_link, more):
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
    # make final url
    final_url = BEFORE_FINAL_URL + this_key + '/videos' + this_link
    # done
    return final_url

# end get_video_url1.py


