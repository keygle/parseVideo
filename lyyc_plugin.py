#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# lyyc_plugin.py, parse_video/, support lyyc_plugin port_version 0.1.0

import json

try:
    from .lib import plugin
except Exception:
    from lib import plugin

# exports plugin functions
lyyc_about = plugin.lyyc_about
lyyc_import = plugin.lyyc_import
#lyyc_install = plugin.lyyc_install
#lyyc_config = plugin.lyyc_config
lyyc_parse = plugin.lyyc_parse

# DEBUG functions
def p(o):
    print(json.dumps(o, indent=4, sort_keys=True, ensure_ascii=False))

# end lyyc_plugin.py


