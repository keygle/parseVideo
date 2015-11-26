# node_port.py, parse_video/lib/e/bks1/enc
# version 0.0.1.0 test201509242340

# TODO support call node to run .js file to gen enc

from .... import b
from .. import var

def gen_enc(tvid, tm):
    '''
    generate the enc key to used in first_url
    return enc
    '''
    # load config file
    conf = b.load_conf_file(var.CONF_FILE)
    salt = conf['salt']
    # gen enc key
    enc = salt + str(tm) + tvid
    sc = b.md5_hash(enc)
    return sc

# end node_port.py


