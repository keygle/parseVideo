# parse.py, parse_video/lib/e/bks1
# LICENSE GNU GPLv3+ sceext 
# version 0.0.11.0 test201509271633

'''
base parse functions for extractor bks1
'''

from ... import b, err
from ...b import log

from . import var, o, enc, vv

def get_vid_info(raw_url):
    # INFO log here
    log.i('loading page \"' + raw_url + '\" ')
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
    if (vid_info['flag_vv'] == 'true') and var._['flag_v']:
        var._['flag_v'] = True
    else:	# will auto turn off flag_v
        # WARNING log here
        if var._['flag_v']:
            log.w('auto turn off flag_v, set to False ')
        var._['flag_v'] = False
    if var._['flag_v_force']:
        # DEBUG log here
        log.d('got flag_v_force True, set flag_v True ')
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
            flag_set_um = var._['flag_set_um'], 
            flag_set_vv = var._['flag_set_vv'], 
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

# normal method to make before_final_url
def normal_make_before_urls(video_info):
    raw = video_info
    # get key info
    if not var._['flag_v']:
        server_time = o.get_server_time()
        # DEBUG log here
        log.d('got server_time ' + str(server_time) + ' ')
    else:	# get token list
        token_flag_list = vv.gen_token_flag_list(raw)
        token_list = vv.get_token_list(token_flag_list)
    # gen before_final_url, process each video
    for v in raw:
        # make raw url list
        raw_url = []
        for f in v['file']:
            raw_url.append(f['url'])
        # get before_final_url
        if not var._['flag_v']:
            before_urls = o.make_before_urls(raw_url, server_time=server_time)
        else:
            before_urls = o.make_before_urls(raw_url, token_list=token_list)
        # update urls
        i = 0
        for f in v['file']:
            f['url'] = before_urls[i]
            i += 1
    return raw

# NOTE normal parse process, used by method pc_flash_gate
def normal_parse(raw_page_url):
    vid_info = get_vid_info(raw_page_url)
    first_url = normal_get_first_url(vid_info)
    # [ OK ] log here
    log.o('got first_url \"' + first_url + '\" ')
    # load raw vms
    raw_vms = b.dl_json(first_url)
    var._['_vms_json'] = raw_vms
    # pre-parse
    try:
        evinfo = pre_parse(raw_vms)
    except Exception as e:
        er = err.MethodError('this parse method may be out-of-date ')
        er.raw_info = raw_vms
        raise er from e
    # select by hd and index
    raw = b.select_hd(evinfo['video'])
    raw = b.select_file_index(raw)
    # make before final urls
    raw = normal_make_before_urls(raw)
    evinfo['video'] = raw
    # make a list of before urls
    before_urls = []
    for v in evinfo['video']:
        for f in v['file']:
            if f['url']:	# check to ignore no-need urls
                before_urls.append(f['url'])
    # get final_urls
    final_urls = normal_get_final_urls(before_urls)
    # update final urls
    i = 0
    for v in evinfo['video']:
        for f in v['file']:
            if f['url']:	# check to skip no-need urls
                f['url'] = final_urls[i]
                i += 1
    return evinfo

# get final urls from before urls
def normal_get_final_urls(before_urls):
    # make raw list for normal_get_one_final_url
    raw = []
    for i in range(len(before_urls)):
        raw.append({
            'i' : i, 
            'url' : before_urls[i], 
        })
    pool_size = var._['pool_size_get_final_url']
    # INFO log here
    log.i('start get ' + str(len(before_urls)) + ' final_urls with pool_size ' + str(pool_size) + ' ')
    # use map_do to get many final_urls at the same time
    final_urls = b.map_do(raw, normal_get_one_final_url, pool_size=pool_size)
    # [ OK ] log here
    log.o('got ' + str(len(before_urls)) + ' final_urls')
    return final_urls

# used by normal_get_final_urls to support DEBUG log
# TODO to support auto-retry if get failed
def normal_get_one_final_url(raw):
    i = raw['i']
    url = raw['url']
    # DEBUG log here
    log.d('get ' + str(i) + ' from \"' + url + '\" ')
    final = o.get_one_final_url(url)
    log.d('got ' + str(i) + ' final \"' + final + '\"')
    return final

# end parse.py


