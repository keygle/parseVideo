#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# sandwich_bin.py, parse_video/lib/bridge/sandwich_bridge/
#
# up_side bin file
#

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from sandwich_host import side_up

# start from main
def start():
    side_up.main(sys.argv[1:])
if __name__ == '__main__':
    start()
# end sandwich_bin.py


