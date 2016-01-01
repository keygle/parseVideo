# method_pc_flash_gate.py, parse_video/lib/e/pptv/

import json
import xml.etree.ElementTree as ET

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import (
    vod_play_proxy, 
    ctx_query, 
    play_info, 
)

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # TODO support --more
    # parse method args
    def rest(r):
        if r == 'get_title_no':
            var._['flag_get_title_no'] = True
        else:	# unknow method arg
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    # load page and get vid info
    vid_info = common.parse_load_page_and_get_vid(var, _get_vid_info)
    
    # get video info and file URLs
    pvinfo = _get_video_info(vid_info)
    out = _get_file_urls(pvinfo)
    # TODO support enable_more
    return out

def _get_vid_info(raw_html_text):
    def do_get(raw_html_text):
        out = common.method_vid_re_get(raw_html_text, var.RE_VID_LIST)
        try:	# parse webcfg as json
            out['webcfg'] = json.loads(out['webcfg'])
        except Exception as e:
            er = err.MethodError('parse webcfg json text failed', out['webcfg'])
            raise er from e
        # get more info from webcfg
        cfg = out['webcfg']
        out['cid'] = cfg['id']
        out['ctx'] = cfg['player']['ctx']
        return out
    return common.method_get_vid_info(raw_html_text, var, do_get)

def _get_video_info(vid_info):
    # TODO support get_title_no here
    first_url = _make_first_url(vid_info)
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    # NOTE download and parse as xml
    first_xml = b.dl_html(first_url)
    var._['_raw_first_xml'] = first_xml	# save raw xml text
    try:
        first  = ET.fromstring(first_xml)
    except Exception as e:
        er = err.ParseXMLError('parse first xml text failed, first_url ', first_url)
        er.text = first
        raise er from e
    # check first Error
    if first.find('error') != None:
        raise err.MethodError('first xml info Error', ET.dump(first.find('error')))
    vid_info['vip'] = str(first.find('channel').get('vip'))
    # parse first info
    pvinfo = common.parse_raw_first(first, _parse_raw_first_info)
    out = common.method_simple_count_and_select(pvinfo, var)
    return out

def _make_first_url(vid_info):
    # reset and set ctx
    ctx_query.ctx.clear()
    ctx_query.setCTX(vid_info['ctx'])
    # make first url
    cid = vid_info['cid']
    return vod_play_proxy.get_play_url(cid)

def _parse_raw_first_info(first):
    channel = first.find('channel')
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = channel.get('nm')
    out['info']['title_short'] = channel.get('hjnm')
    
    # collect info by ft, NOTE ft as str
    info = {}
    # get channel.file[]item
    file_item = channel.find('file').findall('item')
    for i in file_item:
        ft = str(i.get('ft'))
        if not ft in info:
            info[ft] = {}
        info[ft]['item'] = i
    # get dt and dragdata
    dt_list = first.findall('dt')
    for dt in dt_list:
        ft = str(dt.get('ft'))
        info[ft]['dt'] = dt
    dragdata = first.findall('dragdata')
    for d in dragdata:
        ft = str(d.get('ft'))
        info[ft]['drag'] = d
    # gen video info
    out['video'] = []
    for ft, data in info.items():
        one = {}
        one['hd'] = var.TO_HD[str(ft)]
        drag = data['drag']
        px_x = int(drag.get('vw'))
        px_y = int(drag.get('vh'))
        one['size_px'] = [px_x, px_y]
        one['format'] = 'mp4'	# NOTE the video file format should be mp4
        
        # gen file list
        sgm = drag.findall('sgm')
        one['file'] = []
        for s in sgm:
            f = {}
            f['time_s'] = float(s.get('dur'))
            f['size_byte'] = int(s.get('fs'))
            # TODO gen file URL here
            f['url'] = ''
            one['file'].append(f)
        out['video'].append(one)
    return out

# TODO maybe no need this
def _get_file_urls(pvinfo):
    return pvinfo
    # TODO not finished now
    pass

# end method_pc_flash_gate.py


