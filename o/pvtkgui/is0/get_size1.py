# -*- coding: utf-8 -*-
# get_size1.py, part for info_source of evdh : EisF Video Download Helper, sceext <sceext@foxmail.com> 2009EisF2015, 2015.06 
# lib/is/half/get_size1: info_source: get_size1. 
# version 0.1.4.1 test201506201137
# copyright 2015 sceext All rights reserved. 
#

# import

from . import base

# global vars

HTTP_HEAD_OK_CODE = 200
POOL_SIZE_GET_SIZE = 8

# functions

def get_one_size(item):
    # get args
    url_to = item['url']
    user_agent = None
    referer = None
    if 'user_agent' in item:
        user_agent = item['user_agent']
    if 'referer' in item:
        referer = item['referer']
    # use http HEAD to get size
    try:
        res = base.http_head(url_to, user_agent, referer)
    except Exception as e:
        base.log(2500, 'get_size1: get size of \"' + url_to + '\" failed, error \"' + str(e) + '\"')
        return -1
    # get size by Content-Length
    if (res['code'] == HTTP_HEAD_OK_CODE) and ('content-length' in res['header']):
        return int(res['header']['content-length'])
    else:
        base.log(2500, 'get_size1: get size of \"' + url_to + '\" failed, no \"Content-Length\" in resporse http headers. ')
        return -1
    # done

# get_size main function
def get_size(item_list, pool_size=POOL_SIZE_GET_SIZE):
    # use map_do to get many size at the same time
    size_list = base.map_do(item_list, get_one_size, pool_size=pool_size)
    # done
    return size_list

# easy get size method
def easy_get_size(evinfo, log_msg='(unknow) Getting size ...', ignore_m3u8=True, pool_size=POOL_SIZE_GET_SIZE):
    todo_item_list = []
    # make todo get_size item list
    for v in evinfo['video']:
        if ignore_m3u8 and (v['format'] == 'm3u8'):
            continue
        for f in v['file']:
            if f['size'] < 1:
                one = {}
                one['url'] = f['url']
                if 'user_agent' in f:
                    one['user_agent'] = f['user_agent']
                if 'referer' in f:
                    one['referer'] = f['referer']
                todo_item_list.append(one)
    # todo list done, get size now
    if len(todo_item_list) > 0:
        base.log(1500, log_msg + ' (' + str(len(todo_item_list)) + ', ' + str(pool_size) + ')')
        size_list = get_size(todo_item_list, pool_size=pool_size)
    # get size done, write back result
    size_i = 0
    for v in evinfo['video']:
        if ignore_m3u8 and (v['format'] == 'm3u8'):
            continue
        for f in v['file']:
            if f['size'] < 1:
                f['size'] = size_list[size_i]
                size_i += 1
    # save result done, recount size
    for v in evinfo['video']:
        flag_size_ok = True
        size_count = 0
        for f in v['file']:
            if f['size'] < 0:
                flag_size_ok = False
                break
            size_count += f['size']
        if flag_size_ok and (len(v['file']) > 0):
            v['size_byte'] = size_count
        else:
            pass
            # NOTE not reset size_byte
            # v['size_byte'] = -1
    # re-count size done, easy get size done
    return evinfo

# end get_size1.py


