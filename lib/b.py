# b.py, parse_video/lib/

import hashlib

from ._b import log

from ._b.network import (
    dl_blob, 
    dl_html, 
    dl_json, 
    dl_xml, 
    post, 
    post_form, 
)

# md5_hash
def md5_hash(raw):
    return hashlib.md5(bytes(raw, 'utf-8')).hexdigest()

# use many threads to do many tasks at the same time
def map_do(task_list, worker=lambda x:x, pool_size=1):
    pass	# TODO

# end b.py


