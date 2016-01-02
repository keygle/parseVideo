# method_android.py, parse_video/lib/e/pptv/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var, method

# method_android.parse(), entry function
def parse(method_arg_text):
    method.get_raw_more(method_arg_text)
    # parse method args
    def rest(r):
        return True	# NOTE no args now
    common.method_parse_method_args(method_arg_text, var, rest)
    vid_info = method.get_vid_info()
    
    pvinfo = _get_video_info(vid_info)
    # NOTE already got file URLs
    out = method.check_enable_more(pvinfo)
    return out

def _get_video_info(vid_info):
    first_url = _make_first_url(vid_info)
    first = method.dl_first_xml(first_url)
    
    pvinfo = common.parse_raw_first(first, _parse_raw_first)
    # NOTE count and select here
    out = common.method_simple_count_and_select(pvinfo, var)
    return out

def _make_first_url(vid_info):
    BEFORE = 'http://play.api.pptv.com/boxplay.api?platform=android3&type=phone.android&userType=1&&id='
    out = BEFORE + str(vid_info['cid'])
    return out

def _parse_raw_first(first):
    out, channel = method.raw_first_get_base_info(first)
    time_s = float(channel.get('dur'))
    
    # collect info by ft
    info = {}
    file_item = channel.find('file').findall('item')
    for i in file_item:
        ft = str(i.get('ft'))
        if not ft in info:
            info[ft] = {}
        info[ft]['item'] = i
    # get dt
    dt_list = first.findall('dt')
    for dt in dt_list:
        ft = str(dt.get('ft'))
        info[ft]['dt'] = dt
    # gen video info
    out['video'] = []
    for ft, data in info.items():
        one = {}
        one['hd'] = var.TO_HD[str(ft)]
        item = data['item']
        px_x = int(item.get('width'))
        px_y = int(item.get('height'))
        one['size_px'] = [px_x, px_y]
        one['format'] = 'mp4'	# NOTE file format here should be mp4
        # gen only one file info
        one['file'] = []
        f = {}
        f['size'] = int(item.get('filesize'))
        f['time_s'] = time_s
        # gen file url
        rid = item.get('rid')
        f['url'] = _gen_one_file_url(rid, data['dt'])
        
        one['file'].append(f)
        out['video'].append(one)
    return out

def _gen_one_file_url(rid, dt):
    PART_1 = '?w=1&platform=android3&type=phone.android&k='
    
    sh = dt.find('sh').findtext('.')
    k = dt.find('key').findtext('.')
    
    out = 'http://' + sh + '/' + str(rid) + PART_1 + k
    return out

# end method_android.py


