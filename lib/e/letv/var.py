# var.py, parse_video/lib/e/letv/
from .. import common

class Var(common.ExtractorVar):
    # static data
    EXTRACTOR_ID = 'letv'
    EXTRACTOR_NAME = 'letv_1'
    SITE = 'letv'
    SITE_NAME = '乐视视频'
    
    RE_SUPPORT_URL = [
        # http://www.letv.com/ptv/vplay/24143557.html
        '^http://www\.letv\.com/.+\.html', 
        # NOTE only for method m3u8
        '^file:///.+\.m3u8$', 	# NOTE support local m3u8 file, TODO may be not stable
        '^http://.+/letv-uts/.+/ver_.+\.m3u8?', 	# NOTE raw m3u8 file URL
    ]
    
    METHOD_LIST = [
        'pc_flash_gate', 
        'flvsp', 
        'm3u8', 
    ]
    RE_VID_LIST = {
        'vid' : ' vid:([0-9]+),', 
        'pid' : ' pid:([0-9]+),', 
    }
    # site rateid to parse_video hd quality
    TO_HD = {
        '1080p' : 4, 	# 1080p
        '720p' : 2, 	# 720p
        '1300' : 0, 	# HD
        '1000' : -1, 	# SD
        '350' : -3, 	# LW
    }
    _FIRST_OK_CODE = '1001'
    _BEFORE_OK_CODE = 200
    
    def _add_more_data(self, out):  # var data
        # config items
        out['pool_size']['get_m3u8'] = 8
        
        out['flag_fast_parse'] = False
        out['flag_v'] = False
        # private data
        out['_raw_first_json'] = ''
        return out
# var exports
var = Var()
# end var.py


