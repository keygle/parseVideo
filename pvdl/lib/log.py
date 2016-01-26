# log.py, parse_video/pvdl/lib/

# TODO debug log in functions (package) support
# TODO turn off DEBUG log support

import sys

from . import b, conf
from . import lan


# base print functions
def _p(t, file=None, end='\n', add_check_log_prefix=False, fix_check_log_file=False, *k, **kk):
    # NOTE default output file is sys.stderr
    if file == None:
        file = sys.stderr
    if not fix_check_log_file:	# NOTE fix logs not print to screen
        print(t, file=file, end=end, *k, **kk)
    # NOTE support print to check_log file; NOTE not remove color chars (ANSI ESC)
    if conf.check_log_file != None:
        t += end	# fix line end here
        if add_check_log_prefix:
            t = _gen_check_log_prefix() + t
        blob = t.encode('utf-8')	# NOTE just write utf-8 blob data, not raw text
        conf.check_log_file.write(blob)
    # end base print

def _gen_check_log_prefix(prefix='pvdl.check_log'):
    out = '[' + prefix + '] ' + b.print_iso_time() + '::'
    return out


# prefix print function
def _pp(raw, prefix='', color=b.color_reset(), *k, **kk):
    t = b.color_grey() + conf.PVDL_LOG_PREFIX + color + prefix + raw + b.color_reset()
    _p(t, *k, **kk)

# exports log functions

def p(t, *k, **kk):	# just print, no prefix
    _p(t, *k, **kk)

def e(t, color=b.color_light_red(), *k, **kk):	# ERROR
    _pp(t, prefix=lan.log_err(), color=color, *k, **kk)

def w(t, color=b.color_orange(), *k, **kk):	# WARNING
    _pp(t, prefix=lan.log_warn(), color=color, *k, **kk)

def i(t, color=b.color_yellow(), *k, **kk):	# INFO
    _pp(color + t, prefix=lan.log_info(), color=b.color_grey(), *k, **kk)

def o(t, color=b.color_light_blue(), *k, **kk):	# [ OK ]
    _pp(color + t, prefix=lan.log_ok(), color=b.color_blue(), *k, **kk)

def d(t, color=b.color_grey(), *k, **kk):	# DEBUG
    _pp(t, prefix=lan.log_debug(), color=color, *k, **kk)

def raw(t, *k, **kk):
    _pp(t, *k, **kk)
r = raw	# NOTE r() is the same as raw()

# end log.py


