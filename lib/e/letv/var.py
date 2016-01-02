# var.py, parse_video/lib/e/letv/
from .. import common

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
    'flvsp', 
]
RE_VID_LIST = {
    'vid' : ' vid:([0-9]+),', 
}
# site rateid to parse_video hd quality
TO_HD = {
    '1080p' : 4, 	# 1080p
    '720p' : 2, 	# 720p
    '1300' : 0, 	# HD
    '1000' : -1, 	# SD
    '350' : -3, 	# LW
}
FIRST_OK_CODE = '1001'
BEFORE_OK_CODE = 200

# var data
class VarData(common.ExtractorVar):
    def init(self):
        out = super().init()
        # config items
        out['pool_size']['get_m3u8'] = 8
        
        out['flag_fast_parse'] = False
        # private data
        out['_raw_first_json'] = ''
        return out
# var exports
var = VarData()
_ = var._
# end var.py


