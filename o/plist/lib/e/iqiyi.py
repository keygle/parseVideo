# iqiyi.py, parse_video/o/plist/lib/e/

from .. import err, b, log
from .. import common

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
    crumb = root.find('div.crumb-item')
    crumb_s = crumb[0].find('a>strong')
    title = crumb_s[-1].text()
    
    info['title'] = title
    
    log.w('iqiyi._parse_a_page() not finished ')
    
    # get video list info
    out['list'] = []
    # TODO
    return out

# exports
var = Var()
entry = Entry(var)
parse = entry.parse
# end iqiyi.py


