# support_evparse.py, part for parse_video : a fork from parseVideo. 
# support_evparse: o/pvtkgui/support_evparse: parse_video Tk GUI, use evparse to analyse. 
# version 0.0.1.0 test201506112208
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.06. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# import
import os
import re

# global vars

BIN_EVPARSE = './o/evparse/evp'

EVP_SUPPORT_RE = [
    # support sohu
    # http://tv.sohu.com/20150215/n409034362.shtml
    '^http://tv\.sohu\.com/(19|20)[0-9]{6}/n[0-9]+\.shtml', 
    
    # support hunantv
    # http://www.hunantv.com/v/2/150668/f/1518250.html#
    # http://www.hunantv.com/v/2/51717/f/692063.html#
    # http://www.hunantv.com/v/2/107768/f/1517224.html#
    # http://www.hunantv.com/v/2/150121/c/1502027.html#
    '^http://www\.hunantv\.com/v/2/[0-9]+/[a-z]/[0-9]+\.html', 
    
    # support pptv
    # http://v.pptv.com/show/PfQMiaicNZyQdq6FA.html
    # http://v.pptv.com/show/9Vs1sxuB8SibSEHg.html?rcc_src=L1
    '^http://v\.pptv\.com/show/[A-Za-z0-9]+\.html', 
]

# functions

# check if support evp
def check_support_evp(url_to):
    # check if evp installed
    evp_bin = BIN_EVPARSE
    if not os.path.isfile(evp_bin):
        # evp not installed, not support
        return False
    # check re match
    for r in EVP_SUPPORT_RE:
        if re.match(r, url_to):
            # yes, support
            return True
    # check done, not support
    return False

def get_evp_arg(url_to, hd=None, flag_debug=False):
    # make evp args
    arg = [BIN_EVPARSE, '--fix-unicode']
    # check hd
    if hd != None:
        arg += ['--min', str(hd), '--max', str(hd)]
    # check debug
    if flag_debug:
        arg += ['--debug']
    # add url
    arg += [url_to]
    # done
    return arg

# end support_evparse.py


