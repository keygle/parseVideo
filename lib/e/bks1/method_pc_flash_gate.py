# method_pc_flash_gate.py, parse_video/lib/e/bks1/

import re

from ... import err, b, lan
from ...b import log
from .. import common, log_text

from .var import var
from .o import mixer_remote
from .vv import vv_default

class Method(common.ExtractorMethod):
    def _init_data(self):
        self._more_data_list += [
            'raw_first_json', 
        ]
    
    def _gen_more_data(self):
        out = super()._gen_more_data()
        # add first_json info
        out['raw_first_json'] = var._['_raw_first_json']
        return out
    
    def _parse_arg_rest(self, r):
        if r == 'set_um':
            var._['set_um'] = True
        elif r == 'set_vv':
            var._['set_vv'] = True
        elif r == 'set_flag_v':
            var._['flag_v'] = True
        elif r == 'fix_4k':
            var._['flag_fix_4k'] = True
        elif r == 'enable_vv_error':
            var._['flag_enable_vv_error'] = True
        else:	# unknow method arg
            return True
    
    def _fix_vid_info(self, raw):
        out = raw
        # convert flag_vv
        to_flag_vv = {
            'true' : True, 
            'false' : False, 
        }
        out['flag_vv'] = to_flag_vv.get(out['flag_vv'], None)
        # get aid
        raw_html_text = var._['_raw_page_html']
        for key, r in var._RE_VID_LIST2.items():
            try:
                out[key] = re.findall(r, raw_html_text)[0]
            except Exception as e:	# NOTE just ignore Error
                out['key'] = ''	# set empty value
                # WARNING log
                log.w('vid_info [' + key + '] empty ')
        # check enable_vv_error
        if var._['flag_enable_vv_error'] and vid_info['flag_vv']:
            raise err.NotSupportURLError(lan.zh_cn_not_support_vip_video(), var._['_raw_url'])
        return out
    
    def _get_video_info(self, vid_info):
        # get first json
        first = self._get_first_json(vid_info)
        # check code
        if first['code'] != var._FIRST_OK_CODE:
            raise err.MethodError(log_text.method_err_first_code(first['code'], var))
        # parse raw first json
        pvinfo = self._parse_raw_first(first)
        # count and select, hd_min, hd_max, i_min, i_max
        out = common.method_simple_count_and_select(pvinfo, var)
        return out
    
    def _get_first_json(self, vid_info):
        # check get first json from --more
        if var._['_use_more']:
            more_data = var._['more']['_data']
            first_json = more_data['raw_first_json']
        else:
            # make first url
            first_url = self._make_first_url(vid_info)
            # download first json
            first_json = b.dl_json(first_url)
        var._['_raw_first_json'] = first_json	# save to var
        return first_json
    
    def _make_first_url(self, vid_info):
        if var._['flag_v']:	# check flag_v mode
            first_url = vv_default.make_first_url(vid_info)
            prefix = 'flag_v, '
        else:
            first_url = _make_first_url(vid_info)
            prefix = ''
        # check fix_4k
        if var._['flag_fix_4k']:
            first_url = _first_url_fix_4k(first_url)
        # [ OK ] log, got first url
        log.o(log_text.method_got_first_url(first_url, prefix=prefix))
        return first_url
    
    def _do_parse_first(self, first):
        # NOTE just parse it, TODO may be more works here
        return _parse_raw_first_info(first)
    
    def _get_file_urls(self, pvinfo):
        if var._['flag_v']:	# check flag_v mode
            vid_info = var._['_vid_info']
            pvinfo = vv_default.add_tokens(pvinfo, vid_info)
        # get each part file URL
        def worker(f, i):
            raw_info = b.dl_json(f['url'])
            try:
                f['url'] = raw_info['l']	# update url
                return f
            except Exception as e:
                er = err.MethodError('get final file URL failed', f['url'])
                raise er from e
        pool_size = var._['pool_size']['get_file_url']
        return common.simple_get_file_urls(pvinfo, worker, msg='getting part file URLs', pool_size=pool_size)
    
    def _extra_process(self, pvinfo):
        # add part files checksum info
        for v in pvinfo['video']:
            for f in v['file']:
                if f['url'] != '':
                    f['checksum'] = _get_one_checksum(f)
        return pvinfo
    # end Method class

## base parse functions

def _first_url_fix_4k(raw):
    return raw.split('&src=', 1)[0] + '&' + raw.split('&src=', 1)[1].split('&', 1)[1]

def _make_first_url(vid_info):
    tvid = vid_info['tvid']
    vid = vid_info['vid']
    
    set_um = var._['set_um']
    set_vv = var._['set_vv']
    
    out = mixer_remote.get_request(tvid, vid, flag_set_um=set_um, flag_set_vv=set_vv)
    return out

# parse raw first

def _parse_raw_first_info(first):
    out = {}
    data = first['data']
    # get base video info
    vi = data['vi']
    out['info'] = {}
    
    out['info']['title'] = vi['vn']
    out['info']['title_sub'] = vi['subt']
    out['info']['title_short'] = vi['an']
    out['info']['title_no'] = vi['pd']
    # get video list
    vp = data['vp']
    du = vp['du']	# before final url, base part
    raw_list = vp['tkl'][0]['vs']
    
    out['video'] = [_parse_one_video_info(r, du) for r in raw_list]
    return out

def _parse_one_video_info(raw, du):
    bid = raw['bid']
    out = {}
    out['hd'] = var.TO_HD[bid]
    out['size_px'] = common.method_get_size_px(*raw['scrsz'].split('x'))
    out['format'] = 'flv'	# NOTE the video file format shoud be flv
    
    # get file list
    raw_list = raw['fs']
    out['file'] = [_parse_one_file_info(r, du) for r in raw_list]
    return out

def _parse_one_file_info(raw, du):
    out = {}
    out['size'] = raw['b']
    out['time_s'] = raw['d'] / 1e3
    
    l = raw['l']
    out['url'] = du + l	# NOTE before final url, just concat 'du' and 'l'
    return out

# add checksum

def _get_one_checksum(f):
    raw = f['url']
    raw = raw.split('://', 1)[1].split('#', 1)[0].split('?', 1)[0]
    filename = raw.rsplit('/', 1)[1]
    md5 = filename.split('.', 1)[0]	# NOTE the md5 is just the filename
    out = {
        'md5' : md5, 
    }
    return out

# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


