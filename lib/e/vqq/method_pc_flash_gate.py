# method_pc_flash_gate.py, parse_video/lib/e/vqq/
# TODO rewrite and clean code here

import re
import xml.etree.ElementTree as ET

from ... import err, b
from ...b import log
from .. import common

from .var import var
from .o import player

class Method(common.ExtractorMethod):
    def _init_data(self):
        self._v1080 = None  # for fix_1080p
    
    def _parse_arg_rest(self, r):
        if r == 'fix_1080p':
            var._['flag_fix_1080p'] = True
        elif r == 'ignore_fix_1080p_error':
            var._['flag_ignore_fix_1080p_error'] = True
        elif r == 'enable_fmt_black_list':
            var._['flag_enable_fmt_black_list'] = True
            log.d('use fmt_black_list ' + str(var._['fmt_black_list']) + ' ')
        elif r == 'fast_parse':
            var._['flag_fast_parse'] = True
        elif r == 'add_raw_quality':
            var._['flag_add_raw_quality'] = True
        else:
            return True
    
    # NOTE get vid info from vqq html page is not very easy
    def _re_get_vid(self, raw_text):
        # TODO rewrite and clean code here
        raw_url = var._['_raw_url']
        # get scripts
        raw_scripts = raw_text.split('<script')
        scripts = [r.split('</script>')[0] for r in raw_scripts]
        # get key script part
        script = None
        for s in scripts:	# check key words
            if ('COVER_INFO' in s) and ('VIDEO_INFO' in s):
                script = s
                break
        if not script:	# check found
            er = err.NotSupportURLError('get vid_info, find script text failed ', raw_url)
            er.html_text = raw_text
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
            def re_get(r, raw):
                return re.findall(re_list[r], raw)[0]
            re_list = var.RE_VID_LIST
            out = {}
            out['title_short'] = re_get('title_short', raw_cover)
            out['title_sub'] = re_get('title_sub', raw_cover)
            out['title_no'] = re_get('title_no', raw_video)
            out['vid'] = re_get('vid', raw_video)
        except Exception as e:
            er = err.NotSupportURLError('get vid_info items from page html script text failed ', raw_url)
            er.html_text = raw_text
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
        try:	# NOTE fix Error here, int(title_no)
            out['title_no'] = int(out['title_no'])
        except Exception as e:
            # WARNING log
            log.w('get title_no failed, \"' + str(out['title_no']) + '\", ' + str(e) + ' ')
            out['title_sub'] += '-' + str(out['title_no'])	# NOTE add title_no to title_sub first
            # get title_no failed, NOTE reset title_no
            out['title_no'] = -1
        return out	# get vid_info done
    
    def _get_video_info(self, vid_info):
        # TODO support fast_parse here
        pvinfo = _do_get_video_info(vid_info)
        if var._['flag_fix_1080p']:	# NOTE fix_1080p
            self._v1080 = self._fix_1080p(pvinfo)
        out = common.method_simple_count_and_select(pvinfo, var)
        return out
    
    def _do_parse_first(self, first):
        return _do_parse_one_first(raw)
    
    def _fix_1080p(self, pvinfo):
        try:
            out = _do_fix_1080p(pvinfo)
        except Exception as e:
            if var._['flag_ignore_fix_1080p_error']:
                # WARNING log
                log.w('ignored fix_1080p Error, ' + str(e))
                out = None	# NOTE if failed, return None
            else:
                er = err.ParseError('fix_1080p failed')
                raise er from e
        return out
    
    def _get_file_urls(self, pvinfo):
        out = _get_raw_file_urls(pvinfo)	# NOTE count and select before get file URLs
        # add 1080p video info
        v1080p = self._v1080
        if var._['flag_fix_1080p'] and (v1080p != None):
            common.method_count_one_video(v1080p)
            out['video'].append(v1080p)
        common.method_sort_video(out)
        out = _gen_final_urls(out)	# gen final url, NOTE will also gen fix_1080p file URLs
        return out
    # end Method class

# base parse functions

# get raw first

def _do_get_video_info(vid_info):
    _get_first_xml_info(vid_info)
    # create pvinfo
    out = {}
    out['info'] = {}
    for key in ['title', 'title_sub', 'title_short', 'title_no']:
        out['info'][key] = vid_info[key]
    # get video list
    raw_list = var._['_raw_xml_root']
    out['video'] = []
    for fmt, raw in raw_list.items():
        info = _do_parse_one_first(raw[0])
        one = info['video']
        one['hd'] = var.TO_HD[fmt]
        # add more info for later parse
        d = {}
        d['fn'] = info['fn']
        d['lnk'] = info['lnk']
        d['id'] = raw[1]['id']
        d['name'] = raw[1]['name']
        d['cname'] = raw[1]['cname']
        one['_data'] = d
        # NOTE add raw quality text here
        if var._['flag_add_raw_quality']:
            one['quality'] = d['cname']
        out['video'].append(one)
    common.method_sort_video(out)
    return out

def _get_first_xml_info(vid_info):
    # TODO support fast_parse here
    vid = vid_info['vid']
    first_post = player.getvinfo(vid)
    first_root, first_xml = _do_one_post_xml(first_post, log_debug=False)	# INFO log
    # TODO to get first type here, to dec one POST request
    first_info = _do_parse_one_first(first_root)
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
            # add limit info to limit list
            var._['_limit_list'][str(i['name'])] = i
        # check fmt black list
        elif var._['flag_enable_fmt_black_list'] and (i['name'] in var._['fmt_black_list']):
            log.d('skip fmt ' + i['name'] + ' in fmt_black_list ')
        else:	# make todo info
            post_info = player.getvinfo(vid, video_format=i['name'])
            todo.append((i, post_info))
    pool_size = var._['pool_size']['get_formats']
    # INFO log
    log.i('getting video info, count ' + str(len(todo)) + ', pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo, worker=_dl_one_first, pool_size=pool_size)
    log.d('got video info (first) done ')
    # save result
    for r in result:
        fmt = r['fmt']
        var._['_raw_first_xml'][fmt] = r['xml']
        # save xml root
        var._['_raw_xml_root'][fmt] = (r['root'], r['format'])
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
    out['format'] = info[0]
    return out

# parse raw first
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
        # NOTE the md5 is not right
        ## NOTE add checksum.md5
        #one['checksum'] = {
        #    'md5' : ci.find('cmd5').text, 
        #}
        # NOTE add info for later parse
        one['url'] = {
            'idx' : ci.find('idx').text, 
            'keyid' : ci.find('keyid').text, 
        }
        v['file'].append(one)
    out['video'] = v
    return out	# parse first xml and get info done

# get file urls

def _get_raw_file_urls(pvinfo):
    # NOTE just use first server here
    server = var._['_server_list'][0]
    vt = server['vt']
    
    # make post data to get vkey
    for v in pvinfo['video']:
        for i in range(len(v['file'])):
            f = v['file'][i]
            if f['url'] != '':
                v['file'][i] = _make_one_file_post_data(f, v['_data'], vt)
        v.pop('_data')	# remove _data
    # do POSTs
    def worker(f, i):
        post_info = f.pop('_post_info')	# NOTE remove _post_info data
        root, xml_text = _do_one_post_xml(post_info, prefix='get vkey ' + str(i) + ' ')
        # TODO check OK code and Error process
        # get vkey
        vkey = root.find('key').text
        f['_vkey'] = vkey	# save vkey
        return f
    pool_size = var._['pool_size']['get_file_url']
    return common.simple_get_file_urls(pvinfo, worker, msg='getting part file vkey', pool_size=pool_size)

def _gen_final_urls(pvinfo):
    # NOTE use first server
    server = var._['_server_list'][0]
    # gen final file URLs
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                f['url'] = _gen_one_final_url(f, server)
    return pvinfo

def _make_one_file_post_data(f, data, vt):
    fn = data['fn']
    fn_parts = fn.rsplit('.', 1)
    idx = f['url']['idx']
    filename = ('.').join([fn_parts[0], idx, fn_parts[1]])
    
    vid = data['lnk']
    format_ = data['id']
    # gen post info
    post_info = player.getvkey(vid, format_ = format_, vt = vt, filename = filename)
    # NOTE save post_info
    f['_post_info'] = post_info
    f['url'] = filename	# NOTE save filename in f.url
    return f

def _gen_one_final_url(f, server):
    vkey = f.pop('_vkey')
    filename = f['url']	# NOTE set filename to f.url
    server_url = server['url']
    if server_url[-1] != '/':
        server_url += '/'
    # make final url
    out = server_url + filename + '?vkey=' + vkey
    return out

# do one POST and get xml info
def _do_one_post_xml(raw, log_debug=True, prefix=''):
    # do log text
    log_text = prefix + 'POST \"' + raw['url'] + '\" with data \"' + b.make_post_str(raw['post_data'], quote=True) + '\" '
    if log_debug:
        log.d(log_text)	# DEBUG log
    else:
        log.i(log_text)	# INFO log
    raw_blob = b.post_form(raw['url'], header=raw['header'], post_data=raw['post_data'], quote=True)
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

# fix 1080p
def _do_fix_1080p(pvinfo):
    # get 720p info from pvinfo
    v720 = None
    for v in pvinfo['video']:
        if v['hd'] == 2:
            v720 = v
            break
    if v720 == None:
        # WARNING log
        log.w('no 720p video info, can not fix_1080p ')
        return None	# no 720p video
    # check 1080p info
    if not 'fhd' in var._['_limit_list']:
        # WARNING log
        log.w('no 1080p video info, can not fix_1080p ')
        return None
    data = var._['_limit_list']['fhd']	# NOTE 1080p fmt is fhd
    # make post data list
    server = var._['_server_list'][0]	# NOTE use first server
    vt = var._['_server_list'][0]['vt']
    
    fmt = data['name']
    format_ = data['id']
    vid = v720['_data']['lnk']
    
    todo = []
    i = 0
    for f in v720['file']:
        idx = f['url']['idx']
        one = player.getvclip(vid, idx, fmt, format_, vt)
        one['i'], i = i, i + 1	# add index for DEBUG
        todo.append(one)
    def worker(one):
        prefix = 'index ' + str(one['i']) + ' get vclip, '
        root, xml_text = _do_one_post_xml(one, prefix=prefix)
        # TODO check code OK
        vi = root.find('vi')
        out = {}
        out['filename'] = vi.find('fn').text
        out['size'] = int(vi.find('fs').text)
        out['md5'] = vi.find('md5').text
        out['vkey'] = vi.find('key').text
        
        log.d('done index ' + str(one['i']) + ' ')
        return out
    pool_size = var._['pool_size']['fix_1080p']
    log.i('starting fix_1080p, count ' + str(len(todo)) + ', pool_size = ' + str(pool_size) + ' ')
    result = b.map_do(todo, worker=worker, pool_size=pool_size)
    log.d('do vclip POSTs info done. ')
    
    # gen video info
    v = {}
    v['hd'] = var.TO_HD[fmt]
    if var._['flag_add_raw_quality']:
        v['quality'] = data['cname']
    v['size_px'] = [-1, -1]	# NOTE can not get size_px info
    v['format'] = v720['format']
    # add files
    raw = v720['file']
    v['file'] = []
    for i in range(len(result)):
        r = result[i]
        one = {}
        one['size'] = r['size']
        one['time_s'] = raw[i]['time_s']
        # NOTE disable checksum.md5, not works
        #one['checksum'] = {	# add checksum
        #    'md5' : r['md5'], 
        #}
        # save filename in f.url
        one['url'] = r['filename']
        one['_vkey'] = r['vkey']
        v['file'].append(one)
    return v	# fix_1080p, finished

# exports
_method = Method(var)
parse = _method.parse
# end method_pc_flash_gate.py


