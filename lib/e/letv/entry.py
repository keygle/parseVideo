# -*- coding: utf-8 -*-
# entry.py, parse_video/lib/e/letv/, entry for extractor letv
from ... import err
from ...b import log
from .. import common, log_text

from . import var
from . import method_pc_flash_gate

class Entry(common.ExtractorEntry):
    def _do_parse(self, raw_method):
        method, method_arg_text = common.entry_split_method(raw_method)
        # check method name
        if method == 'pc_flash_gate':
            log.d(log_text.entry_log_use_method(method, method_arg_text))	# DEBUG log
            pvinfo = method_pc_flash_gate.parse(method_arg_text)
        else:
            raise err.ConfigError(log_text.entry_err_no_method(method))
        return common.entry_add_more_info(pvinfo, var)
# entry exports
entry = Entry(var)
init, parse = entry.init, entry.parse
# end entry.py


