# -*- coding: utf-8 -*-
# ListNewProxy.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# ListNewProxy: letv/letvplayer, com.letv.player.model.proxy

# import

# global config

URL0 = 'http://api.letv.com/mms/out/album/videos'

# class

class ListNewProxy(object):
    
    def __init__(self):
        # NOTE should be set
        self.pid = ''
        self.cid = ''
        self.vid = ''
        # other data
        self.page = 0
        self.page_size = 10000	# NOTE get all info
        # done
    
    def load(self):
        # make url
        url = URL0
        url += '?id=' + self.pid
        url += '&cid=' + self.cid
        url += '&platform=pc'
        url += '&page=' + str(self.page)
        url += '&size=' + str(self.page_size)
        url += '&vid=' + self.vid
        url += '&queryType=1'
        # done
        return url
    # end ListNewProxy class

# end ListNewProxy.py


