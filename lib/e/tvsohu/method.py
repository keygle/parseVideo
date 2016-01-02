# method.py, parse_video/lib/e/tvsohu/

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import main

# support --more
def get_raw_more(method_arg_text):
    data_list = [	# NOTE --more mode to direct get vid_info
        'vid_info', 
        'raw_first_json', 	# NOTE also get raw first json info in --more mode
    ]
    raw_more = common.method_simple_check_use_more(var, method_arg_text, data_list)
    if raw_more != None:	# set first_json
        var._['_raw_first_json'] = raw_more['_data']['raw_first_json']
    return raw_more

def _do_get_vid_info():
    raw_url = var._['_raw_url']
    # INFO log
    log.i(log_text.method_loading_page(raw_url))
    raw_blob = b.dl_blob(raw_url)
    raw_html_text = raw_blob.decode('utf-8', 'ignore')	# NOTE the html encoding is not 'utf-8'
    var._['_raw_page_html'] = raw_html_text
    
    vid_info = common.parse_simple_get_vid_info(raw_html_text, var)
    var._['_vid_info'] = vid_info
    log.d(log_text.method_got_vid_info(vid_info))
    return vid_info

def get_vid_info():
    # get vid_info from more if possible
    vid_info = common.method_more_simple_get_vid_info(var, _do_get_vid_info)
    return vid_info

def check_enable_more(out):
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = var._['_vid_info']
        out['_data']['raw_first_json'] = var._['_raw_first_json']
    return out

# first part parse

def get_video_info(vid_info, gen_one_before_url):
    # check use_more
    if not var._['_use_more']:
        _get_first_json_info(vid_info, gen_one_before_url)
    # do more parse
    pvinfo = _get_video_info_2(gen_one_before_url)
    return pvinfo

def _get_first_json_info(vid_info, gen_one_before_url):
    # TODO support fast_parse here
    vid = vid_info['vid']
    # make first URL
    first_url = main.gen_first_url(vid)
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'][int(vid)] = first
    # TODO support fast_parse here
    # parse raw first, get other vids, and download other first info jsons
    vid_list = _parse_one_first(first, vid, gen_one_before_url)['vid_list']
    # make todo list
    todo = []
    for name, value in vid_list.items():	# NOTE vid == 0 is null
        if (not int(value) in var._['_raw_first_json']) and (int(value) != 0):
            one = {}
            one['name'] = name
            one['vid'] = value
            one['url'] = main.gen_first_url(value)
            todo.append(one)
    pool_size = var._['pool_size']['get_first']
    # INFO log
    log.i('getting video info, count ' + str(len(todo)) + ', pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo, worker=_dl_one_first, pool_size=pool_size)
    log.d('got video info (first) done ')
    # save more raw_first_json
    for r in result:
        var._['_raw_first_json'][int(r['vid'])] = r['json']
    # get first json info done

def _dl_one_first(info):
    log.d('getting first, name ' + b.str_or_str(info['name']) + ', vid ' + b.str_or_str(info['vid']) + ', url \"' + info['url'] + '\" ')
    raw = b.dl_json(info['url'])
    log.d('[done] got name ' + b.str_or_str(info['name']) + ' ')
    out = {}
    out['vid'] = info['vid']
    out['json'] = raw
    return out

def _parse_one_first(raw, vid, gen_one_before_url):
    try:
        return _do_parse_one_first(raw, int(vid), gen_one_before_url)
    except err.PVError:
        raise
    except Exception as e:
        raise err.MethodError('parse first info json failed ')

def _do_parse_one_first(raw, vid, gen_one_before_url):
    # check first code
    if raw['status'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(raw['status'], var))
    out = {}
    data = raw['data']
    # get base video info
    info = {}
    info['title'] = data['tvName']
    info['title_sub'] = data['subName']
    info['title_no'] = data['num']
    out['info'] = info
    # get vid list
    name_list = var.VID_NAME_LIST
    vid_list = {}
    for i in name_list:
        vid_list[i] = data[i]
    out['vid_list'] = vid_list
    # get one video format info
    v = {}
    v['size_px'] = [
        data['width'], 
        data['height'], 
    ]
    v['format'] = 'mp4'	# NOTE the file format should be mp4
    # get hd
    vid_name = None
    for vid_type, vid_value in vid_list.items():
        if vid_value == vid:
            vid_name = vid_type
            break
    if vid_name == None:
        raise err.MethodError('can not get vid_type from vid ' + b.str_or_str(vid) + ' ')
    v['hd'] = var.TO_HD[vid_name]
    # NOTE add quality here
    quality = var.VID_NAME_LIST[vid_name]
    if quality != None:
        v['quality'] = quality
    # gen file before urls
    tvid, ch = raw['tvid'], data['ch']
    su = data['su']
    clipsDuration = data['clipsDuration']
    clipsBytes = data['clipsBytes']
    v['file'] = []
    for i in range(len(su)):
        one = {}
        one['size'] = clipsBytes[i]
        one['time_s'] = clipsDuration[i]
        # gen file before URL
        one['url'] = gen_one_before_url(su[i], vid, tvid, ch)
        v['file'].append(one)
    out['v'] = v
    out['vid'] = vid
    return out

def _get_video_info_2(gen_one_before_url):
    # TODO support fast_parse here
    raw_list = var._['_raw_first_json']
    out = {}
    out['video'] = []
    for vid, raw in raw_list.items():
        one = _parse_one_first(raw, vid, gen_one_before_url)
        if not 'info' in out:
            out['info'] = one['info']
        out['video'].append(one['v'])
    common.method_sort_video(out)
    return out

def count_and_select(pvinfo):
    # TODO support fast_parse here
    return common.method_simple_count_and_select(pvinfo, var)

# end method.py


