# -*- coding: utf-8 -*-
# parser.py, part for parse_video
# parser: extractors entry module. 
# author sceext <sceext@foxmail.com> 2015.04 
# copyright 2015 sceext 
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : parse videos from many websites. 
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

# import modules

# python3 modules
import re

# parse_video modules

# global vars

# supported urls to module
list_url_to = {
	'^http://www\.iqiyi\.com/v_.+\.html$': 'iqiyi', 
}

# supported urls
# iqiyi		"http://www.iqiyi.com/v_19rro2bcbs.html"

# classes

# functions

# check support
def check_url_support(url):
    for p, m in list_url_to:
        # check match url
        ma = re.match(p, url)
        if ma:	# match this url
            # import this module
            import_str = 'from .extractors import ' + m + ' as extractor'
            # return it
            return extractor	# done
    # not supported url
    return None

# entry function
def entry(url):
    
    # check supported url
    extractor = check_url_support(url)
    if extractor:
        # just parse it
        return extractor.parse(url)
    else:
        # not supported url
        print('ERROR: not supported this url "' + url + '" ! ')


# end parser.py


