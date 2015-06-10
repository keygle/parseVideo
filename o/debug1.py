# -*- coding: utf-8 -*-
# debug1.py, for parse_video

import sys
import subprocess

pybin = sys.executable
arg = ['debug_pvtkgui.bat', pybin]

p = subprocess.Popen(arg, shell=True)
p.communicate()

# end debug1.py


