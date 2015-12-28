# m3u8_encrypt.py, parse_video/lib/e/letv/o/
# KLetvPlayer package M3U8Encryption, this is a reference version use flash.ByteArray

from ....b import flash
ByteArray = flash.ByteArray

# M3U8Encryption.decodeB2T()
def decode(raw):
    # public function decodeB2T(param1:ByteArray) : String
    b = ByteArray()
    b.from_bytearray(bytearray(raw))
    if b.length < 1:
        return ''
    a = ByteArray()
    b.position = 0
    b.readBytes(a, 0, 5)
    version = a.readUTFBytes(a.length)
    if version.lower() == 'vc_01':
        return decodeBytesV1(b)
    return decodeBytes(b)

# private function decodeBytes(param1:ByteArray) : String
def decodeBytes(raw):
    raw.position = 0
    out = raw.readUTFBytes(raw.length);
    return out

# private function decodeBytesV1(param1:ByteArray) : String
def decodeBytesV1(raw):
    data = ByteArray()
    raw.position = 5
    raw.readBytes(data)
    
    first = ByteArray()
    # NOTE fix first size to speed up process data
    first.length = 2 * data.length
    
    for i in range(data.length):
        first[2 * i] = data[i] >> 4
        first[2 * i + 1] = data[i] & 15
    second = ByteArray()
    first.position = first.length - 11
    first.readBytes(second)
    first.position = 0
    first.readBytes(second, 11, first.length - 11)
    
    before = ByteArray()
    # NOTE fix before length here
    before.length = data.length
    for i in range(data.length):
        before[i] = (second[2 * i] << 4) + second[2 * i + 1]
    before.position = 0
    out = before.readUTFBytes(before.length)
    return out

# end m3u8_encrypt.py


