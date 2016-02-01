# var.py, parse_video/lib/e/youku/
from .. import common

class Var(common.ExtractorVar):
    # static data
    EXTRACTOR_ID = 'youku'
    EXTRACTOR_NAME = 'kill_ccyouku_1'
    SITE = 'youku'
    SITE_NAME = '优酷网'
    
    RE_SUPPORT_URL = [
        '^http://v\.youku\.com/v_show/id_[A-Za-z0-9]+\.html', 
    ]
    
    METHOD_LIST = [
        'pc_flash_gate', 
    ]
    RE_VID_LIST = {
        # NOTE http://v.youku.com/v_show/id_XMTA3MDAzMDM2.html
        'vid' : 'v\.youku\.com/v_show/id_([A-Za-z0-9]+)\.html', 
        # TODO support more URL types
    }
    # site stream_type to parse_video hd quality
    TO_HD = {
        'mp4hd3' : 4, 	# 1080p, about 1920x1080
        'mp4hd2' : 2, 	# 720p, about 1104x622
        'mp4hd' : -1, 	# about 672x378
        'flvhd' : -3, 	# about 512x288
    }
    _FIRST_OK_CODE = 0
    
    
    def _add_more_data(self, out):	# var data
        # config items
        out['pool_size']['get_file_url'] = 16
        
        # private data
        out['_raw_first_json'] = ''
        out['_parse_more'] = None	# more data for next parse
        return out
# var exports
var = Var()
# end var.py


