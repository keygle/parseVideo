# method_pc_flash_gate.py, parse_video/lib/e/hunantv/

from ... import err, b
from .. import common

from . import method
from .var import var
from .o import mango_tv3

class Method(method.Method):
    def _init_data(self):
        self._format = 'm3u8'   # NOTE the type should be m3u8
    
    def _parse_arg_rest(self, r):
        if r == 'parse_m3u8':
            var._['flag_parse_m3u8'] = True
        else:	# unknow args
            return True
    
    def _get_video_info(self, vid_info):
        out = super()._get_video_info(vid_info)
        # NOTE select hd here
        common.method_select_hd(out, var)
        return out
    
    def _gen_before_url(self, s_url):
        return mango_tv3.gen_before_url(s_url)
    
    def _get_file_urls(self, pvinfo):
        def worker(f, i):
            raw = f['url']
            before = b.dl_json(raw)
            # check code
            if before['status'] != var._BEFORE_OK_CODE:
                raise err.MethodError('before code ' + b.str_or_str(before['status']) + ' is not ' + str(var._BEFORE_OK_CODE) + ' ')
            f['url'] = before['info']	# update URL
            return f
        pool_size = var._['pool_size']['get_before']
        return common.simple_get_file_urls(pvinfo, worker, msg='getting m3u8 file URLs', pool_size=pool_size)
    
    def _extra_process(self, pvinfo):
        # TODO support parse m3u8 and count here
        return pvinfo
# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


