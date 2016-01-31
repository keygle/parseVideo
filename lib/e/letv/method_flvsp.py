# method_flvsp.py, parse_video/lib/e/letv/

from ... import err, b
from ...b import log
from .. import common, log_text

from .var import var
from . import method
from .o import id_transfer
from .vv import vv_default

class Method(method.Method):
    # static data
    _FLVSP_PLATID = 1
    _FLVSP_SPLATID = 104
    
    def _make_first_url(self, vid_info):
        first_url = id_transfer.get_url(vid_info['vid'], platid=self._FLVSP_PLATID, splatid=self._FLVSP_SPLATID)
        return first_url
    
    def _parse_one_video(self, vid, domain, dispatch):
        one = super()._parse_one_video(vid, domain, dispatch)
        one['format'] = 'mp4'	# NOTE file format here should be mp4
        
        rateid, raw = dispatch
        # get the only one file URL
        one['file'] = []
        f = {}
        f['time_s'], f['size'] = _get_file_info(raw[1])
        raw_url = domain[0] + raw[0]
        f['url'] = _gen_one_file_url(raw_url)
        one['file'].append(f)
        # NOTE add _data
        one['_data'] = {
            'filename' : raw[1], 
        }
        return one
    
    def _get_file_urls(self, pvinfo):
        # check flag_v
        if var._['flag_v']:
            pvinfo = _add_args(pvinfo)
        common.method_count_videos(pvinfo)	# NOTE just count, not select
        # remove _data in video
        for v in pvinfo['video']:
            if '_data' in v:
                v.pop('_data')
        return pvinfo
    # end Method class

# base parse functions

# get file URLs

def _get_file_info(raw):
    raw = raw.rsplit('/', 1)[1].rsplit('.', 1)[0]
    p = raw.split('-')
    time, size = p[-4], p[-3]
    time_s = int(time) / 1e3
    return time_s, int(size)

def _gen_one_file_url(raw):
    # NOTE replace '&tss=ios&' to '&tss=no&'
    a, b = raw.split('&tss=', 1)
    out = a + '&tss=no&' + b.split('&', 1)[1]
    return out

# add args for vv
def _add_args(pvinfo, a_idx=''):
    # INFO log
    log.i('adding args for vv ')
    # TODO clean code here
    # TODO use map_do() here
    # TODO Error process
    pid = var._['_vid_info']['pid']
    for v in pvinfo['video']:
        if not '_data' in v:
            continue
        d = v['_data']
        filename = d['filename']
        f = v['file'][0]
        f['url'] = vv_default.make_one_url(f['url'], pid, filename, a_idx=a_idx)
    return pvinfo

# exports
_method = Method(var)
parse = _method.parse
# end method_flvsp.py


