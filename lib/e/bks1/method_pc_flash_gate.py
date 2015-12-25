# method_pc_flash_gate.py, parse_video/lib/e/bks1/

import re

from ... import err, b
from ...b import log

from . import var

from .o import mixer_remote
from .vv import vv_default

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # parse method args
    if method_arg_text != None:
        args = method_arg_text.split(',')
        for r in args:
            if r == 'set_um':
                var._['set_um'] = True
            elif r == 'set_vv':
                var._['set_vv'] = True
            elif r == 'set_flag_v':
                var._['flag_v'] = True
            else:	# unknow arg
                log.w('unknow method arg \"' + r + '\" ')
    
    # TODO support --more option
    raw_url = var._['_raw_url']
    # INFO log, loading html page
    log.i('loading page \"' + raw_url + '\" ')
    raw_html_text = b.dl_html(raw_url)
    var._['_raw_page_html'] = raw_html_text
    
    vid_info = _get_vid_info(raw_html_text)
    var._['_vid_info'] = vid_info
    # DEBUG log
    log.d('got vid_info ' + str(vid_info))
    
    pvinfo = _get_video_info(vid_info)
    # check flag_v mode
    if var._['flag_v']:
        pvinfo = vv_default.add_tokens(pvinfo, vid_info)
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
        # convert flag_vv
        to_flag_vv = {
            'true' : True, 
            'false' : False, 
        }
        out['flag_vv'] = to_flag_vv.get(out['flag_vv'], None)
        
        return out
    except Exception as e:
        er = err.NotSupportURLError('get vid info failed', var._['_raw_url'])
        raise er from e

def _get_video_info(vid_info):
    # check flag_v mode
    if var._['flag_v']:
        first_url = vv_default.make_first_url(vid_info)
        # [ OK ] log
        log.o('flag_v, got first URL \"' + first_url + '\" ')
    else:
        first_url = _make_first_url(vid_info)
        # [ OK ] log, load first video info json
        log.o('got first URL \"' + first_url + '\" ')
    vms = b.dl_json(first_url)
    var._['raw_vms_json'] = vms
    
    # check code
    if vms['code'] != var.VMS_OK_CODE:
        raise err.MethodError('vms_json info code \"' + vms['code'] + '\" is not ' + var.VMS_OK_CODE + ' ')
    
    try:
        pvinfo = _parse_raw_vms_info(vms)
    except Exception as e:
        er = err.MethodError('parse raw vms info failed')
        raise er from e
    
    out = _select_and_count(pvinfo)
    return out

def _make_first_url(vid_info):
    tvid = vid_info['tvid']
    vid = vid_info['vid']
    
    set_um = var._['set_um']
    set_vv = var._['set_vv']
    
    out = mixer_remote.get_request(tvid, vid, flag_set_um=set_um, flag_set_vv=set_vv)
    return out

def _parse_raw_vms_info(vms_info):
    out = {}
    data = vms_info['data']
    # get base video info
    vi = data['vi']
    out['info'] = {}
    
    out['info']['title'] = vi['vn']
    out['info']['title_sub'] = vi['subt']
    out['info']['title_short'] = vi['an']
    out['info']['title_no'] = vi['pd']
    
    # get video list
    vp = data['vp']
    raw_list = vp['tkl'][0]['vs']
    
    du = vp['du']	# before final url, base part
    
    out['video'] = [_parse_one_video_info(r, du) for r in raw_list]
    return out

def _parse_one_video_info(raw, du):
    out = {}
    
    bid = raw['bid']
    out['hd'] = var.BID_TO_HD[bid]
    try:
        scrsz = raw['scrsz'].split('x')
        out['size_px'] = [
            int(scrsz[0]), 
            int(scrsz[1]), 
        ]
    except Exception:
        out['size_px'] = [-1, -1]
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

# select by hd_min, hd_max, i_min, i_max. count sum data, and sort info
def _select_and_count(pvinfo):
    # sort videos by hd
    pvinfo['video'].sort(key = lambda x: x['hd'], reverse=True)
    # count video info
    for v in pvinfo['video']:
        v['size_byte'] = 0
        v['time_s'] = 0
        v['count'] = len(v['file'])
        for f in v['file']:
            v['size_byte'] += f['size']
            v['time_s'] += f['time_s']
        v['time_s'] = round(v['time_s'], 3)	# NOTE round time to ms
    # select hd_min, hd_max
    hd_min = var._['hd_min']
    hd_max = var._['hd_max']
    for v in pvinfo['video']:
        if ((hd_min != None) and (v['hd'] < hd_min)) or ((hd_max != None) and (v['hd'] > hd_max)):
            v['file'] = []	# clear video file list
    # select i_min, i_max
    i_min = var._['i_min']
    i_max = var._['i_max']
    for v in pvinfo['video']:
        for i in range(len(v['file'])):
            if ((i_min != None) and (i < i_min)) or ((i_max != None) and (i > i_max)):
                v['file'][i]['url'] = ''	# clear file URL
    # done
    return pvinfo

def _get_file_urls(pvinfo):
    # TODO maybe retry here
    # make task raw list
    raw = []
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                one = {}
                one['i'] = i	# add index number for DEBUG
                i += 1
                one['url'] = f['url']	# raw url
                raw.append(one)	# add one task
    # use map_do() to get many file_urls at the same time
    pool_size = var._['pool_size_get_file_url']
    # INFO log
    log.i('getting ' + str(len(raw)) + ' part file URLs, pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(raw, worker = _get_one_file_url, pool_size=pool_size)
    # DEBUG log
    log.d('got file URLs done. ')
    # set back real file urls
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                f['url'] = result[i]
                i += 1
    # done
    return pvinfo

def _get_one_file_url(raw):
    i = raw['i']
    # DEBUG log
    log.d('start get index ' + str(i) + ' ')
    
    raw_info = b.dl_json(raw['url'])
    try:
        result = raw_info['l']
    except Exception as e:
        er = err.MethodError('get final file URL failed', raw['url'])
        raise er from e
    # DEBUG log
    log.d('[done] got index ' + str(i) + ' ')
    return result

# end method_pc_flash_gate.py


