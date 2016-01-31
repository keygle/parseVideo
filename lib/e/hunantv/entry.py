# -*- coding: utf-8 -*-
# entry.py, parse_video/lib/e/hunantv/, entry for extractor hunantv
from .. import common
from .var import var

class Entry(common.ExtractorEntry):
    def _check_method(self, method):
        if method == 'pc_flash_gate':
            from . import method_pc_flash_gate as method_worker
        elif method == 'flvsp':
            from . import method_flvsp as method_worker
        else:
            return None
        return method_worker
# entry exports
entry = Entry(var)
init, parse = entry.init, entry.parse
# end entry.py


