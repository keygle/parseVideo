# -*- coding: utf-8 -*-
# transfer.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# transfer: letv/kletvplayer, com.letv.plugins.kernel.controller.auth.transfer 

# import

from .TimeStamp import TimeStamp

# import from out

# global config
URL3 = 'http://api.letv.com/mms/out/video/playJson?id='
URL4 = 'http://117.121.54.104/mms/out/video/playJson?id='

# class

class IDTransfer(object):
    
    def __init__(self):
        # create timestamp
        self.timestamp = TimeStamp()
        self.base_url = URL3
        
        # static data
        self.platid = None
        self.splatid = None
        self.domain = 'www.letv.com'
        
        # done
    
    # NOTE method add by me, not one of in kletvplayer
    def set_stime(self, stime):
        # set server time
        self.timestamp.stime = stime
    
    # make the URL to get video info json, with tkey
    def getURL(self, vid):
        _loc2_ = self.base_url + str(vid)
        
        # NOTE fix splatid from piaopiao
        _loc2_ += '&platid=3&splatid=301'
        
        # NOTE reserved old code here
        # NOTE fix platid and splatid here, for o/tscn2 method
        # _loc2_ += '&platid=5&splatid=503'
        #
        # _loc2_ += '&platid='
        # if self.platid != None:
        #     _loc2_ += self.platid
        # else:	# 
        #     _loc2_ += '1'
        # 
        # _loc2_ += '&splatid='
        # if self.splatid != None:
        #     _loc2_ += self.splatid
        # else:	# NOTE fix parse_more_url here
        #     _loc2_ += '1401'
        #     # _loc2_ += '101'
        # 
        # _loc2_ += '&format=1'
        
        # add tkey
        tkey = self.timestamp.calcTimeKey()
        _loc2_ += '&tkey=' + str(tkey)
        _loc2_ += '&domain=' + self.domain
        # done
        return _loc2_
    
    # end IDTransfer class

# end transfer.py


