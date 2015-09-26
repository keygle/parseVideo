# __init__.py, parse_video/lib/e/bks1/o
# version 0.0.2.0 test201509261443

import random

from .first_url import make as make_first_url
from .key import getVrsEncodeCode, getDispatchKey

def gen_tm():
    '''
    gen a tm used in first_url
    '''
    # NOTE another method to gen tm is to use flash.getTimer()
    return random.randint(1000, 2000)

# end __init__.py


