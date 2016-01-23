# log.py, parse_video/pvdl/lib/

# TODO debug log in functions (package) support
# TODO turn off DEBUG log support

import sys
from colored import fg, bg, attr

from . import conf


# base print functions
def _p(t, file=sys.stderr, *k, **kk):
    print(t, file=file, *k, **kk)
    # NOTE support print to check_log file; NOTE not remove color chars (ANSI ESC)
    if conf.check_log_file != None:
        blob = t.encode('utf-8')	# NOTE just write utf-8 blob data, not raw text
        conf.check_log_file.write(blob)
    # end base print

# prefix print function
def _pp(raw, prefix='', color=attr('reset'), *k, **kk):
    t = fg('grey_50') + conf.PVDL_LOG_PREFIX + color + prefix + raw + attr('reset')
    _p(t, *k, **kk)

# exports log functions

def p(t, *k, **kk):	# just print, no prefix
    _p(t, *k, **kk)

def e(t, color=fg('light_red'), *k, **kk):	# ERROR
    _pp(t, prefix='ERROR: ', color=color, *k, **kk)

def w(t, color=fg('orange_1'), *k, **kk):	# WARNING
    _pp(t, prefix='WARNING: ', color=color, *k, **kk)

def i(t, color=fg('yellow'), *k, **kk):	# INFO
    _pp(color + t, prefix='INFO: ', color=fg('grey_50'), *k, **kk)

def o(t, color=fg('light_blue'), *k, **kk):	# [ OK ]
    _pp(color + t, prefix='[ OK ] ', color=fg('blue'), *k, **kk)

def d(t, color=fg('grey_50'), *k, **kk):	# DEBUG
    _pp(t, prefix='DEBUG: ', color=color, *k, **kk)

def raw(t, *k, **kk):
    _pp(t, *k, **kk)
r = raw	# NOTE r() is the same as raw()

# end log.py


