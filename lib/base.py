# -*- coding: utf-8 -*-
# base.py, part for parse_video : a fork from parseVideo. 
# base: base part. 
# version 0.0.7.0 test201505061449
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.05. 
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

from urllib import request
import re
import json
import multiprocessing

# global vars
# USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'

# functions

def re1(re0, text):
    result = re.findall(re0, text)
    return result[0]

# just return the content of the url as raw string
# TODO this may be not stable
def simple_http_get(url, user_agent, referer):
    # make headers
    header = {}
    header['User-Agent'] = user_agent
    if referer != None:
        header['Referer'] = referer
    # start a http request
    req = request.Request(url, headers=header)
    # res, response
    res = request.urlopen(req)
    data = res.read()
    # check 'Content-Encoding'
    try:
        ch = re1(r'charset=([\w-]+)', res.getheader('Content-Type'))
    except BaseException as err:
        ch = 'utf-8'
    if type(ch) != type(''):
        ch = 'utf-8'
    if ch == '':
        ch = 'utf-8'
    # just use this charset
    content = data.decode(ch, 'ignore')
    # done
    return content

# return the html content of url as string
def get_html_content(url, user_agent=USER_AGENT, referer=None):
    # just use simple_http_get
    return simple_http_get(url, user_agent=user_agent, referer=referer)

# return object, the text of the url is json format
def get_json_info(url, user_agent=USER_AGENT, referer=None):
    # get text
    text = simple_http_get(url, user_agent=user_agent, referer=referer)
    # use json to decode it
    info = json.loads(text)
    # done
    return info

# map_do, do many tasks at the same time, use multiprocessing.Pool(), .map()
def map_do(todo_list, worker, pool_size=4):
    # create process pool
    pool = multiprocessing.Pool(processes=pool_size)
    pool_output = pool.map(worker, todo_list)
    # do it
    pool.close()
    pool.join()
    # done
    return pool_output

# class

# end base.py


