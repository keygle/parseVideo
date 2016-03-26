# letv.py, parse_video/o/plist/lib/e/

from .. import err, b, log
from .. import common

class Var(common.ExtractorVar):
    EXTRACTOR_ID = 'letv'
    EXTRACTOR_NAME = 'letv_1'
    SITE = 'letv'
    SITE_NAME = '乐视视频'

class Entry(common.ExtractorEntry):
    def _do_parse(self, url, method_name=None):
        # TODO support more list page types
        page = common.load_page(url)
        out = _parse_tv_page(page)
        # NOTE set list_url as raw_url
        out['info']['list_url'] = url
        return out
# base parse functions

# http://www.letv.com/tv/10016481.html
def _parse_tv_page(page):
    root = page['dom']
    out = {}
    # get base info
    out['info'] = info = {}
    
    title_i = root.find('div.listTab p.p1 i')[0]
    title = title_i.text()
    info['title'] = title
    
    # get video list info
    out['list'] = []
    
    raw_list = root.find('div.listTab div.listPic div.list dl')
    for dl in raw_list:
        one = {}
        title = dl.find('dd a')[0].text()
        time = dl.find('span.time').text().strip()
        one['title'] = title
        # NOTE not support title_sub here
        # TODO add time_s
        one['time'] = time
        
        url = dl.find('a')[0].attr('href')
        one['url'] = url
        
        out['list'].append(one)
    # add title_no
    for i in range(len(out['list'])):
        out['list'][i]['title_no'] = i + 1
    return out	# end _parse_tv_page

# exports
var = Var()
entry = Entry(var)
parse = entry.parse
# end letv.py


