# method_pc_flash_gate.py, parse_video/lib/e/tvsohu/

from ... import err, b
from .. import common

from .var import var
from . import method
from .o import main

class Method(method.Method):
    def _init_data(self):
        super()._init_data()
        # set gen_one_before_url
        self._gen_one_before_url = _gen_one_before_url
    
    def _parse_arg_rest(self, r):
        if r == 'fast_parse':
            var._['flag_fast_parse'] = True
        elif r == 'gen_header':
            var._['flag_gen_header'] = True
        else:
            return True
    
    def _get_file_urls(self, pvinfo):
        out = _do_get_file_urls(pvinfo)
        out = _add_headers(out)
        return out
    # end Method class

# base parse functions

def _gen_one_before_url(su_i, vid, tvid, ch):
    return main.gen_before_url(su_i, vid, tvid, ch)

# get file urls

def _do_get_file_urls(pvinfo):
    def worker(f, i):
        raw = b.dl_json(f['url'])
        try:
            f['url'] = raw['url']	# update URL
            return f
        except Exception as e:
            er = err.MethodError('get final file URL failed', f['url'])
            raise er from e
    pool_size = var._['pool_size']['get_final']
    return common.simple_get_file_urls(pvinfo, worker, msg='getting part file URLs', pool_size=pool_size)

def _add_headers(pvinfo):
    # NOTE add type and user_agent header for each file
    user_agent = main.gen_user_agent()
    file_type = var._TVSOHU_FILE_TYPE
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                f['header'] = {
                    'User-Agent' : user_agent, 
                }
                f['type'] = file_type
    # NOTE support gen_header method arg
    if var._['flag_gen_header']:
        for v in pvinfo['video']:
            for f in v['file']:
                if f['url'] != '':	# NOTE Range only for example
                    f['header']['Range'] = 'bytes=0-' + str(f['size'] - 1)
    return pvinfo

# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


