# var.py, parse_video/lib/

# static data

## for lyyc_parsev struct
PVINFO_MARK_UUID = 'd089503d-5ad5-4008-aea1-f2504f95a41a'
PVINFO_PORT_VERSION = '0.4.0'
PVINFO_INFO_SOURCE = 'parse_video version 0.5.2.2'

HD_TO_QUALITY = {
    11 : '8K', 
    
    8 : '高码4K', 
    7 : '4K', 
    
    5 : '高码1080p', 
    4 : '1080p', 
    
    2 : '720p', 
    
    0 : '普清', 
    -1 : '低清', 
    
    -3 : '渣清', 
    -4 : '超渣', 
    -5 : '极其渣', 
    -6 : '无语渣', 
    -7 : '渣的无法形容', 
}

# var data
_ = {}

_var_init_flag = False
# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    
    # config items
    out['hd_min'] = None
    out['hd_max'] = None
    out['i_min'] = None
    out['i_max'] = None
    
    out['more'] = None
    
    out['flag_no_restruct'] = False
    
    # private data
    out['_extractor_id'] = ''
    
    # set default data done
    return out

# base var functions
def push():
    __old.append(_)
def pop():
    return __old.pop()
# end var.py


