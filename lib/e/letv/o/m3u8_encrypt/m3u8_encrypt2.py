# m3u8_encrypt2.py, parse_video/lib/e/letv/o/
# KLetvPlayer package M3U8Encryption, this is a fast version not use flash.ByteArray, just use python3 bytearray

# M3U8Encryption.decodeB2T()
def decode(raw):
    # public function decodeB2T(param1:ByteArray) : String
    b = bytearray(raw)
    if len(b) < 1:
        return ''
    a = b[0:5]
    version = a.decode('utf-8')
    if version.lower() == 'vc_01':
        return decodeBytesV1(b)
    return decodeBytes(b)

# private function decodeBytes(param1:ByteArray) : String
def decodeBytes(raw):
    out = raw.decode('utf-8')
    return out

# private function decodeBytesV1(param1:ByteArray) : String
def decodeBytesV1(raw):
    data = raw[5:]
    first = bytearray(len(data) * 2)
    for i in range(len(data)):
        first[2 * i] = data[i] >> 4
        first[2 * i + 1] = data[i] & 15
    second = first[-11:]
    second += first[:-11]
    
    before = bytearray(len(data))
    for i in range(len(data)):
        before[i] = (second[2 * i] << 4) + second[2 * i + 1]
    out = before.decode('utf-8')
    return out

# end m3u8_encrypt2.py


