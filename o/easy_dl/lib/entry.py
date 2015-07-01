# -*- coding: utf-8 -*-
# entry.py, part for parse_video : a fork from parseVideo. 
# entry:o/easy_dl/lib
# version 0.0.2.0 test201507011632
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.07. 
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

from . import parsev
from . import make_name
from . import wget

from . import conf
from . import merge

# global vars

etc = {}

etc['hd'] = 0	# video hd, quality, used for parsev --min hd --max hd

etc['min'] = -1	# min index of files to download, used for parsev --min-i
etc['max'] = -1	# max index of files to download, used for parsev --max-i

etc['out_dir'] = ''	# output file path
etc['ext_opt'] = []	# ext_opt for parsev

etc['url'] = ''	# url of video play web page
etc['flag_debug'] = False

etc['raw_name_info'] = None

# function

# entry function
def entry():
    
    # check file_num
    print('easy_dl: INFO: checking file num with url \"' + etc['url'] + '\" ')
    
    n, raw_name = get_file_info()
    
    print('easy_dl: [ OK ] found ' + str(n) + ' files. ')
    
    # save raw_name
    etc['raw_name_info'] = raw_name
    
    # process n, with etc.min and etc.max
    if etc['min'] < 0:
        etc['min'] = 0
    
    if (etc['max'] < 0) or (etc['max'] > n):
        etc['max'] = n
    
    print('easy_dl: INFO: starting mainloop')
    # start main loop
    main_loop()
    
    # done
    print('easy_dl: [ OK ] download files done. ')
    
    # TODO auto merge
    
    return 0

# base function

def main_loop():
    
    # get min and max
    i_min = etc['min']
    i_max = etc['max']
    
    file_n = i_max - i_min + 1	# download files count number
    
    print('easy_dl: INFO: will download ' + str(file_n) + ' files with index from ' + str(i_min) + ' to ' + str(i_max) + ' ')
    
    file_i = 0
    # start a loop
    for i in range(i_min, i_max + 1):
        file_i += 1
        # log info
        print('easy_dl: INFO: starting download file index [' + str(i) + '], ' + str(file_i) + ' of ' + str(file_n) + ' ')
        
        # parse this file
        print('easy_dl: INFO: start parse file index [' + str(i) + '] ')
        
        pinfo = parsev.parse(etc['url'], hd=etc['hd'], i_min=i, i_max=i, ext_opt=etc['ext_opt'])
        
        # make output name
        out_name = make_name.make_i_name(etc['raw_name_info'], i)
        out_path = make_file_path(out_name)
        
        # got url
        url_to = pinfo['list'][i]['url']
        
        # just download this file
        print('easy_dl: INFO: start download file index [' + str(i) + '] ')
        wget.dl(url_to, out_path)
        
        # download one file done
        print('easy_dl: [ OK ] download file index [' + str(i) + '], ' + str(file_i) + ' of ' + str(file_n) + ' done. ')
    
    # end mainloop

def get_file_info():
    # just parse it, to get file number
    pinfo = parsev.parse(etc['url'], hd=etc['hd'], i_min=1, i_max=0, ext_opt=etc['ext_opt'])
    
    n = len(pinfo['list'])
    
    raw_name = make_name.make_raw_name(pinfo)
    
    # done
    return n, raw_name

def make_file_path(raw):
    final = os.path.join(etc['out_dir'], raw)
    return final

def set_sub():	# set sub etc config
    
    # set flag_debug
    parsev.etc['flag_debug'] = etc['flag_debug']
    wget.etc['flag_debug'] = etc['flag_debug']
    
    # done

# end entry.py


