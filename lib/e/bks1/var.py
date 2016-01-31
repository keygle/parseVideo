# var.py, parse_video/lib/e/bks1/
from .. import common

class Var(common.ExtractorVar):
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
        # TODO
        'cdn_only_key', 
    ]
    RE_VID_LIST = {
        'tvid' : 'data-player-tvid="([^"]+)"', 
        'vid'  : 'data-player-videoid="([^"]+)"', 
        
        'flag_vv' : 'data-player-ismember="([^"]+)"', 
    }
    _RE_VID_LIST2 = {	# NOTE aid may be empty
        'aid'  : 'data-player-albumid="([^"]+)"', 
    }
    # site video bid to parse_video hd quality
    TO_HD = {	# video bid to video hd
        10 : 7, 	# 4k, 		4K
        5 : 4, 	# fullhd, 	1080p
        4 : 2, 	# super-high, 	720p
        3 : 1, 	# super, 	高清
        2 : 0, 	# high, 	普清
        1 : -1, 	# standard, 	低清
        0 : -2, 	# none, 	超低清
        96 : -3, 	# topspeed, 	渣清
    }
    _FIRST_OK_CODE = 'A000000'
    
    
    def _add_more_data(self, out):	# var data
        # config items
        out['pool_size']['get_file_url'] = 16
        out['pool_size']['vv_get_token'] = 1	# FIXME only for DEBUG now, set to 1
        
        out['set_um'] = False
        out['set_vv'] = False
        out['flag_v'] = False	# NOTE for vv
        out['flag_fix_4k'] = False
        
        out['flag_enable_vv_error'] = False
        # private data
        out['_raw_first_json'] = ''
        return out
# var exports
var = Var()
# end var.py


