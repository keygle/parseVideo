# _key.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.1 test201509232017

import uuid
import hashlib

def gen_uuid():
    return uuid.uuid4().hex

def md5_hash(raw_text=''):
    return hashlib.md5(bytes(raw_text, 'utf-8')).hexdigest()

# end _key.py


