# method_android.py, parse_video/lib/e/pptv/

from ... import err, b
from .. import common

from .var import var
from . import method

class Method(method.Method):
    
    def _make_first_url(self, vid_info):
        BEFORE = 'http://play.api.pptv.com/boxplay.api?platform=android3&type=phone.android&userType=1&&id='
        out = BEFORE + str(vid_info['cid'])
        return out
    
    # sub parse first functions
    def _get_size_px(self, data):
        item = data['item']
        px_x = int(item.get('width'))
        px_y = int(item.get('height'))
        return [px_x, px_y]
    
    def _get_file_info(self, data, channel):
        time_s = float(channel.get('dur'))
        # gen only one file info
        item = data['item']
        f = {}
        f['size'] = int(item.get('filesize'))
        f['time_s'] = time_s
        # gen file url
        rid = item.get('rid')
        f['url'] = _gen_one_file_url(rid, data['dt'])
        return [f]
    # end Method class

# base parse function

def _gen_one_file_url(rid, dt):
    PART_1 = '?w=1&platform=android3&type=phone.android&k='
    
    sh = dt.find('sh').text
    k = dt.find('key').text
    
    out = 'http://' + sh + '/' + str(rid) + PART_1 + k
    return out

# exports
_method = Method(var)
parse = _method.parse
# end method_android.py


