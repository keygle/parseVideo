# var.py, parse_video/lib/e/bks1
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509240030

# static data

# var data
_ = {}

# save old var data for push() and pop()
__old = []

# var functions
def init():
    out = {}
    # set default values
    out['raw_arg'] = ''		# this is used to pass raw_arg to extractor
    out['raw_method'] = ''	# this is used to pass raw_method to extractor
    
    return out

def push():
    __old.append(_)

def pop():
    return __old.pop()

# end var.py


