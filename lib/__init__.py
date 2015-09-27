# -*- coding: utf-8 -*-
# __init__.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.4.0 test201509272013
#
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.09. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext 
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

'''
parse_video lib main entry
'''

_flag_not_imported = True
if _flag_not_imported:
    _flag_not_imported = False
    from . import var, b, e
    from . import parse as _parse

def _load_config():
    conf = b.load_conf_file(var.CONF_FILE)
    # set config items
    var._['user_agent'] = conf['user_agent']
    var._['url_to_e_filter'] = conf['filter_re']
    var._['default_method'] = conf['default_method']

# exports functions

def parse(raw_url, raw_extractor='', raw_method=''):
    # NOTE load config first
    _load_config()
    # NOTE just call _parse function now
    return _parse.parse(raw_url=raw_url, raw_extractor=raw_extractor, raw_method=raw_method)

def get_extractor_info():
    id_list = e.get_list()
    out = []
    for i in id_list:
        one = e.get_about_info(i)
        out.append(one)
    return out

# end __init__.py


