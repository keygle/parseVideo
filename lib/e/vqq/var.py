# var.py, parse_video/lib/e/vqq/
from .. import common
from ... import conf

class Var(common.ExtractorVar):
    # static data
    EXTRACTOR_ID = 'vqq'
    EXTRACTOR_NAME = 'vqq_1'
    SITE = 'v2q'
    SITE_NAME = '疼X视频'
    
    RE_SUPPORT_URL = [
        '^http://v\.qq\.com/.+', 
    ]
    
    METHOD_LIST = [
        'pc_flash_gate', 
    ]
    RE_VID_LIST = {	# NOTE not normal method
        'title_short' : '\ntitle[ :]+"([^"]+)"', 
        'title_sub' : '\nsecTitle[ :]+"([^"]+)"', 
        'title_no' : '\ntitle[ :]+"([^"]+)"', 
        'vid' : '\nvid[ :]+"([^"]+)"', 
    }
    # site fmt to parse_video hd quality
    TO_HD = {
        'fhd' : 4, 		# id : 10209, 蓝光;(1080P)	1080p
        'shd' : 2, 		# id : 10401, 超清;(720P)	720p
        'hd' : 0, 		# id : 10412, 高清;(480P)	普清
        
        # these low quality video, not well support now
        'flv' : -1, 	# id : 1, 高清;(360P)		低清
        'mp4' : -1, 	# id : 2, 高清;(360P)		低清
        'sd' : -3, 		# id : 10203, 标清;(270P)	渣清
    }
    _FIRST_OK_CODE = None	# TODO
    
    # base POST headers, NOTE may be no need
    _BASE_POST_HEADER = {
        'X-Requested-With' : 'ShockwaveFlash/20.0.0.228', 
    }
    
    _DEFAULT_PLATFORM = 11
    _DEFAULT_UTYPE = 0
    
    def _add_more_data(self, out):  # var data
        # config items
        out['pool_size']['get_formats'] = 8
        out['pool_size']['get_file_url'] = 16
        out['pool_size']['fix_1080p'] = 16
        
        out['platform'] = self._DEFAULT_PLATFORM
        out['utype'] = self._DEFAULT_UTYPE
        out['fmt_black_list'] = conf.E_VQQ_FMT_BLACK_LIST
        
        out['flag_fast_parse'] = False
        out['flag_fix_1080p'] = False
        out['flag_ignore_fix_1080p_error'] = False
        out['flag_enable_fmt_black_list'] = False
        out['flag_add_raw_quality'] = False
        # private data
        out['_raw_first_xml'] = {}	# NOTE there will be many first xml info here
        out['_raw_xml_root'] = {}	# save first xml root here
        out['_server_list'] = None
        out['_limit_list'] = {}		# limit info, for fix_1080p
        return out
# var exports
var = Var()
# end var.py


