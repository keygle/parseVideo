# method_pc_flash_gate.py, parse_video/lib/e/letv/
from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import (
    id_transfer, 
    gslb_item_data, 
)
try:
    from .o import m3u8_encrypt2 as m3u8_encrypt
except Exception:
    from .o import m3u8_encrypt

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # NOTE --more mode to just get vid_info
    # TODO check use more code may be can clean
    if _check_use_more():
        var._['_use_more'] = True
        raw_more = var._['more']
        # [ OK ] log
        log.o(log_text.method_enable_more())
        # check method
        common.method_more_check_method(method_arg_text, raw_more)
    # process method args
    def rest(r):
        if r == 'fast_parse':
            var._['flag_fast_parse'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    
    # TODO get vid_info code may be cleaned
    # get vid_info from more
    if not var._['_use_more']:
        vid_info = common.parse_load_page_and_get_vid(var)
    else:
        raw_data = raw_more['_data']
        vid_info = raw_data['vid_info']
        # set var._
        var._['_vid_info'] = vid_info
    pvinfo = _get_video_info(vid_info)
    # TODO support fast parse here
    out = _get_file_urls(pvinfo)
    out = _count_and_select(out)	# NOTE count after get file urls
    
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = vid_info
    return out

def _check_use_more():
    data_list = [
        'vid_info', 
    ]
    return common.method_check_use_more(var, data_list)

def _get_video_info(vid_info):
    # make first url
    first_url = id_transfer.get_url(vid_info['vid'])
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['statuscode'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(first['statuscode'], var))
    return common.parse_raw_first(first, _parse_raw_first_json)

def _parse_raw_first_json(first):
    playurl = first['playurl']
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = playurl['title']
    
    # get video list
    domain = playurl['domain']
    dispatch = playurl['dispatch']
    
    vid = playurl['vid']
    out['video'] = [_parse_one_video_info(vid, domain, i) for i in dispatch.items()]
    return out

def _parse_one_video_info(vid, domain, dispatch):
    out = {}
    rateid, raw_dispatch = dispatch
    out['hd'] = var.TO_HD[rateid]
    # set default values
    out['size_px'] = [-1, -1]
    out['format'] = 'ts'	# NOTE video file format should be ts, from m3u8
    
    out['size_byte'] = -1
    out['time_s'] = -1
    out['count'] = -1
    out['file'] = []
    # only save raw data here
    out['_data'] = {}
    out['_data']['rateid'] = rateid
    # NOTE use domain[0]
    d = domain[0]
    # gen video info URL
    raw_url = d + raw_dispatch[0]
    out['_data']['url'] = gslb_item_data.gen_before_url(raw_url, vid, rateid)
    return out

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

def _get_file_urls(pvinfo):
    # TODO support fast parse mode
    
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
                v['_data'] = m3u8_encrypt.decode(v['_data'])
    except Exception as e:
        er = err.MethodError('decoding letv m3u8 blob failed')
        raise er from e
    
    # DEBUG log, parse m3u8 and update video info
    log.d('parse letv m3u8 text to get video info ')
    try:
        for v in pvinfo['video']:
            if '_data' in v:
                raw = _parse_m3u8(v['_data'])
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
    if raw_before['status'] != var.BEFORE_OK_CODE:
        raise err.MethodError('before json status code \"' + str(raw_before['status']) + '\" is not ' + str(var.BEFORE_OK_CODE) + ' ')
    location = raw_before['location']
    log.d('got final m3u8 location \"' + location + '\" ')
    raw_m3u8 = b.dl_blob(location)
    return raw_m3u8

# parse letv's m3u8 file text
def _parse_m3u8(raw):
    # check raw text
    check_list = [
        '#EXTM3U', 
        '#EXT-X-VERSION:3', 
        '#EXT-LETV-M3U8-TYPE:VOD', 
        '#EXT-LETV-M3U8-VER:ver_00_22', 
    ]
    for c in check_list:
        if not c in raw:
            raise err.ParseError('letv m3u8 file format bad, not exist key value', c)
    lines = raw.splitlines()
    out = {}
    # parse head lines, get size_px
    out['size_px'] = [-1, -1]
    while len(lines) > 0:
        line, lines = lines[0], lines[1:]
        if line.startswith('#EXT-LETV-START-TIME:'):
            break
        elif line.startswith('#EXT-LETV-PIC-WIDTH:'):
            out['size_px'][0] = int(line.split(':', 1)[1])
        elif line.startswith('#EXT-LETV-PIC-HEIGHT:'):
            out['size_px'][1] = int(line.split(':', 1)[1])
    # get file info, use base m3u8 parse function
    out['file'] = b.simple_m3u8_parse(lines)
    for f in out['file']:	# get size from url
        filename = f['url'].split('?', 1)[0].rsplit('/', 1)[1]
        size = filename.split('_')[-2]
        f['size'] = int(size)	# update size
    return out

# end method_pc_flash_gate.py


