# method_flvsp.py, parse_video/lib/e/tvsohu/
from .. import common

from .var import var
from . import method

class Method(method.Method):
    def _init_data(self):
        super()._init_data()
        self._gen_one_before_url = _gen_one_file_url
    # NOTE already got file URLs
    # TODO add more method args

def _gen_one_file_url(su_i, vid=None, tvid=None, ch=None):
    BEFORE = 'http://data.vod.itc.cn/?prod=app&new='
    
    out = BEFORE + su_i
    return out

# exports
_method = Method(var)
parse = _method.parse
# end method_flvsp.py


