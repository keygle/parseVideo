# var.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509232029

# static data

# var data
_ = {}

# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    # set default values
    out['_flag_output_no_restruct'] = False	# for --output-no-restruct
    
    # for --min --max --min-i --max-i
    out['hd_min'] = None
    out['hd_max'] = None
    out['i_min'] = None
    out['i_max'] = None
    
    return out

def push():
    __old.append(_)

def pop():
    return __old.pop()

# end var.py


