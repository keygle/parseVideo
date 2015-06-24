# -*- coding: utf-8 -*-
# remote_mixer.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# remote_mixer: iqiyi, com.qiyi.player.core.model.remote 

# import

import random

from . import node_port
from .key import md5_hash
from . import config as Config

# NOTE last update 201506241630 GMT+0800

# class

class MixerRemote(object):
    
    def __init__(self):
        
        # some flags
        self.flag_is_vip = False
        self.flag_instance_boss = False
        self.flag_set_vinfo = True	# default should be True
        self.flag_set_um = False	# NOTE vip should set this
        
        # NOTE should be set START
        self.tm = 0	# NOTE should be tm, flash getTimer()
        self.tvid = ''	# NOTE should be tvid
        self.vid = ''	# NOTE should be vid, this._holder.runtimeData.originalVid
        self.qyid = ''	# NOTE should be qyid, this._holder.uuid
        
        # NOTE only for VIP
        self.cid = ''	# NOTE should be cid, this._holder.runtimeData.communicationlId
        self.token = ''	# NOTE should be token, this._holder.runtimeData.key
        self.uid = ''	# NOTE should be uid, this._holder.runtimeData.QY00001
        
        # NOTE should be set END
        
        # NOTE for VIP, may be empty
        self.puid = ''	# NOTE should be puid, UserManager.getInstance().user.passportID
        
        # NOTE can be null, empty
        self.ugcAuthKey = ''
        self.thdk = ''	# NOTE should be thdk, this._holder.runtimeData.thdKey
        self.thdt = ''	# NOTE should be thdt, this._holder.runtimeData.thdToken
    
    def getRequest(self):
        
        # var _loc1:String = null;
        _loc1 = None
        
        # this._requestDuration = getTimer();
        
        # if this._holder.pingBack:
        #     this._holder.pingBack.sendStartLoadVrs();
        
        # var _loc2:* = 0;
        _loc2 = 0
        # if (this._holder.runtimeData.CDNStatus == -1 && this._holder.runtimeData.playerUseType == PlayerUseTypeEnum.MAIN):
        if self.flag_set_vinfo:
            _loc2 = 1
        
        # var _loc3:Object
        # var _loc4:uint = _loc3.tm
        # var _loc5:String
        # var _loc6:String = Settings.instance.boss?"&vv=821d3c731e374feaa629dcdaab7c394b":"";
        # var _loc7:String = (UserManager.getInstance().user) && !(UserManager.getInstance().user.level == UserDef.USER_LEVEL_NORMAL)?"1":"0";
        
        # NOTE use node_port to mix
        # _loc3 = Z7elzzup.cexe(this._holder.runtimeData.tvid)
        _loc3 = node_port.mix(self.tvid, self.tm)
        
        _loc4 = _loc3.tm
        
        # NOTE authKey
        # _loc5 = MD5.calculate(MD5.calculate(this._holder.runtimeData.ugcAuthKey) + String(_loc4) + this._holder.runtimeData.tvid)
        _loc5 = md5_hash(md5_hash(self.ugcAuthKey) + str(_loc4) + self.tvid)
        
        # _loc6 = Settings.instance.boss?"&vv=821d3c731e374feaa629dcdaab7c394b":""
        _loc6 = ''
        if self.flag_instance_boss:
            _loc6 = '&vv=821d3c731e374feaa629dcdaab7c394b'
        
        # NOTE set um, vip flag
        # _loc7 = (UserManager.getInstance().user) && !(UserManager.getInstance().user.level == UserDef.USER_LEVEL_NORMAL)?"1":"0";
        _loc7 = '0'
        if self.flag_set_um:
            _loc7 = '1'
        
        # NOTE mix vip and normal together
        
        _a = ''	# append string
        
        # if ! this._holder.runtimeData.movieIsMember:
        if not self.flag_is_vip:
            _loc1 = Config.MIXER_VX_URL
            _a += '?key=fvip'
        else:	# NOTE here is VIP
            _loc1 = Config.MIXER_VX_VIP_URL
            _a += '?key=fvinp'
        
        _a += '&src=1702633101b340d8917a69cf8a4b8c7c'
        
        _a += '&tvId=' + self.tvid
        _a += '&vid=' + self.vid
        
        if self.flag_is_vip:
            # NOTE only for VIP start
            _a += '&cid=' + self.cid
            _a += '&token=' + self.token
            _a += '&uid=' + self.uid
            _a += '&pf=b6c13e26323c537d'
            # NOTE only for VIP end
        
        _a += '&vinfo=' + str(_loc2)
        
        _a += '&tm=' + str(_loc4)
        _a += '&enc=' + _loc3.sc
        
        _a += '&qyid=' + self.qyid
        _a += '&puid=' + self.puid
        _a += '&authKey=' + _loc5
        _a += '&um=' + str(_loc7)
        
        _a += _loc6
        
        _a += '&thdk=' + self.thdk
        _a += '&thdt=' + self.thdt
        
        _a += '&tn=' + str(random.random())
        
        # add str done
        # NOTE just reserved
        # this._holder.runtimeData.ugcAuthKey = ''
        
        _loc1 += _a
        
        # done
        # return new URLRequest(_loc1);
        return _loc1
    
    # end MixerRemote class

# end remote_mixer.py


