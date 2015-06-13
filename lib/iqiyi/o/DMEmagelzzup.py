# -*- coding: utf-8 -*-
# DMEmagelzzup.py, part for evparse : EisF Video Parse, evdh Video Parse. 
# DMEmagelzzup: iqiyi, DMEmagelzzup 

# import

from .key import md5_hash

# function

# var msg:Function = function():String
def msg(name_10, name_11):
    # NOTE on <https://github.com/soimort/you-get/issues/542>
    # jackyzy823 said that the msg() function is just a md5 hash function
    pass

# NOTE this mix function, is copied from <https://github.com/jackyzy823/you-get/blob/iqiyi-new-alogrithm/src/you_get/extractors/iqiyi.py>
# at 2015-06-13 12:56 GMT+0800 CST
def mix0(tvid, tm):
    enc = []
    arr =  [ -0.625, -0.5546875, -0.59375, -0.625, -0.234375, -0.203125, -0.609375, -0.2421875, -0.234375, -0.2109375, -0.625, -0.2265625, -0.625, -0.234375, -0.6171875, -0.234375, -0.5546875, -0.5625, -0.625, -0.59375, -0.2421875, -0.234375, -0.203125, -0.234375, -0.21875, -0.6171875, -0.6015625, -0.6015625, -0.2109375, -0.5703125, -0.2109375, -0.203125 ] [::-1]
    for i in arr:
        enc.append(chr(int(i *(1<<7)+(1<<7))))
    
    src = 'hsalf'
    enc.append(str(tm))
    enc.append(tvid)
    
    enc_text = ('').join(enc)
    sc = md5_hash(enc_text)
    
    return tm, sc, src

# class

class DMEmagelzzup(object):
    
    # function mix(param1:String) : Object
    def mix(param1, tm):    # tm, getTimer() value
        
        # NOTE just use mix() function from jackyzy823/you-get
        tm, sc, src = mix0(param1, tm)
        
        # done
        var_67 = {}
        
        var_67['src'] = 'hsalf'
        var_67['tm'] = tm
        var_67['sc'] = sc
        
        return var_67
    
    # end class DMEmagelzzup

# end DMEmagelzzup.py


