# -*- coding: utf-8 -*-
# vauth_remote.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# vauth_remote: iqiyi, com.qiyi.player.core.model.remote.AuthenticationRemote

# import

import time

from .key import md5_hash
from . import config as Config

# class

class AuthRemote(object):
    
    def __init__(self):
        # NOTE should be set start
        self.album_id = ''	# NOTE may be tvid, this._holder.runtimeData.albumId
        self.cid = ''		# NOTE should be cid, this._holder.runtimeData.communicationlId
        self.vid = ''		# NOTE should be vid, this._holder.runtimeData.vid
        self.uuid = ''		# NOTE may be qyid, UUIDManager.instance.uuid
        self.segment_index = 0	# NOTE easy, this._segmentIndex
        # NOTE should be set end
        
        self.play_type = 'main'	# NOTE should be 'main', this._holder.runtimeData.playerType.name
        self.ut = None
    
    def getRequest(self):
        
        # var s :String = null
        # var ut :Number = NaN
        # var utt :String = null
        # var vt :String = null
        # var MdStr :String = null
        # var uts :String = null
        # var request :URLRequest = null
        # var variables :URLVariables = null
        s = None
        ut = None
        utt = None
        vt = None
        MdStr = None
        uts = None
        # request = None
        # variables = None
        
        # NOTE add post data
        post_data = {}
        
        # this._holder.runtimeData.authenticationError = false
        
        # s = uint(0 ^ 2.391461978E9).toString()
        # NOTE should be '2391461978', use avmshell to run the code
        s = '2391461978'
        
        # check self.ut
        if self.ut == None:
            # ut = new Date().time
            ut = int(time.time() * 1e3)
        else:
            ut = self.ut
        
        uts = str(ut)
        
        # utt = String(ut % 1000 * int(uts.substr(0,2)) + (100 + this._segmentIndex));
        utt = str(ut % 1000 * int(uts[0:2]) + (100 + self.segment_index))
        
        _ms = ''
        _ms += self.album_id
        
        _ms += '_' + self.cid
        _ms += '_' + self.vid
        _ms += '_' + uts + '_' + utt + '_' + s
        
        MdStr = _ms
        
        vt = md5_hash(MdStr)
        
        # NOTE delete debug log here
        
        # request = new URLRequest(Config.VIP_AUTH_URL)
        post_url = Config.VIP_AUTH_URL
        
        # NOTE set post data
        # variables = new URLVariables()
        # variables.ut = ut
        # variables.vid = this._holder.runtimeData.vid
        # variables.cid = this._holder.runtimeData.communicationlId
        # variables.aid = this._holder.runtimeData.albumId
        # variables.utt = utt
        # variables.v = vt
        # variables.version = '1.0'
        post_data['ut'] = ut
        post_data['vid'] = self.vid
        post_data['cid'] = self.cid
        post_data['aid'] = self.album_id
        post_data['utt'] = utt
        post_data['v'] = vt
        # post_data['version'] = '1.0'
        post_data['version'] = '1%2E0'
        
        post_data['uuid'] = self.uuid
        
        # if this._holder.runtimeData.playerType:
        #     variables.playType = this._holder.runtimeData.playerType.name;
        if self.play_type != None:
            post_data['playType'] = self.play_type
        
        # variables.platform = 'b6c13e26323c537d'
        post_data['platform'] = 'b6c13e26323c537d'
        
        # done
        # return request
        return post_url, post_data
    
    # end AuthRemote class

# function
def make_post_string(post_data):
    s = ''
    for i in post_data:
        s += '&' + str(i) + '=' + str(post_data[i])
    # remove first &
    s = s[1:]
    # done
    return s

# end vauth_remote.py


