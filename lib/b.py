# b.py, parse_video/lib/

import hashlib

# md5_hash
def md5_hash(raw):
    return hashlib.md5(bytes(raw, 'utf-8')).hexdigest()

# end b.py


