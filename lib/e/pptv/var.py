# var.py, parse_video/lib/e/pptv/
from .. import common

# static data
EXTRACTOR_ID = 'pptv'
EXTRACTOR_NAME = 'pptv_1'
SITE = 'pptv'
SITE_NAME = 'PPTV聚力'

RE_SUPPORT_URL = [
    # http://v.pptv.com/show/0UyKCXHXR4XoZs4.html
    '^http://v\.pptv\.com/.+\.html', 
]

METHOD_LIST = [
    'pc_flash_gate', 
    'android', 
]
RE_VID_LIST = {
    'webcfg' : 'var webcfg = ([^;]+);', 
}
# site ft to parse_video hd quality
TO_HD = {
    '4' : 5, 	# high-bitrate 1080p
    '3' : 4, 	# 1080p
    '2' : 2, 	# 720p
    '1' : 0, 	# 普清
    '0' : -1, 	# 低清
}
# NOTE pptv not support FIRST_OK_CODE

# var data
class VarData(common.ExtractorVar):
    def init(self):
        out = super().init()
        # NOTE need pool_size here
        
        # make another http request to get title_no info (use video list)
        out['flag_get_title_no'] = False	# TODO
        # private data
        out['_raw_first_xml'] = ''
        return out
# var exports
var = VarData()
_ = var._
# end var.py


