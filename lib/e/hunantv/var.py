# var.py, parse_video/lib/e/hunantv/
from .. import common

class Var(common.ExtractorVar):
    # static data
    EXTRACTOR_ID = 'hunantv'
    EXTRACTOR_NAME = 'hunantv_1'
    SITE = 'hunantv'
    SITE_NAME = '芒果TV'
    
    RE_SUPPORT_URL = [
        # http://www.hunantv.com/v/2/168868/f/2928760.html
        '^http://www\.hunantv\.com/.+\.html', 
    ]
    
    METHOD_LIST = [
        'pc_flash_gate', 
        'flvsp', 
    ]
    RE_VID_LIST = {
        'vid' : 'data-vid="([^"]+)"', 
    }
    # site stream_name to parse_video hd quality
    TO_HD = {
        '超清' : 2, 	# 720p
        '高清' : 0, 
        '标清' : -1, 
    }
    _FIRST_OK_CODE = 200
    _BEFORE_OK_CODE = 'ok'
    
    def _add_more_data(self, out):	# var data
        # config items
        out['pool_size']['get_before'] = 4
        out['pool_size']['get_m3u8'] = 4
        
        out['flag_parse_m3u8'] = False	# TODO
        out['flag_fix_size'] = False	# TODO for method flvsp, fix file size
        # private data
        out['_raw_first_json'] = ''
        return out
# var exports
var = Var()
# end var.py


