# flash_bridge.py, parse_video/lib/bridge/
# NOTE handwich_bridge only works on Windows

from .. import err, b, conf
from ..b import log

from .handwich_bridge import handwich_host

# NOTE handwich_bridge support
def init_handwich_bridge(core, core_path):
    return handwich_host.init(core, core_path)

def handwich_call(core, f='about', a=[]):
    return handwich_host.call(core, f=f, a=a)

# end flash_bridge.py


