# salt.py, parse_video/lib/bridge/wy_bridge/

from ...b import md5_hash

SALT = 'd7184ccc20a84a9d8be798087386b6b8'

def bite(tvid, tm):
    raw = SALT + str(tm) + tvid
    return md5_hash(raw)

# end salt.py


