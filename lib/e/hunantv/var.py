# var.py, parse_video/lib/e/hunantv/
from .. import common

# static data
EXTRACTOR_ID = 'hunantv'
EXTRACTOR_NAME = 'hunantv_1'
SITE = 'hunantv'
SITE_NAME = ''	# TODO

RE_SUPPORT_URL = [
    '', 	# TODO
]

METHOD_LIST = [
    'pc_flash_gate', 
]
RE_VID_LIST = {
    'vid' : '', 	# TODO
}
# site stream_name to parse_video hd quality
TO_HD = {	# TODO
    '' : 2, 	# 720p
    '' : 0, 
    '' : -1, 
}
FIRST_OK_CODE = 	# TODO
BEFORE_OK_CODE = 	# TODO

# var data
class VarData(common.ExtractorVar):
    def init(self):
        out = super().init()
        # config items
        out['pool_size']['get_before'] = 4
        out['pool_size']['get_m3u8'] = 4
        
        out['flag_fast_parse'] = False	# TODO
        out['flag_parse_m3u8'] = False	# TODO
        # private data
        out['_raw_first_json'] = ''
        return out
# var exports
var = VarData()
_ = var._
# end var.py


