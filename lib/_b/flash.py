# flash.py, parse_video/lib/_b/

import struct

from ._flash.byte_array import ByteArray

# bit operations in ActionScript3

# uint(raw)
def uint(raw):
    b = struct.pack('<q', raw)  # TODO this may fail
    return struct.unpack('<I', b[:4])[0]
# raw << l
def l2(raw, l):
    return uint(raw << l)
# raw >>> l
def r3(raw, l):
    return uint(raw) >> l

# end flash.py


