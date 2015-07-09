# -*- coding: utf-8 -*-
# config.py, part for parse_video : a fork from parseVideo. 
# config: bks1, evparse:lib/bks1/o/core/config.py

from .. import s1

CHECK_LIMIT_URL = 'http://cache.vip.' + s1.get_s1()[1] + '.com/ip/'
CHECK_V_INFO_URL = 'http://data.video.' + s1.get_s1()[1] + '.com/v.f4v'
VIP_AUTH_URL = 'http://api.vip.' + s1.get_s1()[0] + '.com/services/ck.action'
MIXER_VX_URL = 'http://cache.video.' + s1.get_s1()[1] + '.com/vms'
MIXER_VX_VIP_URL = 'http://cache.vip.' + s1.get_s1()[1] + '.com/vms'

FIRST_DISPATCH_URL = 'http://data.video.' + s1.get_s1()[1] + '.com/t'

# end config.py


