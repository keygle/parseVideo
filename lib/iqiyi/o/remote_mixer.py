# -*- coding: utf-8 -*-
# remote_mixer.py, part for parse_video : a fork from parseVideo. 
# remote_mixer: iqiyi, evparse:lib/o/iqiyi/o/core/model/remote_mixer.py

# import

import random

from . import config as Config
from .key import md5_hash

# import from out
getTimer = None
# NOTE should be set by exports
def set_import(flash):
    # just set getTimer
    global getTimer
    getTimer = flash.getTimer

# class

class MixerRemote(object):
    
    def __init__(self):
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
        self.uuid = ''	# NOTE should be set
        
        # can only pass null
        self.ugcAuthKey = ''	# password string of the video
        self.thdKey = ''
        self.thdToken = ''
        
        # data only for vip
        self.key = ''
        self.QY00001 = ''
        self.communicationlId = ''	# .communicationlId
    
    def getRequest(self):
        
        if self.flag_show_vinfo:
            _loc2_ = 1
        else:
            _loc2_ = 0
        
        _loc3_ = 'Qakh4T0A'
        _loc4_ = getTimer()
        _loc5_ = md5_hash(_loc3_ + str(_loc4_) + self.tvid)
        _loc6_ = md5_hash(md5_hash(self.ugcAuthKey) + str(_loc4_) + self.tvid)
        
        if self.flag_instance_boss:
            _loc7_ = '&vv=821d3c731e374feaa629dcdaab7c394b'
        else:
            _loc7_ = ''
        
        if self.flag_set_um:
            _loc8_ = 1
        else:
            _loc8_ = 0
        
        # before generate url, fix local to string
        _loc2_ = str(_loc2_)
        _loc4_ = str(_loc4_)
        _loc8_ = str(_loc8_)
        
        if not self.flag_is_vip:
            _loc1_ = Config.MIXER_VX_URL
            _ap = ''
            _ap += '?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c'
            _ap += '&tvId=' + self.tvid
            _ap += '&vid=' + self.vid
            _ap += '&vinfo=' + _loc2_
            _ap += '&tm=' + _loc4_
            _ap += '&enc=' + _loc5_
            _ap += '&qyid=' + self.uuid
            _ap += '&puid=' + self.passportID
            _ap += '&authKey=' + _loc6_
            _ap += '&um=' + _loc8_ + _loc7_
            _ap += '&thdk=' + self.thdKey
            _ap += '&thdt=' + self.thdToken
            _ap += '&tn=' + str(random.random())
        # NOTE vip video, not support finished now. 
        else:
            _loc1_ = Config.MIXER_VX_VIP_URL
            _ap = ''
            # FIXME key=fvinp, different from no vip video
            _ap += '?key=fvinp&src=1702633101b340d8917a69cf8a4b8c7c'
            
            _ap += '&tvId=' + self.tvid
            _ap += '&vid=' + self.vid
            
            # TODO only for VIP, start
            _ap += '&cid=' + self.communicationlId
            _ap += '&token=' + self.key
            _ap += '&uid=' + self.QY00001
            _ap += '&pf=b6c13e26323c537d'
            # TODO only for vip end
            
            _ap += '&vinfo=' + _loc2_
            _ap += '&tm=' + _loc4_
            _ap += '&enc=' + _loc5_
            _ap += '&qyid=' + self.uuid
            _ap += '&puid=' + self.passportID
            _ap += '&authKey=' + _loc6_
            _ap += '&um=' + _loc8_ + _loc7_
            _ap += '&thdk=' + self.thdKey
            _ap += '&thdt=' + self.thdToken
            _ap += '&tn=' + str(random.random())
        # just return request URL
        return _loc1_ + _ap
        # an example for not vip method 'http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7c&tvId=362184200&vid=0e8947a1b4fcbde51e943fe9e21f25a1&vinfo=1&tm=796&enc=afbf5e4414ddfec2155093f953449fe8&qyid=cccaa2d11b684850103b7b2f047114ed&puid=&authKey=bb59cba92736f1a251b6f085b943bc91&um=0&thdk=&thdt=&tn=0.7928885882720351'

# end remote_mixer.py


