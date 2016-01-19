# b.py, parse_video/pvdl/lib/

from . import conf

def replace_filename_bad_char(raw, replace='-'):
    bad_chars = conf.FILENAME_BAD_CHAR
    out = ('').join([i if not i in bad_chars else replace for i in raw])
    return out


def num_len(n, l=2):
    out = (str(n)).zfill(l)
    return out

# TODO

def md5sum():
    pass

# TODO
# end b.py


