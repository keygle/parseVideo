# var.py, parse_video/lib/e/youku/
from .. import common

# TODO re-write for parse_video -> version 0.6.0.0

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
    # TODO
}
# site TODO to parse_video hd quality
TO_HD = {
    # TODO
}
FIRST_OK_CODE = ''	# TODO

# var data
class VarData(common.ExtractorVar):
    def init(self):
        out = super().init()
        # config items
        out['pool_size']['get_file_url'] = 16
        
        # private data
        out['_raw_first_json'] = ''
        return out
# var exports
var = VarData()
_ = var._
# end var.py


