# method_pc_flash_gate.py, parse_video/lib/e/youku/
# TODO support many other parse format, youku is not very easy

import re

from ... import err, b
from ...b import log
from .. import common, log_text

from .var import var
from .o import get_url, play_service_proxy

class Method(common.ExtractorMethod):
    
    def _parse_arg_rest(self, r):
        # TODO support more method args
        return True
    
    def _do_get_vid_info(self):
        raw_url = var._['_raw_url']
        # NOTE just get vid from URL, not download html page
        # TODO maybe can get more info from html text
        # TODO support more url types
        # TODO Error process
        # NOTE http://v.youku.com/v_show/id_XMTA3MDAzMDM2.html
        re_list = var.RE_VID_LIST
        vid = re.findall(re_list['vid'])[0]
        out = {
           'vid' : vid, 
        }
        return out
    
    def _get_video_info(self, vid_info):
        # dl first json
        first_url = self._make_first_url(vid_info)
        log.o(log_text.method_got_first_url(first_url))
        
        first = b.dl_json(first_url)
        var._['_raw_first_json'] = first
        # TODO check first OK code
        
        pvinfo = self._parse_raw_first(first)
        # NOTE count and select here
        out = common.method_simple_count_and_select(pvinfo, var)
        return out
    
    def _make_first_url(self, vid_info):
        vid = vid_info['vid']
        first_url = play_service_proxy.request_playlist(vid)
        return first_url
    
    def _do_parse_first(self, first):
        # NOTE just parse it
        pvinfo, more = _parse_raw_first_info(first)
        # TODO save more data
        # TODO maybe gen more data for next parse
        return pvinfo
    
    def _get_file_urls(self, pvinfo):
        # TODO
        # TODO remove _data in video info
        return pvinfo
    
    # TODO
    # end Method class

# base parse functions

def _parse_raw_first_info(first):
    data = first['data']
    # get base info
    out = {}
    out['info'] = {}
    info = out['info']
    
    show = data['show']
    info['title'] = show['title']
    # get title_no
    info['title_no'] = _parse_first_get_title_no(data)
    # NOTE not support title_sub, title_short here
    
    # TODO support many other languages, video and audio
    # TODO support more other drm_type and transfer_mode
    
    # get video info
    stream = data['stream']
    out['video'] = []
    for s in stream:	# process each stream
        one = {}
        # get one format info
        stream_type = s['stream_type']
        one['hd'] = var.TO_HD[stream_type]
        # get size px
        px_x = s['width']
        px_y = s['height']
        one['size_px'] = [px_x, px_y]
        # NOTE format of the file should be flv
        one['format'] = 'flv'
        
        # get file info
        one['file'] = []
        for se in s['segs']:
            f = {}
            f['size'] = se['size']
            # NOTE just get video time_s here
            raw_ms = int(se['total_milliseconds_video'])
            f['time_s'] = raw_ms / 1e3	# ms to second
            # NOTE save key in f['url']
            f['url'] = f['key']
            one['file'].append(f)
        # NOTE add more info for next parse
        one['_data'] = {}
        d = one['_data']
        d['fileid'] = s['stream_fileid']
        d['stream_type'] = stream_type
        # get one video done
        out['video'].append(one)
    # get more data for next parse
    more['security'] = data['security']
    return out, more	# done

def _parse_first_get_title_no(videos):
    # check has title_no
    if not 'videos' in data:
        return -1
    v = data['videos']
    if not 'list' in v:
        return -1
    l = v['list']
    # check id match
    id_ = data['id']
    one = None
    for item in l:
        if item['vid'] == id_:
            one = item
            break
    if one == None:
        return -1
    # got it
    title_no = int(one['seq'])
    return title_no

# TODO
# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


