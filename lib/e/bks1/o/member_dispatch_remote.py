# member_dispatch_remote.py, parse_video/lib/e/bks1/o/
# package com.qiyi.player.core.model.remote.MemberDispatchRemote

import random

# package com.qiyi.player.core.player.RuntimeData.communicationlId
CID = 'afbe8fd3d73448c9'

# MemberDispatchRemote.getRequest()
def get_request(
        raw_url, 
        vid, 
        key, 		# vv token
        uid='', 	# NOTE QY00001 is uid
        qyid='', 
        
        tn=None, 
        cid=CID):
    # override protected function getRequest() : URLRequest
    
    # replace '.f4v' with '.hml'
    out = raw_url.replace('.f4v', '.hml')
    # add more args
    if '?' in out:
        out += '&'
    else:
        out += '?'
    out += 't=' + key
    out += '&cid=' + cid
    out += '&vid=' + vid
    out += '&QY00001=' + uid
    # NOTE not needed args
    #if start != None:
    #    out += '&start=' + str(start)
    #if retry > 0:
    #    out += '&retry=' + str(retry)
    out += '&su=' + qyid
    #out += '&client=' + current_user_ip
    #out += '&z=' + pre_dispatch_area
    #out += '&mi=' + movie_info
    #out += '&bt=' + pre_def
    #out += '&ct=' + current_def
    #if pre_average_speed > 0:
    #    out += '&s=' + pre_average_speed
    #out += '&e=' + pre_err_code
    out += '&qyid=' + qyid
    if tn == None:
        tn = gen_tn()
    out += '&tn=' + str(tn)
    return out

def gen_tn():
    return random.randint(1000, 5000)

# end member_dispatch_remote.py


