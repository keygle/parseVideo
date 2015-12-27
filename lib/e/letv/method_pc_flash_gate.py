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
        # TODO support more args
        pass
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
    # TODO may be more works here
    out = _get_file_urls(pvinfo)
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
    # TODO support select and count, now not support it
    # NOTE sort videos by hd
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

def _get_file_urls(pvinfo):
    # FIXME DEBUG here, only output raw m3u8, not do actually parse
    for v in pvinfo['video']:
        # TODO use map_do to get info
        rateid = v['_data']['rateid']
        raw_url = v['_data']['url']
        # DEBUG log
        log.d('DEBUG: rateid [' + rateid + '] load raw before URL \"' + raw_url + '\" ')
        raw_before = b.dl_json(raw_url)
        # check status code
        if raw_before['status'] != var.BEFORE_OK_CODE:
            raise err.MethodError('before json status code \"' + str(raw_before['status']) + '\" is not ' + str(var.BEFORE_OK_CODE) + ' ')
        location = raw_before['location']
        # DEBUG log
        log.d('got final m3u8 location \"' + location + '\" ')
        raw_m3u8 = b.dl_blob(location)
        # DEBUG log
        log.d('DEBUG: decoding m3u8 blob ')
        m3u8_text = m3u8_encrypt.decode(raw_m3u8)
        
        # FIXME DEBUG here
        # NOTE write to tmp file for DEBUG
        filename = rateid + '.tmp.m3u8'
        with open(filename, 'wt') as f:
            f.write(m3u8_text)
        # DEBUG log
        log.d('DEBUG: write to debug tmp file \"' + filename + '\" ')
    # FIXME TODO DEBUG here
    return pvinfo

# end method_pc_flash_gate.py


