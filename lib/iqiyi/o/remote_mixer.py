# -*- coding: utf-8 -*-
# remote_mixer.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# remote_mixer: iqiyi, com.qiyi.player.core.model.remote 

# import

import random

from . import config as Config
from .key import md5_hash

from .DMEmagelzzup import DMEmagelzzup

# import from out
getTimer = None
# NOTE should be set by exports
def set_import(flash):
    # just set getTimer
    global getTimer
    getTimer = flash.getTimer

# class

class MixerRemote(object):
    
    def __init__(self, param1=None):
        
        # self._holder = param1;
        
        # add some flags
        self.flag_is_vip = False
        self.flag_show_vinfo = True
        self.flag_set_um = False
        self.flag_instance_boss = False
        
        # add some static config
        self.passportID = ''	# passportID of the user
        
        # add some static data
        self.vid = ''
        self.tvid = ''
        # to get uuid
        self.uuid = '' # NOTE should be set
        
        # can only pass null
        self.ugcAuthKey = ''	# password string of the video
        self.thdKey = ''
        self.thdToken = ''
        
        # data only for vip
        self.key = ''
        self.QY00001 = ''
        self.communicationlId = ''	# .communicationlId
    
    def getRequest(self):
        
        # just reserved
        # self._requestDuration = getTimer()
        # if self._holder.pingBack:
        #     self._holder.pingBack.sendStartLoadVrs()
        
        if self.flag_show_vinfo:
            _loc2_ = 1
        else:
            _loc2_ = 0
        
        # var _loc3:Object = DMEmagelzzup.mix(this._holder.runtimeData.tvid)
        # var _loc4:uint = _loc3.tm
        _loc4 = getTimer()
        
        # NOTE use iqiyi new hash function here
        _loc3 = DMEmagelzzup.mix(self.tvid, _loc4)
        
        # var _loc5:String
        # var _loc6:String
        # var _loc7:String
        _loc5 = md5_hash(md5_hash(self.ugcAuthKey) + str(_loc4) + self.tvid)
        
        _loc6 = ''
        if self.flag_instance_boss:
            _loc6 = '&vv=821d3c731e374feaa629dcdaab7c394b'
        
        _loc7 = 0
        if self.flag_set_um:
            _loc7 = 1
        
        # before generate url, fix local to string
        _loc2 = str(_loc2_)
        _loc4 = str(_loc4)
        _loc7 = str(_loc7)
        
        if not self.flag_is_vip:
            pass
            _loc1 = Config.MIXER_VX_URL
            _ap = ''
            _ap += '?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c'
            _ap += '&tvId=' + self.tvid
            _ap += '&vid=' + self.vid
            _ap += '&vinfo=' + _loc2
            _ap += '&tm=' + _loc4
            _ap += '&enc=' + _loc3['sc']
            _ap += '&qyid=' + self.uuid
            _ap += '&puid=' + self.passportID
            _ap += '&authKey=' + _loc5
            _ap += '&um=' + _loc7 + _loc6
            _ap += '&thdk=' + self.thdKey
            _ap += '&thdt=' + self.thdToken
            _ap += '&tn=' + str(random.random())
            
            # TODO not reset runtimeData.ugcAuthKey
            # self.ugcAuthKey = ''
        # NOTE vip code, TOO old, not been updated
        # NOTE vip video, not support finished now. 
        else:
            pass
        # just return request URL
        return _loc1 + _ap
    pass

# end remote_mixer.py


