# var.py, parse_video/lib/e/tvsohu/
from .. import common

# static data
EXTRACTOR_ID = 'tvsohu'
EXTRACTOR_NAME = 'tvsohu_1'
SITE = 'tvsohu'
SITE_NAME = '搜狐视频'

RE_SUPPORT_URL = [
    # TODO
    '', 
]

METHOD_LIST = [
    'pc_flash_gate', 
]
RE_VID_LIST = {
    'vid' : '', 	# TODO
}
# site vid_type to parse_video hd quality
TO_HD = {	# TODO
    '' : , 
    '' : , 
}
FIRST_OK_CODE = ''	# TODO

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


