# method.py, parse_video/lib/e/pptv/

import json
import xml.etree.ElementTree as ET
import datetime

from ... import err, b
from ...b import log
from .. import common, log_text

from .var import var

class Method(common.ExtractorMethod):   # common method class for extractor pptv
    
    def _fix_vid_info(self, out):
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
    
    # get video info and file URLs
    def _get_video_info(self, vid_info):
        first_url = self._make_first_url(vid_info)
        first = self._dl_first_xml(first_url)
        
        pvinfo = self._parse_raw_first(first)
        
        # NOTE count and select here
        out = common.method_simple_count_and_select(pvinfo, var)
        return out
    
    def _dl_first_xml(self, first_url):
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
    
    def _do_parse_first(self, first):
        out, channel = raw_first_get_base_info(first)
        # collect info by ft, NOTE ft as str
        info = self._collect_info(channel, first)
        
        # gen video info
        out['video'] = []
        for ft, data in info.items():
            one = {}
            one['hd'] = var.TO_HD[str(ft)]
            one['size_px'] = self._get_size_px(data)
            one['format'] = 'mp4'	# NOTE the video file format should be mp4
            
            # gen file list
            one['file'] = self._get_file_info(data, channel)
            # add expire time
            expire = get_expire(data['dt'])
            for f in one['file']:
                f['expire'] = expire
            out['video'].append(one)
        return out
    
    # sub parse first functions
    def _collect_info(self, channel, first):
        info = {}
        # get channel.file[]item
        file_item = channel.find('file').findall('item')
        for i in file_item:
            ft = str(i.get('ft'))
            if not ft in info:
                info[ft] = {}
            info[ft]['item'] = i
        # get dt
        dt_list = first.findall('dt')
        for dt in dt_list:
            ft = str(dt.get('ft'))
            info[ft]['dt'] = dt
        return info
    
    # for sub class
    def _get_size_px(self, data):
        raise NotImplementedError
    def _get_file_info(self, data, channel):
        raise NotImplementedError
    # end Method class

# base parse functions

def raw_first_get_base_info(first):
    channel = first.find('channel')
    out = {}
    # get base video info
    out['info'] = {}
    out['info']['title'] = channel.get('nm')
    out['info']['title_short'] = channel.get('hjnm')
    return out, channel

def get_expire(dt):
    key = dt.find('key')
    date = _get_key_expire(key)
    expire = b.print_time_iso(date)
    return expire

def _get_key_expire(key):
    date_format = '%a %b %d %H:%M:%S %Y %Z'
    expire_time = key.get('expire')
    expire = datetime.datetime.strptime(expire_time, date_format)
    return expire

# end method.py


