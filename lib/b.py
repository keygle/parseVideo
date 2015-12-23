# b.py, parse_video/lib/

import hashlib

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

# end b.py


