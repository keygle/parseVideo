# NOTE this code is from <https://github.com/lvqier/crawlers> 

import base64
import random
import time

from .encrypt import pack, rand, oi_symmetry_encrypt2

KEY = [
    0xfa, 0x82, 0xde, 0xb5, 0x2d, 0x4b, 0xba, 0x31,
    0x39, 0x6,  0x33, 0xee, 0xfb, 0xbf, 0xf3, 0xb6
]

def packstr(data):
    l = len(data)
    t = []
    t.append((l&0xFF00) >> 8)
    t.append(l&0xFF)
    t.extend([ord(c) for c in data])
    return t

def strsum(data):
    s = 0
    for c in data:
        s = s*131 + c
    return 0x7fffffff & s

def echo_ckeyv3(vid, guid='', t=None, player_version='3.2.19.334', platform=10902, stdfrom='bcng'):
    data = []
    data.extend(pack([21507, 3168485562]))
    data.extend(pack([platform]))
    
    if not t:
        t = time.time()
    seconds = int(t)
    microseconds = int(1000000*(t - int(t)))
    data.extend(pack([microseconds, seconds]))
    data.extend(packstr(stdfrom))
    
    r = random.random()
    data.extend(packstr('%.16f' % r))
    data.extend(packstr(player_version))
    data.extend(packstr(vid))
    data.extend(packstr('2%s' % guid))
    data.extend(packstr('4null'))
    data.extend(packstr('4null'))
    data.extend([0x00, 0x00, 0x00, 0x01])
    data.extend([0x00, 0x00, 0x00, 0x00])
    
    l = len(data)
    data.insert(0, l&0xFF)
    data.insert(0, (l&0xFF00) >> 8)
    
    enc = oi_symmetry_encrypt2(data, KEY)
    
    pad = [0x00, 0x00, 0x00, 0x00, 0xff&rand(), 0xff&rand(), 0xff&rand(), 0xff&rand()]
    pad[0] = pad[4] ^ 71 & 0xFF
    pad[1] = pad[5] ^ -121 & 0xFF
    pad[2] = pad[6] ^ -84 & 0xFF
    pad[3] = pad[7] ^ -86 & 0xFF
    
    pad.extend(enc)
    pad.extend(pack([strsum(data)]))
    
    result = base64.b64encode(bytes(pad), b'_-').decode('utf-8').replace('=', '')
    return result

# end echo_ckeyv3.py


