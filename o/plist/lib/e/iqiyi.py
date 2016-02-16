# iqiyi.py, parse_video/o/plist/lib/e/

import re

from .. import err, b, log
from .. import common

# TODO support more list page types

class Var(common.ExtractorVar):
    EXTRACTOR_ID = 'iqiyi'
    EXTRACTOR_NAME = 'iqiyi_1'
    SITE = 'iqiyi'
    SITE_NAME = '癌弃医'
    
    _RE_LIST = {
        'aid' : 'albumId: ([0-9]+),', 	# aid for list API
    }
    _LIST_API_PAGE_SIZE = 50
    # http://cache.video.qiyi.com/jp/avlist/203288601/3/50/
    _LIST_API_BASE = 'http://cache.video.qiyi.com/jp/avlist'
    
    # v page to a page
    _CSS_TO_A = '#datainfo-navlist a'
    # http://www.iqiyi.com/v_19rrl5b1rc.html
    _RE_V_PAGE = '^http://www\.iqiyi\.com/v_([0-9a-z]+)\.html'
    # http://www.iqiyi.com/a_19rrha9kmt.html
    _RE_A_PAGE = '^http://www\.iqiyi\.com/a_([0-9a-z]+)\.html'
    
    # runtime vars data
    _flag_use_list_api = False

class Entry(common.ExtractorEntry):
    
    def _parse_rest_arg(self, r):
        if r == 'use_list_api':
            var._flag_use_list_api = True
        else:	# unknow method arg
            return True
    
    def _do_parse(self, url, method_name=None):
        # NOTE now only support 'html' method here
        # check method_name
        if method_name != 'html':
            raise err.ConfigError('no such method', method_name)
        page = common.load_page(url)
        # NOTE check v page
        try:
            url, page = _check_v_page(url, page)
        except Exception as e:
            er = err.NotSupportURLError('not support this url', url)
            raise er from e
        out = _parse_a_page(page)
        # check use_list_api
        if var._flag_use_list_api:
            out = _do_use_list_api(out, page)
        # NOTE here list_url is just raw_url
        out['info']['list_url'] = url
        return out
# base parse functions

# http://www.iqiyi.com/v_19rrl5b1rc.html
def _check_v_page(url, page):	# get a page from v page
    # check v page url
    if len(re.findall(var._RE_V_PAGE, url)) < 1:
        return url, page	# not v page
    # try to get a page url
    try:
        root = page['dom']
        a = root.find(var._CSS_TO_A)[-1]
        a_url = a.attr('href')
        # check match
        if len(re.findall(var._RE_A_PAGE, a_url)) < 1:
            raise err.MethodError('can not get a_page url', a_url)
    except Exception as e:
        er = err.ConfigError('get a_page url failed')
        raise er from e
    # loading page
    page = common.load_page(a_url)
    return a_url, page

# http://www.iqiyi.com/a_19rrha9kmt.html
def _parse_a_page(page):
    root = page['dom']
    out = {}	# output plinfo
    # get base video info
    out['info'] = {}
    info = out['info']
    
    # get title
    crumb = root.find('div.crumb-item')[0]
    crumb_s = crumb.find('a>strong')
    title = crumb_s[-1].text()
    
    info['title'] = title
    
    # get video list info
    out['list'] = []
    
    block_i = root.find('div#block-I')[0]
    li = block_i.find('ul>li')
    for i in li:	# get each video item info
        one = {}
        
        a = i.find('div.site-piclist_info a')
        title = a[0].text()
        title_sub = a[1].text()
        time = i.find('span.mod-listTitle_right').text()
        # TODO add time_s
        one['title'] = title
        one['title_sub'] = title_sub
        one['time'] = time
        
        url = i.find('a')[0].attr('href')
        one['url'] = url
        
        out['list'].append(one)
    # add title_no
    for i in range(len(out['list'])):
        out['list'][i]['title_no'] = i + 1
    return out	# end _parse_a_page

# for use_list_api
def _do_use_list_api(raw, page):
    raw_html = page['text']
    list_info = _get_list_from_api(raw_html)
    # update list info
    out = raw
    out['list'] = list_info
    return out

# get list info with API
def _get_list_from_api(raw_html_text):
    # TODO ERROR process here
    aid = _get_aid(raw_html_text)
    page_no = 1
    raw_list = []
    while True:
        api_url = _make_list_api_url(aid, page_no=page_no)
        log.i('request list API \"' + api_url + '\" ')
        raw = b.dl_blob(api_url).decode('utf-8')
        info = _parse_one_list_info(raw)
        # check exit loop
        if len(info) < 1:
            break
        # append list info
        raw_list += info
        page_no += 1
    out = _gen_list_info(raw_list)
    return out

def _get_aid(raw_html_text):
    aid = re.findall(var._RE_LIST['aid'], raw_html_text)[0]
    return aid

def _make_list_api_url(aid, page_no=1, page_size=None):
    if page_size == None:
        page_size = var._LIST_API_PAGE_SIZE
    out = ('/').join([var._LIST_API_BASE, str(aid), str(page_no), str(page_size), ''])
    return out

def _parse_one_list_info(raw):
    # get json text
    text = raw.split('=', 1)[1]
    info = b.parse_json(text)
    
    out = info['data']['vlist']
    return out

def _gen_list_info(raw):
    out = []
    for i in raw:
        one = {}
        # NOTE not support title here
        one['title_sub'] = i['vt']
        one['title_no'] = i['pd']
        one['time_s'] = i['timeLength']
        
        one['url'] = i['vurl']
        out.append(one)
    return out

# exports
var = Var()
entry = Entry(var)
parse = entry.parse
# end iqiyi.py


