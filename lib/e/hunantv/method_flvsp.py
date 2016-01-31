# method_flvsp.py, parse_video/lib/e/hunantv/

from ... import err, b
from .. import common

from . import method
from .var import var
from .o import mango_tv3

class Method(method.Method):
    def _init_data(self):
        self._format = 'mp4'    # NOTE the file format should be mp4
    
    def _parse_arg_rest(self, r):
        if r == 'fix_size':
            var._['flag_fix_size'] = True
        else:
            return True
    
    def _gen_before_url(self, s_url):
        return _gen_one_file_url(s_url)
    
    def _extra_process(self, pvinfo):
        if var._['flag_fix_size']:	# check fix_size
            pass	# TODO
        return pvinfo
    # end Method class

## base parse functions

def _gen_one_file_url(raw):
    # static data
    INSERT1 = '/vod.do?fmt=4&pno=1021'
    
    # get info from raw url
    a, q = raw.split('?', 1)
    p, rest = a.split('://', 1)
    r_host, f = rest.split('/', 1)
    host = p + '://' + r_host
    filepath = '/' + f.rsplit('/', 1)[0]
    info = {}
    for r in q.split('&'):
        key, value = r.split('=', 1)
        info[key] = value
    # get final URL
    out = host + INSERT1
    out += '&fid=' + info['fid']
    out += '&file=' + filepath
    return out

# exports
_method = Method(var)
parse = _method.parse
# end method_flvsp.py


