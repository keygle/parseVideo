# method_flvsp.py, parse_video/lib/e/tvsohu/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method

# method_flvsp.parse(), entry function
def parse(method_arg_text):
    method.get_raw_more(method_arg_text)
    # process method args
    def rest(r):
        return True	# NOTE no more args here
    common.method_parse_method_args(method_arg_text, var, rest)
    vid_info = method.get_vid_info()
    
    pvinfo = method.get_video_info(vid_info, _gen_one_file_url)
    # NOTE already got file URLs
    out = method.count_and_select(pvinfo)
    out = method.check_enable_more(out)
    return out

def _gen_one_file_url(su_i, vid=None, tvid=None, ch=None):
    BEFORE = 'http://data.vod.itc.cn/?prod=app&new='
    
    out = BEFORE + su_i
    return out

# end method_flvsp.py


