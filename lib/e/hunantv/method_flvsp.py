# method_flvsp.py, parse_video/lib/e/hunantv/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method
from .o import mango_tv3

# method_flvsp.parse(), entry function
def parse(method_arg_text):
    method.get_raw_more(method_arg_text)
    # process method args
    def rest(r):
        if r == 'fix_size':
            var._['flag_fix_size'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    vid_info = method.get_vid_info()
    
    pvinfo = method.get_video_info(vid_info, _parse_raw_first_json)
    # NOTE already got file URLs
    if var._['flag_fix_size']:	# check fix_size
        pass	# TODO
    out = method.check_enable_more(pvinfo)
    return out

def _parse_raw_first_json(first):
    out, data, info = method.raw_first_get_base_info(first)
    # get video list
    duration, stream = float(info['duration']), data['stream']
    out['video'] = []
    for s in stream:
        one = {}
        one['hd'] = var.TO_HD[s['name']]
        # set default values
        one['format'] = 'mp4'	# NOTE the file format should be mp4
        one['size_px'] = [-1, -1]
        one['size_byte'] = -1
        one['time_s'] = duration
        one['count'] = 1
        # add the only file info
        one['file'] = []
        f = {}
        f['size'] = -1
        f['time_s'] = duration
        f['url'] = _gen_one_file_url(s['url'])
        
        one['file'].append(f)
        out['video'].append(one)
    return out

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

# end method_flvsp.py


