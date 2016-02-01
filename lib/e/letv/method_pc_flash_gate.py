# method_pc_flash_gate.py, parse_video/lib/e/letv/

from ... import err, b
from ...b import log
from .. import common

from .var import var
from . import method
from .o import (
    id_transfer, 
    gslb_item_data, 
)
from .vv import vv_default

class Method(method.Method):
    
    def _parse_arg_rest(self, r):
        if r == 'fast_parse':
            var._['flag_fast_parse'] = True
        else:
            return super()._parse_arg_rest(r)
    
    def _make_first_url(self, vid_info):
        first_url = id_transfer.get_url(vid_info['vid'])
        return first_url
    
    def _get_video_info(self, vid_info):
        pvinfo = super()._get_video_info(vid_info)
        if var._['flag_fast_parse']:	# NOTE support fast_parse here
            pvinfo = _select_fast_parse(pvinfo)
        return pvinfo
    
    def _parse_one_video(self, vid, domain, dispatch):
        out = super()._parse_one_video(vid, domain, dispatch)
        out['format'] = 'ts'	# NOTE video file format should be ts, from m3u8
        
        out['size_byte'] = -1
        out['time_s'] = -1
        out['count'] = -1
        out['file'] = []
        
        rateid, raw_dispatch = dispatch
        # only save raw data here
        out['_data'] = {}
        out['_data']['rateid'] = rateid
        # NOTE use domain[0]
        d = domain[0]
        # gen video info URL
        raw_url = d + raw_dispatch[0]
        out['_data']['url'] = gslb_item_data.gen_before_url(raw_url, vid, rateid)
        out['_data']['filename'] = raw_dispatch[1]	# NOTE add for vv
        return out
    
    def _get_file_urls(self, pvinfo):
        # check flag_v
        if var._['flag_v']:
            pvinfo = vv_default.add_args(pvinfo)
        out = _do_get_file_urls(pvinfo)
        out = _count_and_select(out)	# NOTE count after get file urls
        return out
    # end Method class

# base parse functions

def _select_fast_parse(pvinfo):
    # select by hd
    hd_min, hd_max = var._['hd_min'], var._['hd_max']
    for v in pvinfo['video']:
        if ((hd_min != None) and (v['hd'] < hd_min)) or ((hd_max != None) and (v['hd'] > hd_max)):
            v.pop('_data')
    return pvinfo

def _count_and_select(pvinfo):
    common.method_sort_video(pvinfo)
    # count video info
    for v in pvinfo['video']:
        # check skip videos
        if len(v['file']) < 1:
            continue
        common.method_count_one_video(v)
    # NOTE only select hd_min, hd_max, not select i_min, i_max
    common.method_select_hd(pvinfo, var)
    return pvinfo

# get file urls

def _do_get_file_urls(pvinfo):
    # download m3u8
    todo_list = []
    for v in pvinfo['video']:
        if '_data' in v:
            todo_list.append(v['_data'])
    pool_size = var._['pool_size']['get_m3u8']
    # INFO log here
    log.i('downloading ' + str(len(todo_list)) + ' m3u8 files, pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo_list, worker=_download_one_m3u8, pool_size=pool_size)
    log.d('download m3u8 files done. ')
    i = 0	# set back result
    for v in pvinfo['video']:
        if '_data' in v:
            v['_data'], i = result[i], i + 1
    
    # INFO log, decoding m3u8
    log.i('decoding ' + str(len(result)) + ' m3u8 blobs ')
    try:
        for v in pvinfo['video']:
            if '_data' in v:
                v['_data'] = method.decode_m3u8(v['_data'])
    except Exception as e:
        er = err.MethodError('decoding letv m3u8 blob failed')
        raise er from e
    # DEBUG log, parse m3u8 and update video info
    log.d('parse letv m3u8 text to get video info ')
    try:
        for v in pvinfo['video']:
            if '_data' in v:
                raw = method.parse_m3u8(v['_data'])
                # update video info
                v['size_px'] = raw['size_px']
                v['file'] = raw['file']
                
                v.pop('_data')
                v['format'] = 'ts'	# NOTE reset format here
    except Exception as e:
        er = err.MethodError('parse m3u8 text failed')
        raise er from e
    return pvinfo

def _download_one_m3u8(info):
    rateid = info['rateid']
    url = info['url']
    log.d('rateid [' + rateid + '] load raw before URL \"' + url + '\" ')
    raw_before = b.dl_json(url)
    # check status code
    if raw_before['status'] != var._BEFORE_OK_CODE:
        raise err.MethodError('before json status code \"' + str(raw_before['status']) + '\" is not ' + str(var._BEFORE_OK_CODE) + ' ')
    location = raw_before['location']
    log.d('got final m3u8 location \"' + location + '\" ')
    raw_m3u8 = b.dl_blob(location)
    return raw_m3u8

# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


