# mango_tv3.py, parse_video/lib/e/hunantv/o/, MangoTV_3.swf

import random

# package com.global.Config
CMS_ADDRESS = 'http://v.api.hunantv.com/player/video?video_id='

# package com.global.Method
def get_random_str(length=0):
    # public static function GetRandomStr(param1:int) : String
    out = ''
    for i in range(length):
        out +=  str(int(random.random() * 1e3))
    return out

# package Main

def gen_first_url(vid):
    # private function GetCMSVideoInfo()
    VIDEO_CMS = CMS_ADDRESS + vid + '&r=' + get_random_str(5)
    return VIDEO_CMS

def gen_before_url(raw):
    # private function GetVideoRouteURL()
    VIDEO_DISPATCHER_URL = raw + '&r=' + get_random_str(5)
    return VIDEO_DISPATCHER_URL

# end mango_tv3.py


