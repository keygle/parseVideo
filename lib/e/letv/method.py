# method.py, parse_video/lib/e/letv/, method common code

from ... import err, b
from ...b import log
from .. import common, log_text

from .var import var
from .o.m3u8_encrypt import m3u8_encrypt

class Method(common.ExtractorMethod):   # common method class for extractor letv
    
    def _parse_arg_rest(self, r):
        if r == 'set_flag_v':
            var._['flag_v'] = True
        else:
            return True
    
    def _dl_first_json(self, first_url):
        log.o(log_text.method_got_first_url(first_url))
        first = b.dl_json(first_url)
        var._['_raw_first_json'] = first
        # check code
        if first['statuscode'] != var._FIRST_OK_CODE:
            raise err.MethodError(log_text.method_err_first_code(first['statuscode'], var))
        return first
    
    def _get_video_info(self, vid_info):
        first_url = self._make_first_url(vid_info)
        first = self._dl_first_json(first_url)
        
        pvinfo = self._parse_raw_first(first)
        return pvinfo
    
    def _do_parse_first(self, first):
        out, playurl = raw_first_get_base_info(first)
        # get video list
        domain, dispatch = playurl['domain'], playurl['dispatch']
        
        vid = playurl['vid']
        out['video'] = [self._parse_one_video(vid, domain, i) for i in dispatch.items()]
        return out
    
    # sub parse first info process
    def _parse_one_video(self, vid, domain, dispatch):
        rateid = dispatch[0]
        one = {}
        one['hd'] = var.TO_HD[rateid]
        # set default values
        one['size_px'] = [-1, -1]
        
        return one
    # end Method class

# base parse functions

def raw_first_get_base_info(first):
    playurl = first['playurl']
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = playurl['title']
    return out, playurl

# for process letv encrypt m3u8
def decode_m3u8(raw):
    return m3u8_encrypt.decode(raw)

def parse_m3u8(raw):	# parse letv's m3u8 file text
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
        size = filename.split('_')[-3]	# NOTE fix this at 2016-01-24
        f['size'] = int(size)	# update size
    return out

# end method.py


