# -*- coding: utf-8 -*-
# uuid.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# uuid: bks1, com.71.player.base.uuid 

# import

import random
import re
import json

from .. import s1

# import from out
base = None
# NOTE should be set by exports
def set_import(base1):
    global base
    base = base1

# global static config
UUID_URL = 'http://data.video.' + s1.get_s1()[1] + '.com/uid'

LOAD_UUID_RETRY = 5

# class

class UUIDManager(object):
    
    def __init__(self):
        self.uuid = ''
    
    def get_uuid(self, flag_debug=False):
        # check uuid
        if self.uuid != '':
            return self.uuid
        # load from server
        self.uuid = self._load_from_server(flag_debug)
        return self.uuid
    
    # auto retry load
    def _load_from_server(self, flag_debug):
        retry = 0
        while retry < LOAD_UUID_RETRY:
            try:
                uid = self._load_from_server0(flag_debug)
                return uid
            except Exception as err:
                if retry >= LOAD_UUID_RETRY:
                    raise Exception('DEBUG: load uuid retry' + str(retry) + ' failed', err)
        # done
    
    # load a user uuid from bks1 server
    def _load_from_server0(self, flag_debug):
        # make a url to request
        url_to = UUID_URL + '?tn=' + str(random.random())
        # DEBUG info
        if flag_debug:
            print('lib/bks1/o/uuid: DEBUG: request \"' + url_to + '\"')
        try:
            # get uuid by http request
            info = base.get_html_content(url_to)
        except Exception as err:
            raise Exception('DEBUG: bks1, load uuid http error', err)
        # an example of info
        # 'var uid={"uid":"f21e1ae1c44f6c40f0674316ba7cf55b"};'
        # analyse received text
        uid_raw = re.findall('var uid=([^;]+);', info)
        json_text = uid_raw[0]
        uid_info = json.loads(json_text)
        uid = uid_info['uid']
        # done
        return uid

# end uuid.py


