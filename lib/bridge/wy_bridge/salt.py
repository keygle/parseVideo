# salt.py, parse_video/lib/bridge/wy_bridge/

from ...b import md5_hash

# update from you-get <https://github.com/soimort/you-get/blob/develop/src/you_get/extractors/iqiyi.py#L48> at 2016-03-26 T 15:01 GMT+0800 (CST) 
SALT = '4a1caba4b4465345366f28da7c117d20'

def bite(tvid, tm):
    raw = SALT + str(tm) + tvid
    return md5_hash(raw)

# end salt.py


