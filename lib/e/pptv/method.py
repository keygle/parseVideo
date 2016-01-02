# method.py, parse_video/lib/e/pptv/

import json
import functools
import xml.etree.ElementTree as ET

from ... import err, b
from ...b import log
from .. import common, log_text

from . import var

# support --more
def get_raw_more(method_arg_text):
    data_list = [	# NOTE --more mode to direct get vid_info
        'vid_info', 
    ]
    raw_more = common.method_simple_check_use_more(var, method_arg_text, data_list)
    return raw_more

def get_vid_info():
    default_get_vid_info = functools.partial(common.parse_load_page_and_get_vid, var, _do_get_vid_info)
    # get vid_info from more if possible
    vid_info = common.method_more_simple_get_vid_info(var, default_get_vid_info)
    return vid_info

def _do_get_vid_info(raw_html_text):
    def do_get(raw_html_text):
        out = common.method_vid_re_get(raw_html_text, var.RE_VID_LIST)
        try:	# parse webcfg as json
            out['webcfg'] = json.loads(out['webcfg'])
        except Exception as e:
            er = err.MethodError('parse webcfg json text failed', out['webcfg'])
            raise er from e
        # get more info from webcfg
        cfg = out['webcfg']
        out['cid'] = cfg['id']
        out['ctx'] = cfg['player']['ctx']
        return out
    return common.method_get_vid_info(raw_html_text, var, do_get)

def check_enable_more(out):
    # check enable_more
    if var._['enable_more']:
        out['_data'] = {}
        out['_data']['vid_info'] = var._['_vid_info']
    return out

def dl_first_xml(first_url):
    # [ OK ] log
    log.o(log_text.method_got_first_url(first_url))
    # NOTE download and parse as xml
    first_xml = b.dl_html(first_url)
    var._['_raw_first_xml'] = first_xml	# save raw xml text
    try:
        first  = ET.fromstring(first_xml)
    except Exception as e:
        er = err.ParseXMLError('parse first xml text failed, first_url ', first_url)
        er.text = first
        raise er from e
    # check first Error
    if first.find('error') != None:
        raise err.MethodError('first xml info Error', ET.dump(first.find('error')))
    var._['_vid_info']['vip'] = str(first.find('channel').get('vip'))
    return first

def raw_first_get_base_info(first):
    channel = first.find('channel')
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = channel.get('nm')
    out['info']['title_short'] = channel.get('hjnm')
    return out, channel

# end method.py


