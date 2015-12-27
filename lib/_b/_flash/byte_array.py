# byte_array.py, parse_video/lib/_b/_flash/
# support ByteArray API as action script 3 in flash

import struct

# main ByteArray class implementation
class ByteArray(object):
    # ignored properties
    #defaultObjectEncoding
    #objectEncoding
    #shareable
    # ignored public methods
    #atomicCompareAndSwapIntAt()
    #atomicCompareAndSwapLength()
    #readObject()
    #toJSON()
    #toString()
    #writeObject()
    
    # Endian
    BIG_ENDIAN = '>'
    LITTLE_ENDIAN = '<'
    
    def __init__(self):
        # NOTE default endian should be BIG_ENDIAN
        self._endian = ByteArray.BIG_ENDIAN
        # NOTE length is underly bytearray's length
        self._data = None	# underly bytearray
        self._pos = 0	# position
        # clear when init
        self.clear()
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, i):
        return self._data[i]
    def __setitem__(self, i, value):
        # check length and extend bytearray
        if len(self._data) < (i + 1):
            self._resize(i + 1)
        self._data[i] = value
    
    # base functions
    def _resize(self, new_size):
        '''
        check and set underly bytearray's length to new_size (in Byte)
        '''
        if len(self._data) < new_size:	# extend data
            old = self._data
            self._data = bytearray(new_size)
            self._data[0:len(old)] = old
        elif len(self._data) > new_size:	# truncat data
            old = self._data
            self._data = old[0:new_size]
    
    def _read_bytes(self, size=0):
        '''
        read some raw bytes from current position, and increase position after read
        '''
        size_ = int(size)
        if size_ < 0:
            raise ValueError('can not read bytes size', size)
        size = size_
        # check rest data
        if self.bytesAvailable < size:
            raise ValueError('no enough data to read, bytes size', size)
        # read data to bytes and update pos
        out = bytes(self._data[self._pos:self._pos + size])
        self._pos += size
        return out
    
    def _write_bytes(self, data):
        '''
        write some raw bytes from current position, and increase position after write
        '''
        # check space enough
        if len(data) > self.bytesAvailable:
            self._resize(self._pos + len(data))	# extend bytearray before write
        # write data and update pos
        self._data[self._pos:self._pos + len(data)] = data
        self._pos += len(data)
    
    # base convert functions
    def _pack(self, mode, raw):
        return struct.pack(self._endian + mode, raw)
    def _unpack(self, mode, raw):
        return struct.unpack(self._endian + mode, raw)
    
    # additional functions for python 3
    def to_bytearray(self):
        return self._data.copy()
    def from_bytearray(self, data):
        if not isinstance(data, bytearray):
            raise TypeError('only accept bytearray', data)
        self._data = data.copy()
    
    # public properties
    
    # [read-only] -> uint
    @property
    def bytesAvailable(self):
        out = max(0, len(self._data) - self._pos)
        return out
    
    # -> str
    @property
    def endian(self):
        return self._endian
    @endian.setter
    def endian(self, value):
        if value in [ByteArray.LITTLE_ENDIAN, ByteArray.BIG_ENDIAN]:
            self._endian = value
        else:
            raise ValueError('no such endian', value)
    
    # -> uint
    @property
    def length(self):
        return len(self._data)
    @length.setter
    def length(self, value):
        value_ = int(value)
        if value_ < 0:
            raise ValueError('can not set length to', value)
        self._resize(value_)	# resize data
    
    # -> uint
    @property
    def position(self):
        return self._pos
    @position.setter
    def position(self, value):
        value_ = int(value)
        if value_ < 0:
            raise ValueError('can not set position to', value)
        self._pos = value_
    
    # public methods
    
    def clear(self):
        self._data = bytearray(0)
        self._pos = 0
    
    ## complex read and write functions
    
    # out :ByteArray, offset :uint, length :uint
    def readBytes(self, out, offset=0, length=0):
        if not isinstance(out, ByteArray):
            raise TypeError('pos 1 argument should be ByteArray', out)
        if length < 0:
            raise ValueError('can not read length', length)
        # read data
        if (length == 0) and (self.bytesAvailable > 0):
            length = self.bytesAvailable	# NOTE length == 0 will read all data
        data = self._read_bytes(length)
        # write bytes to the ByteArray
        old = out.position	# NOTE save and restore old position
        out.position = offset
        out._write_bytes(data)
        out.position = old
    # bytes :ByteArray, offset :uint, length :uint
    def writeBytes(self, raw, offset=0, length=0):
        if not isinstance(raw, ByteArray):
            raise TypeError
        if length < 0:
            raise ValueError('can not write length', length)
        old = raw.position
        raw.position = offset
        if (length == 0) and (raw.bytesAvailable > 0):
            length = raw.bytesAvaliable
        data = raw._read_bytes(length)
        raw.position = old
        # write bytes to self
        self._write_bytes(data)
        # TODO out of range process
    
    # length :uint -> str
    def readUTFBytes(self, length):
        blob = self._read_bytes(length)
        text = blob.decode('utf-8')
        return text
    # value :str
    def writeUTFBytes(self, value):
        blob = value.encode('utf-8')
        self._write_bytes(blob)
    
    # -> str
    def readUTF(self):
        pass
    # value :str
    def writeUTF(self, value):
        pass
    
    # length :uint, charSet :str -> str
    def readMultiByte(self, length, charset):
        blob = self._read_bytes(length)
        # decode blob to text
        text = blob.decode(charset)
        return text
    # value :str, charset :str
    def writeMultiByte(self, value, charset):
        # encode text to binary
        blob = value.encode(charset)
        self._write_bytes(blob)
    
    ## compress
    
    # algorithm :str
    def uncompress(self, algorithm):
        pass
    # algorithm :str
    def compress(self, algorithm):
        pass
    
    def deflate(self):
        pass
    def inflate(self):
        pass
    
    ## read simple value
    def _read_value(self, mode, size):
        raw = self._read_bytes(size)
        out = self._unpack(mode, raw)
        return out
    
    # -> bool
    def readBoolean(self):
        return self._read_value('?', 1)
    
    # -> int
    def readByte(self):
        return self._read_value('b', 1)
    # -> uint
    def readUnsignedByte(self):
        return self._read_value('B', 1)
    
    # -> int
    def readShort(self):
        return self._read_value('h', 2)
    # -> uint
    def readUnsignedShort(self):
        return self._read_value('H', 2)
    
    # -> int
    def readInt(self):
        return self._read_value('i', 4)
    # -> uint
    def readUnsignedInt(self):
        return self._read_value('I', 4)
    
    # -> float
    def readFloat(self):
        return self._read_value('f', 4)
    # -> float
    def readDouble(self):
        return self._read_value('d', 8)
    
    ## write simple value
    def _write_value(self, mode, raw):
        data = self._pack(mode, raw)
        self._write_bytes(data)
    
    # value :bool
    def writeBoolean(self, value):
        self._write_value('?', value)
    
    # value :int
    def writeByte(self, value):
        self._write_value('b', value)
    # value :int
    def writeUnsignedByte(self, value):
        self._write_value('B', value)
    
    # value :int
    def writeShort(self, value):
        self._write_value('h', value)
    # value :uint
    def writeUnsignedShort(self, value):
        self._write_value('H', value)
    
    # value :int
    def writeInt(self, value):
        self._write_value('i', value)
    # value :uint
    def writeUnsignedInt(self, value):
        self._write_value('I', value)
    
    # value :float
    def writeFloat(self, value):
        self._write_value('f', value)
    # value :float
    def writeDouble(self, value):
        self._write_value('d', value)
    # end ByteArray class

# end byte_array.py


