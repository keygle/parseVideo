# parse.py, parse_video/lib/e/bks1
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509251751

from ... import b, err
from ...b import log

from . import var

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
    '''
    pass

def get_vp():
    pass	# TODO

# end parse.py


