# -*- coding: utf-8 -*-
# TimeStamp.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# TimeStamp: letv/kletvplayer, com.letv.plugins.kernel.tools

# import
import time
import math

from ..keygen import AS3Lib

# import from out
getTimer = None
# NOTE should be set
def set_import(flash):
    global getTimer
    getTimer = flash.getTimer

# functions
def get_time():	# convert js (new Data()).getTime() to python3
    return int(math.floor(time.time() * 1e3))	# TODO this may be not stable

# class

class TimeStamp(object):
    
    def __init__(self):
        self._stime = 0	# server time
        self.nowTime = 0
        pass
    
    @property
    def stime(self):
        return self._stime
    
    @stime.setter
    def stime(self, value):
        # update self.nowTime
        self.nowTime = getTimer()
        # save server time
        self._stime = value
    
    @property
    def tm(self):
        if self.stime > 0:
            return self.stime + int((getTimer() - self.nowTime) * 0.001)
        return int(get_time() * 0.001)
    
    def calcTimeKey(self):
        return AS3Lib.calcTimeKey(self.tm)
    # end TimeStamp class

# end TimeStamp.py


