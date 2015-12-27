# var.py, parse_video/lib/e/letv/

# static data

EXTRACTOR_ID = 'letv'
EXTRACTOR_NAME = 'letv_1'
SITE = 'letv'
SITE_NAME = '乐视网'

RE_SUPPORT_URL = [
    # http://www.letv.com/ptv/vplay/24143557.html
    '^http://www\.letv\.com/.+\.html', 
]

METHOD_LIST = [
    'pc_flash_gate', 
]

RE_VID_LIST = {
    'vid' : ' vid:([0-9]+),', 
}

# site rateid to parse_video hd quality
RATEID_TO_HD = {
    '1080p' : 4, 	# 1080p
    '720p' : 2, 	# 720p
    '1300' : 0, 	# HD
    '1000' : -1, 	# SD
    '350' : -3, 	# LW
}

FIRST_OK_CODE = '1001'
BEFORE_OK_CODE = 200

# var data
_ = {}

_var_init_flag = False
# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    # set default values
    out['raw_arg'] = ''
    out['raw_method'] = ''
    
    out['more'] = None
    # config items
    out['hd_min'] = None
    out['hd_max'] = None
    out['i_min'] = None
    out['i_max'] = None
    
    out['pool_size_get_m3u8'] = 8	# TODO
    
    out['enable_more'] = False
    out['_use_more'] = False
    # private data
    out['_raw_url'] = ''
    out['_raw_page_html'] = ''
    out['_vid_info'] = None
    
    out['_raw_first_json'] = ''
    # add data done
    return out

# base var functions
def push():
    __old.append(_)
def pop():
    return __old.pop()    
# end var.py


