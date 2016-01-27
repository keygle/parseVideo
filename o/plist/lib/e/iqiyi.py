# iqiyi.py, parse_video/o/plist/lib/e/

from .. import err, b, log
from .. import common

# TODO use list api to get more info

class Var(common.ExtractorVar):
    EXTRACTOR_ID = 'iqiyi'
    EXTRACTOR_NAME = 'iqiyi_1'
    SITE = 'iqiyi'
    SITE_NAME = '癌弃医'

class Entry(common.ExtractorEntry):
    def _do_parse(self, url):
        # TODO support more list page types
        page = common.load_page(url)
        out = _parse_a_page(page)
        # NOTE here list_url is just raw_url
        out['info']['list_url'] = url
        return out
# base parse functions

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

# exports
var = Var()
entry = Entry(var)
parse = entry.parse
# end iqiyi.py


