# -*- coding: utf-8 -*-
# debug2.py, for parse_video

import sys
import subprocess

pybin = sys.executable
arg = ['debug_pvtkgui2.bat', pybin]

p = subprocess.Popen(arg, shell=True)
p.communicate()

# end debug2.py


