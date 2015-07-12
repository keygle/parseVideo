# -*- coding: utf-8 -*-
# base.py, part for parse_video : a fork from parseVideo. 
# base: base part. 
# version 0.1.8.0 test201507071615
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

from urllib import request
import re
import json
import multiprocessing.dummy as multiprocessing

import socket

# global vars
# USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0'
# USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'

# base global http_proxy setting
http_proxy = None

# functions

def re1(re0, text):
    result = re.findall(re0, text)
    return result[0]

# http_get with http_proxy
def http_proxy_http_get(url, proxy=None, header={}):
    
    # create proxy
    proxy_handler = request.ProxyHandler({'http' : proxy})
    opener = request.build_opener(proxy_handler)
    
    # make headers
    header_list = []
    for i in header:
        header_list.append((i, header[i]))
    # add headers
    opener.addheaders = header_list
    
    # just start http_get request and return raw data
    raw = None
    with opener.open(url) as f:
        raw = f.read()
    
    # done
    return raw

# just return the content of the url as raw string
# TODO this may be not stable
def simple_http_get(url, user_agent, referer, header={}, method='GET'):
    more_header = header
    # make headers
    header = {}
    header['User-Agent'] = user_agent
    if referer != None:
        header['Referer'] = referer
    # add connection close
    header['Connection'] = 'close'
    
    # add more headers
    for h in more_header:
        header[h] = more_header[h]
    
    # check http_proxy
    if http_proxy != None:
        raw = http_proxy_http_get(url, proxy=http_proxy, header=header)
        # TODO now just spport utf-8
        content = raw.decode('utf-8', 'ignore')
        # done
        return content
    # NOT use http_proxy
    
    # start a http request
    req = request.Request(url, headers=header, method=method)
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
def get_html_content(url, user_agent=USER_AGENT, referer=None, header={}, method='GET'):
    # just use simple_http_get
    return simple_http_get(url, user_agent=user_agent, referer=referer, header=header, method=method)

# return object, the text of the url is json format
def get_json_info(url, user_agent=USER_AGENT, referer=None, header={}, method='GET'):
    # get text
    text = simple_http_get(url, user_agent=user_agent, referer=referer, header=header, method=method)
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

# http post
def http_post(url, post_data='', user_agent=USER_AGENT, referer=None, cookie=None, fix_header=None, flag_debug=False):
    # make headers
    header = {}
    header['User-Agent'] = user_agent
    if referer != None:
        header['Referer'] = referer
    if cookie != None:
        header['Cookie'] = cookie
    # add connection close
    header['Connection'] = 'close'
    
    # fix headers
    if fix_header != None:
        for i in fix_header:
            header[i] = fix_header[i]
    
    data = bytes(post_data, 'utf-8')	# encode as utf-8
    # add content-length
    content_len = len(data)
    header['Content-Length'] = str(content_len)
    
    # parse url
    first_p = url.split('://', 1)
    next_p = first_p[1].split('/', 1)
    host_p = next_p[0]
    get_p = next_p[1]
    if get_p[0] != '/':
        get_p = '/' + get_p
    port = 80	# TODO
    
    # add Host header
    header['Host'] = host_p
    
    # use socket to send http POST
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host_p, port))
    
    # make http head text
    ht = []
    ht += ['POST ' + get_p + ' HTTP/1.1']
    # add headers
    for h in header:
        ht += [str(h) + ': ' + str(header[h])]
    # done
    ht_text = ('\r\n').join(ht)
    ht_text += '\r\n\r\n'
    
    # DEBUG info
    if flag_debug:
        print('base: DEBUG: http text to send [' + ht_text + ']')
    
    # send http head
    s.send(bytes(ht_text, 'utf-8'))
    # post data
    s.send(data)
    
    recv_size_byte = 1024
    # recv data
    recv_data = []
    while True:
        d = s.recv(recv_size_byte)
        if d:
            recv_data.append(d)
        else:
            break
    # recv done
    data = (b'').join(recv_data)
    data = data.decode('utf-8', 'ignore')
    
    # remove http head
    http_part = data.split('\r\n\r\n', 1)
    
    # DEBUG info
    if flag_debug:
        print('base: DEBUG: got http head [\n' + http_part[0] + ']')
    
    return http_part[1]
    # start http request
    req = request.Request(url, method='POST', headers=header, data=data)
    # res, response
    res = request.urlopen(req)
    data = res.read()
    
    # just decode as utf-8
    content = data.decode('utf-8', 'ignore')
    # done
    return content

# class

# end base.py


