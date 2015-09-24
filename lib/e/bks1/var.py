# var.py, parse_video/lib/e/bks1
# version 0.0.3.0 test201509241303

'''
parse_video/lib/e/bks1/var.py
    global common data for extractor bks1
part of standard port for parse_video extractor
'''

# static data

RE_SUPPORT_URL = [
    '^http://[a-z]+\.iqiyi\.com/.+\.html', 
]

RE_VID_LIST = {
    'vid' : 'data-(player|drama)-videoid="([^"]+)"', 
    'tvid' : 'data-(player|drama)-tvid="([^"]+)"', 
    'aid' : 'data-(player|drama)-albumid="([^"]*)"', 
    'flag_vv' : 'data-(player|drama)-ismember="([^"]+)"', 
}
RE_VID_LIST_FIX = 1

# var data
_ = {}

# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    # set default values
    out['raw_arg'] = ''		# this is used to pass raw_arg to extractor
    out['raw_method'] = ''	# this is used to pass raw_method to extractor
    
    out['flag_v'] = False
    out['flag_v_force'] = False
    
    # private data
    out['_raw_url'] = ''
    out['_raw_page_html'] = ''
    out['_vid_info'] = None
    out['_first_url'] = ''
    out['_raw_vms_json'] = ''
    out['_vms_json'] = None
    out['_vp'] = None
    # TODO add more data here
    
    return out

def push():
    __old.append(_)

def pop():
    return __old.pop()

# end var.py


