# _key.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509232013

import uuid
import hashlib

def gen_uuid():
    return uuid.uuid4().hex

def md5_hash(raw_text=''):
    return hashlib.md5(bytes(string, 'utf-8')).hexdigest()

# end _key.py


