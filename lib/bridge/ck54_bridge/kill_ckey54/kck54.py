# kck54.py, kill_ckey54, for parse_video bridge/

import uuid

from .echo_ckeyv3 import echo_ckeyv3

# global data
etc = {}
# default platform for gen ckey
etc['enc_ver'] = '5.4'
etc['player_version'] = '3.2.19.346'
etc['default_platform'] = 11

# NOTE should gen uuid here
etc['uuid'] = uuid.uuid4().hex

# main gen_ckey function
def gen_ckey(vid, platform = etc['default_platform'], userid = etc['uuid'], referer = ''):
    player_version = etc['player_version']
    # NOTE use echo_ckeyv3 to gen ckey
    ckey = echo_ckeyv3(vid, guid=userid, player_version=player_version, platform=platform)
    # make output info
    out = {}
    out['enc_ver'] = etc['enc_ver']
    out['player_ver'] = player_version
    out['ckey'] = ckey
    out['vid'] = vid
    out['platform'] = platform
    out['userid'] = userid
    out['referer'] = referer
    return out	# done

# end kck54.py


