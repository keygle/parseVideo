# kill_ckey_bridge.py, parse_video/lib/bridge/, for extractor vqq

from .ck54_bridge.kill_ckey54 import kck54

# gen ckey5.4 with python code
def _default_gen_ckey(vid, platform=11, userid='', referer=''):
    return kck54.gen_ckey(vid, platform=platform, userid=userid, referer=referer)

# gen_ckey(vid, 
#         platform=11, 
#         userid='', 
#         referer=''):
# -> {
#     'enc_ver' : '', 
#     'player_ver' : '', 
#     
#     'ckey' : '', 
#     'vid' : '', 
#     'platform' : , 
#     'userid' : '', 
#     'referer' : '', 
# }
gen_ckey = _default_gen_ckey
# NOTE set bridge callback function here

# end kill_ckey_bridge.py


