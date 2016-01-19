# -*- coding: utf-8 -*-
# entry.py, parse_video/pvdl/lib/
#
#    pvdl : A reference implemention of a downloader which uses parse_video. 
#    Copyright (C) 2016 sceext <sceext@foxmail.com>
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

import colored

from . import err, conf, log
from . import b
from . import parse, make_title, dl_worker, merge
from . import lan


def start():
    # TODO support retry
    
    # TODO support parse_twice
    # TODO support parse_twice_enable_more
    
    # do first parse to get video formats
    pvinfo = parse.parse()
    # gen format labels and print it
    labels = make_title.gen_labels(pvinfo)
    # [ OK ] log here
    log.o('got ' + str(len(labels)) + ' video formats ')
    for i in range(len(labels) -1, -1, -1):	# NOTE print labels reverse
        log.p(labels[i])
    # print video name (title)
    common_title = make_title.gen_common_title(pvinfo)
    log.p(colored.fg('blue') + 'video ' + colored.fg('light_blue') + colored.attr('bold') + common_title + colored.attr('reset') + ' ')
    
    # TODO select hd
    
    # TODO create task
    
    log.w('entry.start() not finished ')
    pass

# TODO
def _retry_error():
    pass

def _select_hd():
    pass

def _check_lock_file():
    pass

def _check_disk_space():
    pass

def _check_permission():
    pass	# TODO

def _auto_remove_tmp_files():
    pass

# TODO
# end entry.py


