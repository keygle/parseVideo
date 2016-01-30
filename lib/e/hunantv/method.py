# method.py, parse_video/lib/e/hunantv/

from ... import err, b
from ...b import log
from .. import common, log_text

from .var import var
from .o import mango_tv3

class Method(common.ExtractorMethod):   # common method class for extractor hunantv
    def _init_data(self):
        # NOTE should be set by sub method class
        self._format = ''
    
    def _get_first_json(self, vid_info):
        # make first url
        first_url = mango_tv3.gen_first_url(vid_info['vid'])
        # [ OK ] log
        log.o(log_text.method_got_first_url(first_url))
        first = b.dl_json(first_url)
        var._['_raw_first_json'] = first
        return first
    
    def _get_video_info(self, vid_info):
        first = self._get_first_json(vid_info)
        # check code
        if first['status'] != var._FIRST_OK_CODE:
            raise err.MethodError(log_text.method_err_first_code(first['status'], var))
        return self._parse_raw_first(first)
    
    def _do_parse_first(self, first):
        out, data, info = raw_first_get_base_info(first)
        # get video list
        duration, stream = float(info['duration']), data['stream']
        out['video'] = []
        for s in stream:
            one = {}
            one['hd'] = var.TO_HD[s['name']]
            # set default values
            one['format'] = self._format
            one['size_px'] = [-1, -1]
            one['size_byte'] = -1
            one['time_s'] = duration
            one['count'] = 1
            # add the only one file info
            one['file'] = []
            f = {}
            f['size'] = -1
            f['time_s'] = duration
            f['url'] = self._gen_before_url(s['url'])
            one['file'].append(f)
            out['video'].append(one)
        return out
    
    # NOTE for sub method class
    def _gen_before_url(self, s_url):
        raise NotImplementedError
    # end Method class

# base parse function

def raw_first_get_base_info(first):
    data = first['data']
    out = {}
    # get base video info
    info = data['info']
    out['info'] = {}
    out['info']['title'] = info['title']
    out['info']['title_short'] = info['collection_name']
    out['info']['title_sub'] = info['sub_title']
    out['info']['title_no'] = b.simple_get_number_from_text(info['series'])
    return out, data, info

# end method.py


