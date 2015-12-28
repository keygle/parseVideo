# method_pc_flash_gate.py, parse_video/lib/e/letv/

import re

from ... import err, b
from ...b import log

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
    # TODO support --more
    # process method args
    if method_arg_text != None:
        args = method_arg_text.split(',')
        for r in args:
            if r == 'fast_parse':
                var._['flag_fast_parse'] = True
            elif r == 'enable_more':
                var._['enable_more'] = True
            else:	# unknow arg
                log.w('unknow method arg \"' + r + '\" ')
    raw_url = var._['_raw_url']
    # INFO log
    log.i('loading page \"' + raw_url + '\" ')
    raw_html_text = b.dl_html(raw_url)
    var._['_raw_page_html'] = raw_html_text
    
    vid_info = _get_vid_info(raw_html_text)
    var._['_vid_info'] = vid_info
    # DEBUG log
    log.d('got vid_info ' + str(vid_info))
    
    pvinfo = _get_video_info(vid_info)
    # TODO support fast parse here
    out = _get_file_urls(pvinfo)
    # NOTE count after get file urls
    out = _count_and_select(out)
    return out

def _get_vid_info(raw_html_text):
    re_list = var.RE_VID_LIST
    try:
        out = {}
        for key, r in re_list.items():
            one = re.findall(r, raw_html_text)[0]
            # check empty result
            if (one == None) or (one == ''):
                raise err.ParseError('vid_info \"' + key + '\" empty', one)
            out[key] = one
        return out
    except Exception as e:
        er = err.NotSupportURLError('get vid info failed', var._['_raw_url'])
        raise er from e

def _get_video_info(vid_info):
    first_url = _make_first_url(vid_info)
    # [ OK ] log
    log.o('got first URL \"' + first_url + '\" ')
    first = b.dl_json(first_url)
    var._['_raw_first_json'] = first
    # check code
    if first['statuscode'] != var.FIRST_OK_CODE:
        raise err.MethodError('first_json status code \"' + first['statuscode'] + '\" is not ' + var.FIRST_OK_CODE + ' ')
    # TODO
    # parse raw first json
    try:
        pvinfo = _parse_raw_first_json(first)
    except Exception as e:
        er = err.MethodError('parse raw first json info failed')
        raise er from e
    # sort videos by hd
    pvinfo['video'].sort(key=lambda x:x['hd'], reverse=True)
    return pvinfo

def _make_first_url(vid_info):
    vid = vid_info['vid']
    out = id_transfer.get_url(vid)
    return out

def _parse_raw_first_json(first):
    out = {}
    playurl = first['playurl']
    
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
    out['hd'] = var.RATEID_TO_HD[rateid]
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

def _select_and_count(pvinfo):
    # sort videos by hd
    pvinfo['video'].sort(key = lambda x: x['hd'], reverse=True)
    # count video info
    for v in pvinfo['video']:
        # check skip videos
        if len(v['file']) < 1:
            continue
        v['size_byte'] = 0
        v['time_s'] = 0
        v['count'] = len(v['file'])
        for f in v['file']:
            v['size_byte'] += f['size']
            v['time_s'] += f['time_s']
        v['time_s'] = round(v['time_s'], 3)
    # NOTE only select hd_min, hd_max, not select i_min, i_max
    hd_min = var._['hd_min']
    hd_max = var._['hd_max']
    for v in pvinfo['video']:
        if ((hd_min != None) and (v['hd'] < hd_min)) or ((hd_max != None) and (v['hd'] > hd_max)):
            v['file'] = []
    # done
    return pvinfo

def _get_file_urls(pvinfo):
    # TODO support fast parse mode
    # download m3u8
    todo_list = []
    for v in pvinfo['video']:
        if '_data' in v:
            todo_list.append(v['_data'])
    pool_size = var._['pool_size_get_m3u8']
    # INFO log here
    log.i('downloading ' + str(len(todo_list)) + ' m3u8 files, pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo_list, worker=_download_one_m3u8, pool_size=pool_size)
    # DEBUG log here
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
    # DEBUG log
    log.d('rateid [' + rateid + '] load raw before URL \"' + raw_url + '\" ')
    raw_before = b.dl_json(raw_url)
    # check status code
    if raw_before['status'] != var.BEFORE_OK_CODE:
        raise err.MethodError('before json status code \"' + str(raw_before['status']) + '\" is not ' + str(var.BEFORE_OK_CODE) + ' ')
    location = raw_before['location']
    # DEBUG log
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
            out['size_px'][0] = int(line.split(':', 1)[1])
    # get file info
    out['file'] = []
    one = {}
    for line in lines:
        if line.startswith('http://'):	# got url
            one['url'] = line
            # get file size from url
            filename = line.split('?', 1)[0].rsplit('/', 1)[1]
            size = filename.split('_')[-2]
            one['size'] = int(size)
            # add one file and reset one
            out['file'].append(one)
            one = {}
        elif line.startswith('#EXTINF:'):	# got time_s
            time = line.split(':', 1)[1].split(',', 1)[0]
            one['time_s'] = float(time)
        elif line.startswith('#EXT-X-ENDLIST'):	# got m3u8 file end
            return out
    # not get #EXT-X-ENDLIST
    raise err.ParseError('not get m3u8 file end #EXT-X-ENDLIST ')

# end method_pc_flash_gate.py


