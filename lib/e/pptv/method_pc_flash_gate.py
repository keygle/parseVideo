# method_pc_flash_gate.py, parse_video/lib/e/pptv/

from ... import err, b
from .. import common

from .var import var
from . import method
from .o import (
    vod_play_proxy, 
    ctx_query, 
    play_info, 
)

class Method(method.Method):
    
    def _parse_arg_rest(self, r):
        if r == 'get_title_no':
            var._['flag_get_title_no'] = True
        else:
            return True
    
    def _extra_process(self, raw):
        # TODO support get_title_no here
        return raw
    
    def _make_first_url(self, vid_info):
        # reset and set ctx
        ctx_query.ctx.clear()
        ctx_query.setCTX(vid_info['ctx'])
        # gen first url
        cid = vid_info['cid']
        return vod_play_proxy.get_play_url(cid)
    
    # sub parse first functions
    def _collect_info(self, channel, first):
        raw = super()._collect_info(channel, first)
        # NOTE get dragdata
        out = self._get_dragdata(first, raw)
        return out
    
    def _get_dragdata(self, first, info):
        dragdata = first.findall('dragdata')
        for d in dragdata:
            ft = str(d.get('ft'))
            info[ft]['drag'] = d
        return info
    
    def _get_size_px(self, data):
        drag = data['drag']
        px_x = int(drag.get('vw'))
        px_y = int(drag.get('vh'))
        return [px_x, px_y]
    
    def _get_file_info(self, data, channel):
        out = []    # gen file list
        drag = data['drag']
        sgm = drag.findall('sgm')
        for s in sgm:
            f = {}
            f['size'] = int(s.get('fs'))
            f['time_s'] = float(s.get('dur'))
            # NOTE gen file URL here
            server = data['dt'].find('bh').text
            filename = data['item'].get('rid')
            index = int(s.get('no'))
            more = {}
            more['k'] = data['dt'].find('key').text
            more['key'] = play_info.gen_key()
            f['url'] = play_info.make_cdn_url(server, filename, index, more=more)
            out.append(f)
        return out
# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


