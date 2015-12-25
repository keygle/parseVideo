# bridge.py, parse_video/lib/e/bks1/

import random

from ...bridge import wuyan_bridge

def gen_tm():
    return random.randint(1000, 3000)

# package Zombie.bite()
def bite(tvid, tm=None):	# TODO
    if tm == None:
        tm = gen_tm()
    
    enc, tm = wuyan_bridge.bks1_bite(tvid, tm)
    return enc, tm

# end bridge.py


