# method_pc_flash_gate.py, parse_video/lib/e/tvsohu/

import functools

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import main

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # TODO support --more
    # process method args
    def rest(r):
        if r == 'fast_parse':
            var._['flag_fast_parse'] = True
        elif r == 'gen_header':
            var._['flag_gen_header'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    # TODO get vid_info and first info from --more mode
    
    # load page and get vid_info
    vid_info = _get_vid_info()
    
    pvinfo = _get_video_info(vid_info)
    pvinfo = _count_and_select(pvinfo)	# NOTE count and select
    out = _get_file_urls(pvinfo)
    # NOTE add headers
    out = _add_headers(out)
    # TODO support enable_more
    return out

def _get_vid_info():
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

def _get_video_info(vid_info):
    # TODO support fast_parse here
    vid = vid_info['vid']
    # make first URL
    first_url = main.gen_first_url(vid)
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    first = b.dl_json(first_url)
    var._['_raw_first_json'][vid] = first
    # TODO support fast_parse here
    # parse raw first, get other vids, and download other first info jsons
    vid_list = _parse_one_first(first, vid)['vid_list']
    # make todo list
    todo = []
    for name, value in vid_list.items():	# NOTE vid == 0 is null
        if (not value in var._['_raw_first_json']) and (value != 0):
            one = {}
            one['name'] = name
            one['vid'] = value
            one['url'] = main.gen_first_url(vid)
            todo.append(one)
    pool_size = var._['pool_size']['get_first']
    # INFO log
    log.i('getting video info, count ' + str(len(todo)) + ', pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo, worker=_dl_one_first, pool_size=pool_size)
    log.d('got video info (first) done ')
    # save more raw_first_json
    for r in result:
        var._['_raw_first_json'][r['vid']] = r['json']
    # do more parse
    pvinfo = _get_video_info_2()
    return pvinfo

def _dl_one_first(info):
    log.d('getting first, name ' + b.str_or_str(info['name']) + ', vid ' + b.str_or_str(info['vid']) + ' ')
    raw = b.dl_json(info['url'])
    log.d('[done] got name ' + b.str_or_str(info['name']) + ' ')
    out = {}
    out['vid'] = info['vid']
    out['json'] = raw
    return out

def _parse_one_first(raw, vid):
    try:
        return _do_parse_one_first(raw, vid)
    except err.PVError:
        raise
    except Exception as e:
        raise err.MethodError('parse first info json failed ')

def _do_parse_one_first(raw, vid):
    # check first code
    if raw['status'] != var.FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(raw['status'], var))
    # TODO check raw info version: data.version == 31
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
        one['url'] = main.gen_before_url(su[i], vid, tvid, ch)
        v['file'].append(one)
    out['v'] = v
    out['vid'] = vid
    return out

def _get_video_info_2():
    # TODO support fast_parse here
    raw_list = var._['_raw_first_json']
    out = {}
    out['video'] = []
    for raw in raw_list.values():
        one = _parse_one_first(raw)
        if not 'info' in out:
            out['info'] = one['info']
        out['video'].append(one['v'])
    common.method_sort_video(out)
    return out

def _count_and_select(pvinfo):
    # TODO support fast_parse here
    return common.method_simple_count_and_select(pvinfo, var)

def _get_file_urls(pvinfo):
    def worker(f, i):
        raw = b.dl_json(f['url'])
        try:
            f['url'] = raw['url']	# update URL
            return f
        except Exception as e:
            er = err.MethodError('get final file URL failed', f['url'])
            raise er from e
    pool_size = var._['pool_size']['get_final']
    return common.simple_get_file_urls(pvinfo, worker, msg='getting part file URLs', pool_size=pool_size)

def _add_headers(pvinfo):
    # TODO support gen_header method arg here
    # TODO
    return pvinfo

# end method_pc_flash_gate.py


