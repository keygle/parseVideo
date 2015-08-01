# -*- coding: utf-8 -*-
# make_final_url.py, part for parse_video : a fork from parseVideo. 
# lib/letv/o/tscn2: make letv final url, use the method from flvsp
# last_update 2015-07-15 16:15 GMT+0800 CST

# import
import random

# function

# main url text make function, raw: raw url text
def make(raw):
    
    out = ''	# final url text
    
    # separate url before ?
    before, rest = raw.split('?', 1)
    
    # NOTE can not just replace platid splatid here, its in letv key
    # url args value replace list
    replace_list = {
        # 'splatid' : '503', 
        'platid' : '5', 
        'tss' : 'no', 
    }
    
    # split rest with '&'
    rests = rest.split('&')
    # process each args
    for r in rests:
        # split with '='
        name, value = r.split('=', 1)
        # replace some value
        if name in replace_list:
            value = replace_list[name]
        # add to final url
        out += '&' + name + '=' + value
    # remove first '&'
    out = out[1:]
    # add more args
    out += '&retry=1&tag=letv&sign=letv&tn='
    # add a random number
    out += str(random.random())		# &tn=0.9844
    # add more args
    out += '&termid=1&pay=0&ostype=Windows7&hwtype=un&ctv=pc&m3v=1'
    
    # add before part
    out = before + '?' + out
    # done
    return out

# end make_final_url.py


