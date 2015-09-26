# e_list.py, parse_video/lib/e :: extractor list
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509262022

import importlib

from .. import err

def import_extractor(extractor_id):
    try:
        ex = importlib.import_module('..' + extractor_id, __name__)
        return ex
    except Exception as e:
        raise err.ConfigError('can not import extractor \"' + extractor_id + '\" ') from e

# TODO

# end e_list.py


