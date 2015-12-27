# gslb_item_data.py, parse_video/lib/e/letv/o/
# KLetvPlayer package com.letv.plugins.kernel.model.special.gslb.GslbItemData

import random

# KLetvPlayer package com.letv.plugins.kernel.model.special.FlashVars
P1 = '1'
P2 = '10'
P3 = '-'

# KLetvPlayer package com.letv.plugins.kernel.model.special.ConfigData
TAG = 'letv'

def gen_before_url(
        raw, 
        vid, 
        rateid, 
        p1 = P1, 
        p2 = P2, 
        p3 = P3, 
        tag = TAG, 
        type_from = 'letv', 
        ostype = 'Windows7'):
    # public function GslbItemData(param1:Object, param2:Vector.<String>)
    out = raw
    #out = out.replace('tss=no', 'tss=ios')
    out += '&ctv=pc' + '&m3v=1'
    if not 'termid=' in out:
        out += '&termid=1'
    out += '&format=1' + '&hwtype=un'
    out += '&ostype=' + ostype
    out += '&tag=' + tag
    out += '&sign=' + type_from
    out += '&expect=3'
    out += '&p1=' + p1 + '&p2=' + p2 + '&p3=' + p3
    out += '&vid=' + vid
    out += '&tn=' + str(random.random())
    # TODO may be need more args here
    # NOTE add rateid
    out += '&rateid=' + rateid
    return out

# end gslb_item_data.py


