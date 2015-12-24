# var.py, parse_video/lib/e/bks1/

# static data

EXTRACTOR_ID = 'bks1'
EXTRACTOR_NAME = 'bks1_1'
SITE = 'bks1'
SITE_NAME = '不可说'

RE_SUPPORT_URL = [
    '^http://[a-z]+\.iqiyi\.com/.+\.html', 
]

# available method list of the extractor
METHOD_LIST = [
    # default method, only support flv format video
    'pc_flash_gate', 
]

RE_VID_LIST = {
    'tvid' : 'data-player-tvid="([^"]+)"', 
    'vid'  : 'data-player-videoid="([^"]+)"', 
    'aid'  : 'data-player-albumid="([^"]+)"', 
    
    'flag_vv' : 'data-player-ismember="([^"]+)"', 
}

# site video bid to parse_video hd quality
BID_TO_HD = {	# video bid to video hd
    10 : 7, 	# 4k, 		4K
    5 : 4, 	# fullhd, 	1080p
    4 : 2, 	# super-high, 	720p
    3 : 1, 	# super, 	高清
    2 : 0, 	# high, 	普清
    1 : -1, 	# standard, 	低清
    0 : -2, 	# none, 	超低清
    96 : -3, 	# topspeed, 	渣清
}

VMS_OK_CODE = 'A000000'

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
    
    out['pool_size_get_file_url'] = 16
    
    out['set_um'] = False
    out['set_vv'] = False
    
    out['flag_v'] = False	# NOTE for vv
    # TODO
    
    # private data
    out['_raw_url'] = ''
    out['_raw_page_html'] = ''
    out['_vid_info'] = None
    
    out['_raw_vms_json'] = ''
    
    # TODO
    # add data done
    return out

# base var functions
def push():
    __old.append(_)
def pop():
    return __old.pop()
# end var.py


