# parse.py, parse_video/lib/e/bks1
# LICENSE GNU GPLv3+ sceext 
# version 0.0.5.0 test201509261528

'''
base parse functions for extractor bks1
'''

from ... import b, err
from ...b import log

from . import var, o, enc, vv

def get_vid_info(raw_url):
    # DEBUG log here
    log.d('loading page \"' + raw_url + '\" ')
    html_text = b.dl_html(raw_url)
    vid_info = b.re_get_list(var.RE_VID_LIST, text=html_text, re_fix=var.RE_VID_LIST_FIX)
    # DEBUG log here
    log.d('got tvid:vid, aid:flag_vv \"' + str(vid_info['tvid']) + ':' + str(vid_info['vid']) + ', ' + str(vid_info['aid']) + ':' + str(vid_info['flag_vv']) + '\"')
    # check vid info
    if (vid_info['vid'] == None) or (vid_info['tvid'] == None):
        er = err.NotSupportURLError('get vid_info (vid, tvid) failed', raw_url)
        er.html_text = html_text
        raise er
    # check flag_vv
    if (vid_info['flag_vv'] = 'true') and var._['flag_v']:
        var._['flag_v'] = True
    else:	# will auto turn off flag_v
        var._['flag_v'] = False
    if var._['flag_v_force']:
        var._['flag_v'] = True
    # save vid_info, and more
    var._['_raw_url'] = raw_url
    var._['_raw_page_html'] = html_text
    var._['_vid_info'] = vid_info
    return vid_info

def pre_parse(raw_vms):
    '''
    pre-parse of this extractor, will get video info and raw file info
    input raw vms json info
    the later parse process will base on this function's output
    
    NOTE should try: to run this function, and raise err.MethodError() if this failed. 
    '''
    data = raw_vms['data']
    vi = data['vi']
    try:
        vp = get_vp(data)
    except Exception as e:
        er = err.MethodError('not support this video, may be a VIP video ')
        er.raw_info = data
        raise er from e
    var._['_vp'] = vp	# save it
    # output info, standard parse_video video_info format struct
    evinfo = {}
    evinfo['info'] = {}
    evinfo['video'] = []
    info = evinfo['info']
    video = evinfo['video']
    # add base video info
    info['title'] = vi['vn']
    info['title_sub'] = vi['subt']
    info['title_short'] = vi['an']
    info['title_no'] = vi['pd']
    # get base info, and save it
    du = vp['du']
    var._['_du'] = du
    # get raw video list info
    tkl = vp['tkl']
    vs = tkl[0]['vs']
    # make raw video list and get info
    for raw in vs:
        one = {}	# one raw video info
        bid = int(raw['bid'])
        one['hd'] = var.BID_TO_HD[bid]
        # get size_px
        raw_s = raw['scrsz']	# NOTE now there is no need to make a request to get video size_px
        raw_x, raw_y = raw_s.split('x', 1)
        one['size_px'] = [int(raw_x), int(raw_y)]
        one['format'] = 'flv'	# NOTE now the video file format should be .flv
        # get raw file info
        fs = raw['fs']
        one['file'] = []
        for rawf in fs:
            onef = {}
            onef['size'] = rawf['b']
            onef['time_s'] = rawf['d'] / 1e3	# raw data is in ms
            rawl = rawf['l']	# NOTE try to decode raw l
            if not rawl.startswith('/'):
                rawl = o.getVrsEncodeCode(rawl)
            onef['url'] = rawl
            one['file'].append(onef)
        video.append(one)
    # sort raw video list by hd
    video.sort(key=lambda x:x['hd'], reverse=True)
    return evinfo	# raw pre-parse done

def get_vp(data):
    if var._['flag_v']:
        vp = data['np']
    else:
        vp = data['vp']
    return vp

# normal method to get first_url for normal parse
def normal_get_first_url(vid_info):
    # gen tm and enc for first_url
    tm = o.gen_tm()
    _enc = enc.gen(vid_info['tvid'], tm)
    if not var._['flag_v']:	# normal make first url
        first_url = o.make_first_url(
            vid = vid_info['vid'], 
            tvid = vid_info['tvid'], 
            enc = _enc, 
            tm = tm)
    else:	# load vv config
        vvc = vv.load_conf()
        token = vv.get_ck_token()	# load a token for first_url
        # make first_url
        first_url = o.make_first_url(
            vid = vid_info['vid'], 
            tvid = vid_info['tvid'], 
            enc = _enc, 
            qyid = var._['_qyid'], 
            flag_v = var._['flag_v'], 
            cid = var.DEFAULT_CID, 
            token = token, 
            uid = vvc['uid'], 
            puid = vvc['uid'], 
            tm = tm)
    var._['_first_url'] = first_url
    return first_url

# TODO normal parse process, used by method pc_flash_gate
# TODO this process may should be split in sub-process
def normal_parse(raw_page_url):
    vid_info = get_vid_info(raw_page_url)
    first_url = normal_get_first_url(vid_info)
    # DEBUG log here
    log.d('got first_url \"' + first_url + '\" ')
    # load raw vms
    raw_vms = b.dl_json(first_url)
    var._['_vms_json'] = raw_vms
    # pre-parse
    raw_evinfo = pre_parse(raw_vms)
    # select by hd and index
    raw = b.select_hd(raw_evinfo)
    raw = b.select_file_index(raw)
    # get key list
    # TODO
    pass

# end parse.py


