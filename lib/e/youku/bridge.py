# bridge.py, parse_video/lib/e/youku/

from ...bridge import kill_ccyouku_bridge
# package com.youku.utils.PlayListUtil

# setSize(raw :str) -> str
def set_size(raw):
    out = kill_ccyouku_bridge.youku_set_size(raw)
    return out

# getSize(raw :str) -> str
def get_size(raw):
    out = kill_ccyouku_bridge.youku_get_size(raw)
    return out

# changeSize(raw :str) -> str
def change_size(raw):
    out = kill_ccyouku_bridge.youku_change_size(raw)
    return out

# end bridge.py


