# log.py, parse_video/pvdl/lib/

# TODO color output support
# TODO debug log in functions (package) support
# TODO turn off DEBUG log support

import sys

from colored import fg, bg, attr

from . import conf

# TODO

# base print functions
def _p(t, file=sys.stderr, *k, **kk):
    print(t, file=file, *k, **kk)

# prefix print function
def _pp(raw, prefix='', *k, **kk):
    t = conf.PVDL_LOG_PREFIX + prefix + raw
    _p(t, *k, **kk)

# exports log functions

def p(t, *k, **kk):	# just print, no prefix
    _p(t, *k, **kk)

# TODO color output support
def e(t, *k, **kk):	# ERROR
    _pp(t, prefix='ERROR: ', *k, **kk)
def w(t, *k, **kk):	# WARNING
    _pp(t, prefix='WARNING: ', *k, **kk)
def i(t, *k, **kk):	# INFO
    _pp(t, prefix='INFO: ', *k, **kk)
def o(t, *k, **kk):	# [ OK ]
    _pp(t, prefix='[ OK ] ', *k, **kk)
def d(t, *k, **kk):	# DEBUG
    _pp(t, prefix='DEBUG: ', *k, **kk)

def raw(t, *k, **kk):
    _pp(t, *k, **kk)
r = raw	# NOTE r() is the same as raw()

# end log.py


