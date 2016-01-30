# -*- coding: utf-8 -*-
# entry.py, parse_video/lib/e/bks1/, entry for extractor bks1
from .. import common
from .var import var

class Entry(common.ExtractorEntry):
    def _check_method(self, method):
        if method == 'pc_flash_gate':
            from . import method_pc_flash_gate as method_worker
        elif method == 'cdn_only_key':
            from . import method_cdn_only_key as method_worker
        else:	# no such method
            return None
        return method_worker
# entry exports
entry = Entry(var)
init, parse = entry.init, entry.parse
# end entry.py


