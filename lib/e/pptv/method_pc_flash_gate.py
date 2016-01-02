# method_pc_flash_gate.py, parse_video/lib/e/pptv/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method
from .o import (
    vod_play_proxy, 
    ctx_query, 
    play_info, 
)

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    method.get_raw_more(method_arg_text)
    # parse method args
    def rest(r):
        if r == 'get_title_no':
            var._['flag_get_title_no'] = True
        else:	# unknow method arg
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    vid_info = method.get_vid_info()
    
    # get video info and file URLs
    pvinfo = _get_video_info(vid_info)
    # NOTE already got file URLs here
    out = method.check_enable_more(pvinfo)
    return out

def _get_video_info(vid_info):
    # TODO support get_title_no here
    first_url = _make_first_url(vid_info)
    first = method.dl_first_xml(first_url)
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
    out, channel = method.raw_first_get_base_info(first)
    
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
            f['size'] = int(s.get('fs'))
            f['time_s'] = float(s.get('dur'))
            # NOTE gen file URL here
            server = data['dt'].find('bh').findtext('.')
            filename = data['item'].get('rid')
            index = int(s.get('no'))
            more = {}
            more['k'] = data['dt'].find('key').findtext('.')
            more['key'] = play_info.gen_key()
            f['url'] = play_info.make_cdn_url(server, filename, index, more=more)
            one['file'].append(f)
        out['video'].append(one)
    return out

# end method_pc_flash_gate.py


