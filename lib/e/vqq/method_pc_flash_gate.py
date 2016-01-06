# method_pc_flash_gate.py, parse_video/lib/e/vqq/

import re
import xml.etree.ElementTree as ET

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var
from .o import player

# method_pc_flash_gate.parse(), entry function
def parse(method_arg_text):
    # TODO support --more
    # process method args
    def rest(r):
        if r == 'fix_1080p':
            var._['flag_fix_1080p'] = True
            # NOTE fix_1080p requires hd range
            if (var._['hd_min'] != None) and (var._['hd_min'] > 2):
                var._['hd_min'] = 2	# NOTE to fix_1080p, should get 720p video info
                # WARNING log
                log.w('set fix_1080p, auto set hd_min = 2 ')
            if (var._['hd_max'] != None) and (var._['hd_max'] < 4):
                var._['hd_max'] = 4
                # WARNING log
                log.w('set fix_1080p, auto set hd_max = 4')
        elif r == 'ignore_fix_1080p_error':
            var._['flag_ignore_fix_1080p_error'] = True
        elif r == 'enable_fmt_black_list':
            var._['flag_enable_fmt_black_list'] = True
            log.d('use fmt_black_list ' + str(var._['fmt_black_list']) + ' ')
        elif r == 'fast_parse':
            var._['flag_fast_parse'] = True
        else:	# unknow args
            return True
    common.method_parse_method_args(method_arg_text, var, rest)
    
    # TODO support fast_parse here
    # TODO support --more here for vid_info
    # get vid info
    vid_info = common.parse_load_page_and_get_vid(var, _get_vid_info)
    # TODO base parse
    pvinfo = _get_video_info(vid_info)
    
    # TODO fix_1080p
    if var._['flag_fix_1080p']:
        pvinfo = _fix_1080p(pvinfo)
    
    out = _get_file_urls(pvinfo)
    # TODO support enable_more
    return out

def _get_vid_info(raw_html_text):
    raw_url = var._['_raw_url']
    # get scripts
    raw_scripts = raw_html_text.split('<script')
    scripts = [r.split('</script>')[0] for r in raw_scripts]
    # get key script part
    script = None
    for s in scripts:	# check key words
        if ('COVER_INFO' in s) and ('VIDEO_INFO' in s):
            script = s
            break
    if not script:	# check found
        er = err.NotSupportURLError('get vid_info, find script text failed ', raw_url)
        er.html_text = raw_html
        raise er
    # get info from the script
    try:
        parts = {}	# get parts from script
        raw_parts = script.split('var ')
        for r in raw_parts:
            if 'COVER_INFO' in r:
                parts['cover_info'] = r
            elif 'VIDEO_INFO' in r:
                parts['video_info'] = r
        raw_cover = parts['cover_info']
        raw_video = parts['video_info']
        # get some info items
        re_list = var.RE_VID_LIST
        out = {}
        out['title_short'] = re.findall(re_list['title_short'], raw_cover)[0]
        out['title_sub'] = re.findall(re_list['title_sub'], raw_cover)[0]
        out['title_no'] = re.findall(re_list['title_no'], raw_video)[0]
        out['vid'] = re.findall(re_list['vid'], raw_video)[0]
    except Exception as e:
        er = err.NotSupportURLError('get vid_info items from page html script text failed ', raw_url)
        er.html_text = raw_html
        er.script_text = script
        raise er from e
    # NOTE check URL format, such as http://v.qq.com/cover/e/e7hi6lep1yc51ca.html?vid=u0018rahda3
    uparts = raw_url.split('://', 1)[1]
    if '?' in uparts:
        uparts = uparts.split('?', 1)[1]
    else:
        uparts = ''
    if uparts and ('#' in uparts):
        uparts = uparts.split('#', 1)[0]
    if uparts:
        parts = uparts.split('&')
        uparts = {}
        for p in parts:
            if '=' in p:
                key, value = p.split('=', 1)
                uparts[key] = value
        if ('vid' in uparts) and uparts['vid']:
            out['vid'] = uparts['vid']
            out['title_no'] = -1	# NOTE fix title_no here
            log.d('reset vid to \"' + out['vid'] + '\" to fix URL \"' + raw_url + '\" ')
    out['title_no'] = int(out['title_no'])	# FIXME may be Error here
    return out	# get vid_info done

def _get_video_info(vid_info):
    _get_first_xml_info(vid_info)
    # create pvinfo
    out = {}
    out['info'] = {}
    for key in ['title', 'title_sub', 'title_short', 'title_no']:
        out['info'][key] = vid_info[key]
    # get video list
    raw_list = var._['_raw_xml_root']
    out['video'] = []
    for fmt, root in raw_list.items():
        info = _parse_one_first(root)
        one = info['video']
        # add more info
        one['hd'] = var.TO_HD[fmt]
        out['video'].append(one)
    common.method_sort_video(out)
    return out

# do one POST and get xml info
def _do_one_post_xml(raw, log_debug=True, prefix=''):
    # do log text
    log_text = prefix + 'POST \"' + raw['url'] + '\" with data \"' + b.make_post_str(raw['post_data']) + '\" '
    if log_debug:
        log.d(log_text)	# DEBUG log
    else:
        log.i(log_text)	# INFO log
    raw_blob = b.post_form(raw['url'], header=raw['header'], post_data=raw['post_data'])
    # decode as xml, NOTE only support utf-8 encoding here
    try:
        raw_xml = raw_blob.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('can not decode raw blob with utf-8 ')
        er.blob = raw_blob
        raise er from e
    try:
        root = ET.fromstring(raw_xml)
    except Exception as e:
        er = err.ParseXMLError('can not parse raw xml text ')
        er.text = raw_xml
        raise er from e
    return root, raw_xml	# done

def _get_first_xml_info(vid_info):
    # TODO support fast_parse here
    vid = vid_info['vid']
    first_post = player.getvinfo(vid)
    first_root, first_xml = _do_one_post_xml(first_post, log_debug=False)	# INFO log
    # TODO to get first type here, to dec one POST request
    first_info = _parse_one_first(first_root)
    var._['_server_list'] = first_info['server']	# save server list
    # save title to vid_info
    vid_info['title'] = first_info['title']
    
    format_list = first_info['format']
    format_name = [i['name'] for i in format_list]
    # [ OK ] log
    log.o('got formats ' + str(format_name) + ' ')
    
    # make get other first info todo list
    todo = []
    for i in format_list:
        # check limit and skip it
        if str(i['limit']) != '0':	# 0 is un-limit
            # WARNING log
            log.w('skip limit format ' + i['id'] + ':' + i['name'] + ':' + i['cname'] + ' ')
        # check fmt black list
        elif var._['flag_enable_fmt_black_list'] and (i['name'] in var._['fmt_black_list']):
            log.d('skip fmt ' + i['name'] + ' in fmt_black_list ')
        else:	# make todo info
            post_info = player.getvinfo(vid, video_format=i['name'])
            todo.append((i, post_info))
    pool_size = var._['pool_size']['get_formats']
    # INFO log
    log.i('getting video info, count ' + str(len(todo)) + ', pool_size = ' + str(len(pool_size)) + ' ')
    result = b.map_do(todo, worker=_dl_one_first, pool_size=pool_size)
    log.d('got video info (first) done ')
    # save result
    for r in result:
        fmt = r['fmt']
        var._['_raw_first_xml'][fmt] = r['xml']
        # save xml root
        var._['_raw_xml_root'][fmt] = r['root']
    # get first xml info done

def _dl_one_first(info):
    fmt = str(info[0]['name'])
    prefix = 'get raw first xml [' + fmt + '] '
    root, raw_xml = _do_one_post_xml(info[1], prefix=prefix)
    log.d('[done] got first [' + fmt + '] ')
    out = {}
    out['fmt'] = fmt
    out['xml'] = raw_xml
    out['root'] = root
    return out

def _parse_one_first(raw):
    try:
        return _do_parse_one_first(raw)
    except err.PVError:
        raise
    except Exception as e:
        raise err.MethodError('parse first info xml failed ')

def _do_parse_one_first(root):
    # TODO check first OK code
    out = {}
    # get format list
    fl = root.find('fl')
    out['format'] = []
    for f in fl.findall('fi'):
        one = {}
        one['cname'] = f.find('cname').text
        one['name'] = f.find('name').text
        one['id'] = f.find('id').text
        one['limit'] = f.find('lmt').text
        out['format'].append(one)
    # get one format info
    vl = root.find('vl')
    vi = vl.find('vi')
    # get server list
    ul = vi.find('ul')
    out['server'] = []
    for u in ul.findall('ui'):
        one = {}
        one['dt'] = u.find('dt').text
        one['dtc'] = u.find('dtc').text
        one['url'] = u.find('url').text
        one['vt'] = u.find('vt').text
        out['server'].append(one)
    # get fn, lnk
    out['fn'] = vi.find('fn').text
    out['lnk'] = vi.find('lnk').text
    # get title
    out['title'] = vi.find('ti').text
    # get video info
    v = {}
    v['format'] = 'mp4'	# NOTE the format here should be mp4
    # get size_px
    vw = vi.find('vw').text
    vh = vi.find('vh').text
    v['size_px'] = [int(vw), int(vh)]
    # get file list
    cl = vi.find('cl')	# clip list
    v['file'] = []
    for ci in cl.findall('ci'):
        one = {}
        one['size'] = int(ci.find('cs').text)
        one['time_s'] = float(ci.find('cd').text)
        # NOTE add checksum.md5
        one['checksum'] = {
            'md5' : ci.find('cmd5').text, 
        }
        # NOTE add info for later parse
        one['url'] = {
            'idx' : ci.find('idx').text, 
            'keyid' : ci.find('keyid').text, 
        }
        v['file'].append(one)
    out['video'] = v
    return out	# parse first xml and get info done

def _fix_1080p(pvinfo):
    # TODO not support now
    return pvinfo

def _get_file_urls(pvinfo):
    # TODO not support now
    return pvinfo

# end method_pc_flash_gate.py


