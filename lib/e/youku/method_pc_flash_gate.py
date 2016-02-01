# method_pc_flash_gate.py, parse_video/lib/e/youku/

from ... import err, b
from ...b import log
from .. import common

from .var import var
# TODO

class Method(common.ExtractorMethod):
    
    def _parse_arg_rest(self, r):
        # TODO support more method args
        return True
    
    def _get_video_info(self, vid_info):
        
        # TODO
        pass
    
    def _make_first_url(self, vid_info):
        
        # TODO
        pass
    
    def _do_parse_first(self, first):
        
        # TODO
        pass
    
    def _get_file_urls(self, pvinfo):
        
        # TODO
        pass
    
    # TODO
    # end Method class

# base parse functions

# TODO
# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


