# vqq.py, parse_video/o/plist/lib/e/

import re

from .. import err, b, log
from .. import common

class Var(common.ExtractorVar):
    EXTRACTOR_ID = 'vqq'
    EXTRACTOR_NAME = 'vqq_1'
    SITE = 'vqq'
    SITE_NAME = '腾讯视频'
    
    # http://s.video.qq.com/loadplaylist?type=6&plname=qq&otype=json&id=mhlu0ezl5yxg9ru
    _LIST_API_BASE = 'http://s.video.qq.com/loadplaylist?type=6&plname=qq&otype=json&id='
    _RE_LIST_ID = 'v\.qq\.com/detail/m/([0-9a-z]+)\.html'

class Entry(common.ExtractorEntry):
    def _do_parse(self, url, method_name=None):
        # TODO support more list page types and more method
        page = common.load_page(url)
        out = _parse_detail_m_page(page, url)
        # set list_url
        out['info']['list_url'] = url
        return out
# base parse functions

# http://v.qq.com/detail/m/mhlu0ezl5yxg9ru.html
def _parse_detail_m_page(page, url):
    root = page['dom']
    out = {}
    # get base info
    out['info'] = info = {}
    title_a = root.find('.video_title .title a')[0]
    info['title'] = title_a.text()
    
    # NOTE use API to get list info
    v_id = re.findall(var._RE_LIST_ID, url)[0]
    raw = _req_list_api(v_id)
    
    # get video list
    raw_list = raw['video_play_list']['playlist']
    out['list'] = []
    for r in raw_list:
        one = {}
        one['title'] = r['title']
        one['title_no'] = int(r['episode_number'])
        # NOTE not support time here
        one['url'] = r['url']
        out['list'].append(one)
    return out	# end _parse_detail_m_page

def _req_list_api(v_id):
    to = var._LIST_API_BASE + str(v_id)
    # TODO error process
    log.i('request API \"' + to + '\" ')
    blob = b.dl_blob(to)
    raw = b.decode_utf8(blob)
    raw = '{' + raw.split('{', 1)[1]
    raw = raw.rsplit('}', 1)[0] + '}'
    info = b.parse_json(raw)
    return info

# exports
var = Var()
entry = Entry(var)
parse = entry.parse
# end vqq.py


