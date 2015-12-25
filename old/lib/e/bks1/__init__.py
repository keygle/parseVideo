# -*- coding: utf-8 -*-
# __init__.py, parse_video/lib/e/bks1
# LICENSE GNU GPLv3+ sceext 
# version 0.0.9.0 test201509271518
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
parse_video/lib/e/bks1
    standard port and main entry for extractor bks1
'''

_flag_not_imported = True
if _flag_not_imported:
    _flag_not_imported = False
    from ... import b, err
    from ... import var as var0
    from ...b import log
    
    from . import var, about, fx_key
    from . import enc, nosalt, o, vv
    from . import parse as _parse

# load this extractor's config file
def load_config():
    conf = b.load_conf_file(var.CONF_FILE)
    # set config items
    var._['pool_size_get_final_url'] = conf['pool_size_get_final_url']
    var._['cdn_server'] = conf['cdn_server']
    var._['chrome_bin'] = conf['chrome_bin']
    var._['node_bin'] = conf['node_bin']
    var._['enhp_bin'] = conf['enhp_bin']

# export functions
def get_about_info():
    return about.get_info()

def parse(raw_url):
    # load config file
    load_config()
    # check method and process method args
    raw_method = var._['raw_method']
    raw_parts = raw_method.split(';', 1)
    if len(raw_parts) < 2:
        raw_parts.append('')
    method_name, raw_args = raw_parts
    if method_name == 'pc_flash_gate':
        # DEBUG log here
        log.d('use method \"' + method_name + '\" ')
        # process args
        args = raw_args.split(',')
        for a in args:
            if a == '':
                pass	# just ignore this null arg
            elif a == 'set_flag_v':
                var._['flag_v'] = True
            elif a == 'force':
                var._['flag_v_force'] = True
            elif a == 'set_um':
                var._['flag_set_um'] = True
            elif a == 'set_vv':
                var._['flag_set_vv'] = True
            else:	# not support this arg
                log.w('not support this method arg \"' + a + '\" ')
        # use normal parse function
        raw_evinfo = _parse.normal_parse(raw_url)
    # TODO to support more method
    else:	# not support this method
        raise err.ConfigError('not support this method \"' + method_name + '\" ')
    # add more info to raw_evinfo
    evinfo = raw_evinfo
    evinfo['info']['extractor_name'] = var.EXTRACTOR_NAME
    evinfo['info']['site'] = var.SITE
    evinfo['info']['site_name'] = var.SITE_NAME
    # done
    return evinfo

# end __init__.py


