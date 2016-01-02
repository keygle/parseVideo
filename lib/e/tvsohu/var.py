# var.py, parse_video/lib/e/tvsohu/
from .. import common

# static data
EXTRACTOR_ID = 'tvsohu'
EXTRACTOR_NAME = 'tvsohu_1'
SITE = 'tvsohu'
SITE_NAME = '搜狐视频'

RE_SUPPORT_URL = [
    # http://tv.sohu.com/20140914/n404300963.shtml
    '^http://tv\.sohu\.com/.+\.shtml', 
]

METHOD_LIST = [
    'pc_flash_gate', 
    'flvsp', 
]
RE_VID_LIST = {
    'vid' : 'var vid="([0-9]+)";', 
}
# site vid_type to parse_video hd quality
TO_HD = {
    'h2654kVid'    : 7.1, 	# 4K, h265
    'h2654mVid'    : 5.1, 	# high bitrate 1080p, h265
    'h265oriVid'   : 4.1, 	# 1080p, h265
    'h265superVid' : 2.1, 	# 720p, h265
    'h265highVid'  : 0.1, 
    'h265norVid'   : -0.9, 
    
    'h2644kVid' : 7, 	# 4K, h264
    'oriVid'    : 4, 	# 1080p
    'superVid'  : 2, 	# 720p
    'highVid'   : 0, 
    'norVid'    : -1, 
}
FIRST_OK_CODE = 1	# first.status

# vid_name to quality text
VID_NAME_LIST = {
    'h2654kVid'    : 'h265', 
    'h2654mVid'    : 'h265', 
    'h265oriVid'   : 'h265', 
    'h265superVid' : 'h265', 
    'h265highVid'  : 'h265', 
    'h265norVid'   : 'h265', 
    
    'h2644kVid' : None, 
    'oriVid'    : None, 
    'superVid'  : None, 
    'highVid'   : None, 
    'norVid'    : None, 
}
TVSOHU_FILE_TYPE = [
    'pv_tvsohu_http', 
]

# var data
class VarData(common.ExtractorVar):
    def init(self):
        out = super().init()
        # config items
        out['pool_size']['get_first'] = 8
        out['pool_size']['get_final'] = 16
        
        out['flag_fast_parse'] = False	# TODO
        out['flag_gen_header'] = False
        # private data
        out['_raw_first_json'] = {}	# NOTE there will be many first jsons
        return out
# var exports
var = VarData()
_ = var._
# end var.py


