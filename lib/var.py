# var.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509232021

# static data

# var data
_ = {}

# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    return out

def push():
    __old.append(_)

def pop():
    return __old.pop()

# end var.py


