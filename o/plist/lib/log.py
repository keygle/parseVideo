# log.py, parse_video/o/plist/lib/

import sys
import functools

from . import b, conf

# base print function
def _p(t, file=sys.stderr, end='\n', *k, **kk):
    print(t, file=sys.stderr, end=end, *k, **kk)

# prefix print function
def _pp(raw, prefix='', *k, **kk):
    t = conf.PLIST_LOG_PREFIX + prefix + raw
    _p(t, *k, **kk)

## exports log functions

# just print, no prefix
p = functools.partial(_p)

def _export_log(prefix=''):
    return functools.partial(_pp, prefix=prefix)
# ERROR
e = _export_log('ERROR: ')
# WARNING
w = _export_log('WARNING: ')
# INFO
i = _export_log('INFO: ')
# OK
o = _export_log('[ OK ] ')
# RAW
raw = _export_log()
r = raw

_d = _export_log('DEBUG: ')
# DEBUG, NOTE check flag_debug
def d(*k, **kk):
    if conf.flag_debug:
        _d(*k, **kk)

# end log.py


