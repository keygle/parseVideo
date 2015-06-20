# -*- coding: utf-8 -*-
# base.py, part for info_source of evdh : EisF Video Download Helper, sceext <sceext@foxmail.com> 2009EisF2015, 2015.05 
# lib/is/base: info_source base support. 
# version 0.1.5.2 test201506201236
# copyright 2015 sceext All rights reserved. 
#

# import

import json
import datetime
import subprocess
import sys
import urllib.request as request
import multiprocessing.dummy as multiprocessing

# global vars
log_level = 2000	# default log_level normal 2000

flag_fix_unicode = False	# print json text, fix unicode

USER_AGENT = None

# functions

# simple console log functions
def set_log_level(level):
    global log_level
    log_level = level

def log(level, text):
    # check level
    if level < log_level:
        print(text)
        try:
            sys.stdout.flush()
        except Exception:
            pass	# run in pythonw, no sys.stdout, None

# pretty json print
def pretty_json_print(obj):
    text = json.dumps(obj, indent=4, sort_keys=False, ensure_ascii=flag_fix_unicode)
    return text

# subprocess functions

def run(args, shell=False):
    exit_code = subprocess.call(args, shell=shell)
    return exit_code

def get_output(args, shell=False):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(args, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return p.communicate()

# text process

# remove chars before and after text
def pure_string(text, to_remove=' \n	'):
    rest = text
    # check length
    if len(rest) < 1:
        return rest
    # remove before
    while rest[0] in to_remove:
        rest = rest[1:]
        if len(rest) < 1:
            return rest
    # remove after
    while rest[-1] in to_remove:
        rest = rest[:len(rest) - 1]
        if len(rest) < 1:
            return rest
    # done
    return rest

# http request
def http_get(url_to, user_agent=USER_AGENT, referer=None):
    # make headers
    header = {}
    if user_agent != None:
        header['User-Agent'] = user_agent
    if referer != None:
        header['Referer'] = referer
    # start http request
    req = request.Request(url_to, headers=header, method='GET')
    # res, response
    with request.urlopen(req) as res:
        data = res.read()
    # just decode it as utf-8
    content = data.decode('utf-8', 'ignore')
    # done
    return content

def http_head(url_to, user_agent=USER_AGENT, referer=None):
    # make headers
    header = {}
    if user_agent != None:
        header['User-Agent'] = user_agent
    if referer != None:
        header['Referer'] = referer
    # start http request
    req = request.Request(url_to, headers=header, method='HEAD')
    # res, response
    resp = {}
    with request.urlopen(req) as res:
        resp['code'] = res.code		# get http code and http headers
        resp['header'] = res.headers
    # translate header name
    header = {}
    for i in resp['header']:
        header[i.lower()] = resp['header'][i]
    resp['header'] = header
    # done
    return resp

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

# time function
def get_iso_now():
    raw = datetime.datetime.utcnow().isoformat()
    raw += 'Z'
    return raw

# end base.py


