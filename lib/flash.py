# -*- coding: utf-8 -*-
# flash.py, part for parse_video : a fork from parseVideo. 
# flash: support some flash functions (action script 3) in python3. 
# version 0.0.5.0 test201505061452
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.05. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# import

import time
import base64

# global vars
_GET_TIMER_START_MS = 0

# functions

def _get_ms():
    return int(round(time.time() * 1e3))

def getTimer(start=0):
    global _GET_TIMER_START_MS
    _GET_TIMER_START_MS -= start
    now_ms = _get_ms()
    return (now_ms - _GET_TIMER_START_MS)

# convert data to uint format
def uint(num):
    n = int(num)	# int is of 4 bytes
    b = None
    out = None
    try:	# fix for overflow, may not be right
        b = n.to_bytes(4, 'little', signed=True)
    except OverflowError as err:
        try:
            b = n.to_bytes(8, 'little', signed=True)
        except OverflowError as err2:
            # print('DEBUG: flash.uint() 8 Bytes failed')
            try:
                b = n.to_bytes(16, 'little', signed=True)
            except OverflowError as err3:
                print('DEBUG: flash.uint() 16 Bytes failed')
                try:
                    b = n.to_bytes(32, 'little', signed=True)
                except OverflowError as err4:
                    print('DEBUG: flash.uint() 32 Bytes failed')
                    try:
                        b = n.to_bytes(64, 'little', signed=True)
                    except OverflowError as err5:
                        print('DEBUG: flash.uint() 64 Bytes failed')
                        b = n.to_bytes(128, 'little', signed=True)
    finally:
        out = int.from_bytes(b[:4], 'little', signed=False)
    return out

# class

class ByteArray(object):
    
    def __init__(self):
        self._data = bytearray()
        self.position = 0
    
    def __len__(self):
        return len(self._data)
    
    def __str__(self):
        return str(self._data)
    
    def __repr__(self):
        return repr(self._data)
    
    def __getitem__(self, n):
        b = self._data[n:n + 1]
        # make byte
        return int.from_bytes(b, 'little', signed=True)
    
    @property
    def bytesAvailable(self):
        return (len(self._data) - self.position)
    
    def writeUTFBytes(self, string):
        # create bytearray
        b = bytearray(string, 'utf-8')
        # just set and update data
        i = self.position
        self._data[i : i + len(b)] = b
        # increase position
        self.position += len(b)
    
    def writeByte(self, num):
        # make byte
        n = int(num)
        b = n.to_bytes(4, 'little')[:1]
        # set it
        i = self.position
        self._data[i: i + 1] = b
        self.position += 1
    
    def readByte(self):
        # get byte
        i = self.position
        b = self._data[i:i + 1]
        self.position += 1
        # make byte
        return int.from_bytes(b, 'little', signed=True)
    
    def clear(self):
        self._data = bytearray()
        self.position = 0
    
    # NOTE add by me, not a method of flash ByteArray
    def encode_base64(self):
        return base64.b64encode(self._data)
    # end ByteArray

class Array(object):
    
    def __init__(self):
        self._data = []
    
    def __len__(self):
        return len(self._data)
    
    def __str__(self):
        return str(self._data)
    
    def __repr__(self):
        return repr(self._data)
    
    def __getitem__(self, n):
        # check slice
        if isinstance(n, slice):
            return self._data[n.start:n.step:n.stop]
        # check len
        if n > len(self._data) - 1:
            return None
        return self._data[n]
    
    def __setitem__(self, n, item):
        # check max length
        if isinstance(n, slice):
            max_i = n.stop
        else:
            max_i = n + 1
        # check array length
        while len(self._data) < max_i:
            self._data.append(None)
        # check slice
        if isinstance(n, slice):
            self._data[n.start:n.step:n.stop] = item
        else:
            # set it
            self._data[n] = item
    
    def append(self, item):
        self._data.append(item)
    # end Array

# init

# init for getTimer()
_GET_TIMER_START_MS = _get_ms()

# end flash.py


