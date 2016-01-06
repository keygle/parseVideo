# NOTE this code is from <https://github.com/lvqier/crawlers> 

import struct

DELTA = 0x9e3779b9
ROUNDS = 16

SALT_LEN = 2
ZERO_LEN = 7

SEED = 0xdead

def rand():
    global SEED
    if SEED == 0:
        SEED = 123459876
    k1 = 0xffffffff & (-2836 * (SEED // 127773))
    k2 = 0xffffffff & (16807 * (SEED % 127773))
    SEED = 0xffffffff & (k1 + k2)
    if SEED < 0:
        SEED = SEED + 2147483647
    return SEED

def pack(data):
    target = []
    for i in data:
        target.extend(struct.pack('>I', i))
    return target

def unpack(data):
    data = bytes(data)
    target = []
    for i in range(0, len(data), 4):
        target.extend(struct.unpack('>I', data[i:i+4]))
    return target

def tea_encrypt(v, key):
    s = 0
    key = unpack(key)
    v = unpack(v)
    for i in range(ROUNDS):
        s += DELTA
        s &= 0xffffffff
        v[0] += (v[1]+s) ^ ((v[1]>>5)+key[1]) ^ ((v[1]<<4)+key[0])
        v[0] &= 0xffffffff
        v[1] += (v[0]+s) ^ ((v[0]>>5)+key[3]) ^ ((v[0]<<4)+key[2])
        v[1] &= 0xffffffff
    return pack(v)

def oi_symmetry_encrypt2(raw_data, key):
    pad_salt_body_zero_len = 1 + SALT_LEN + len(raw_data) + ZERO_LEN
    pad_len = pad_salt_body_zero_len % 8
    if pad_len:
        pad_len = 8 - pad_len
    data = []
    data.append(rand() & 0xf8 | pad_len)
    while pad_len + SALT_LEN:
        data.append(rand() & 0xff)
        pad_len = pad_len - 1
    data.extend(raw_data)
    data.extend([0x00] * ZERO_LEN)
    
    temp = [0x00] * 8
    enc = tea_encrypt(data[:8], key)
    for i in range(8, len(data), 8):
        d1 = data[i:]
        for j in range(8):
            d1[j] = d1[j] ^ enc[i-8+j]
        d1 = tea_encrypt(d1, key)
        for j in range(8):
            d1[j] = d1[j] ^ data[i-8+j] ^ temp[j]
            enc.append(d1[j])
            temp[j] = enc[i-8+j]
    return enc

# end encrypt.py

