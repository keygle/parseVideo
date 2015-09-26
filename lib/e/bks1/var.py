# var.py, parse_video/lib/e/bks1
# version 0.0.14.0 test201509261818

'''
parse_video/lib/e/bks1/var.py
    global common data for extractor bks1
part of standard port for parse_video extractor
'''

# static data

EXTRACTOR_ID = 'bks1'
EXTRACTOR_NAME = 'bks1_1'
SITE = 'bks1'
SITE_NAME = '不可说'

RE_SUPPORT_URL = [
    '^http://[a-z]+\.iqiyi\.com/.+\.html', 
]

CONF_FILE = 'e_bks1.conf.json'

# available methods of this extractor
METHOD_LIST = [
    # TODO normal method, use the big gate from PC web page flash player
    # this method will request before_final_url to get final_url
    'pc_flash_gate', 		# NOTE only support flv video format
    # TODO use inter cdn server with given key
    # this method will process normal final_url to get key
    'cdn_inter', 		# NOTE only support flv video format
    # TODO only use dispatch key, not send a request to get key; 
    # only works with normal F videos
    'only_dispatch_key', 	# NOTE only support flv video format
    
    # NOTE nosalt methods
    # TODO use enhp and google-chrome http_proxy
    # only no enc salt, other process is the same as pc_flash_gate
    'nosalt_chrome_proxy', 	# NOTE only support flv video format
    
    # TODO add more mix functions
]

RE_VID_LIST = {
    'vid' : 'data-(player|drama)-videoid="([^"]+)"', 
    'tvid' : 'data-(player|drama)-tvid="([^"]+)"', 
    'aid' : 'data-(player|drama)-albumid="([^"]*)"', 
    'flag_vv' : 'data-(player|drama)-ismember="([^"]+)"', 
}
RE_VID_LIST_FIX = 1

# player global config data
# NOTE get this code from com.qiyi.player.core.Config
CHECK_LIMIT_URL = 'http://cache.vip.qiyi.com/ip/'
CHECK_V_INFO_URL = 'http://data.video.qiyi.com/v.f4v'
VIP_AUTH_URL = 'http://api.vip.iqiyi.com/services/ck.action'
MIXER_VX_URL = 'http://cache.video.qiyi.com/vms'
MIXER_VX_VIP_URL = 'http://cache.vip.qiyi.com/vms'

FIRST_DISPATCH_URL = 'http://data.video.qiyi.com/t'

# to load user uuid from server
UUID_URL = 'http://data.video.qiyi.com/uid'
# cid for first_url
DEFAULT_CID = 'afbe8fd3d73448c9'

# translate video bid to parse_video hd quality
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

'''
video quality define
    NOTE get this code from com.qiyi.player.core.model.def.DefinitionEnum

视频清晰度定义

# 官方清晰度	实际清晰度	hd

# (极速)	渣清		-3
LIMIT 		= EnumItem(96, 'topspeed', items)
# (流畅)	超低清		-2
NONE 		= EnumItem(0, 'none', items)
# (标清)	低清		-1
STANDARD 	= EnumItem(1, 'standard', items)
# (高清)	普清		0
HIGH 		= EnumItem(2, 'high', items)
# (超清)	高清		1
SUPER 		= EnumItem(3, 'super', items)
# (720p)	720p		2
SUPER_HIGH 	= EnumItem(4, 'super-high', items)
# (1080p)	1080p		4
FULL_HD 	= EnumItem(5, 'fullhd', items)
# (4K)		4K		7
FOUR_K 		= EnumItem(10, '4k', items)
'''

# var data
_ = {}

# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    # set default values
    out['raw_arg'] = ''		# this is used to pass raw_arg to extractor
    out['raw_method'] = ''	# this is used to pass raw_method to extractor
    
    # config items
    out['flag_v'] = False
    out['flag_v_force'] = False
    out['pool_size_get_final_url'] = 16
    
    # private data
    out['_raw_url'] = ''
    out['_raw_page_html'] = ''
    out['_vid_info'] = None
    out['_first_url'] = ''
    out['_raw_vms_json'] = ''
    out['_vms_json'] = None
    out['_vp'] = None
    out['_qyid'] = ''	# user's uuid
    out['_vv_conf'] = None
    # data used when parse video info
    out['_du'] = None	# base url part of before_final_url
    out['_ck_info'] = None	# used with ck token for vv
    # TODO add more data here
    
    return out

def push():
    __old.append(_)

def pop():
    return __old.pop()

# end var.py


