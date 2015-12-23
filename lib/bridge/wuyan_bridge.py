# wuyan_bridge.py, parse_video/lib/bridge/

from .wy_bridge import salt

def _default_salt_bite(tvid, tm):
    enc = salt.bite(tvid, tm)
    return enc, tm

# NOTE set bridge callback function here
bks1_bite = _default_salt_bite

# end wuyan_bridge.py


