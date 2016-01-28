# -*- coding: utf-8 -*-
# pvdl.py, parse_video/pvdl/bin/
# language: English (en)
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
''' pvdl main bin file

OPTIONS not in --help: 

TODO support speed limit (only for wget)
  --limit-kb  VALUE  limit download speed to value (unit KB/s)

'''
# NOTE support --list mode here

import time

from lib import err, b, conf, log
from lib import entry, lan

VERSION_STR = 'pvdl version 0.0.11.0 test201601281312'

# global data
etc = {}
etc['start_mode'] = 'normal'	# ['normal', '--help', '--version', '--license', 'list']
etc['list_file'] = ''
etc['list_retry'] = conf.list_retry_times	# NOTE use default value


# print functions

def p_help():
    print('''\
Usage: pvdl [OPTION]... URL
pvdl: A reference implemention of a downloader which uses parse_video. 

      --hd HD                  set hd to select
  -o, --output DIR             save downloaded file to DIR
      --title-suffix SUFFIX    add suffix to resolve name conflicts
      --title-no NO            set title_no
      --retry TIMES            set retry times
      --retry-wait SECONDS     wait seconds before retry
      --parse-timeout SECONDS  set parse timeout
      
      --enable FEATURE   enable pvdl features
      --disable FEATURE  disable pvdl features
      
      --list FILE         download each item in list file
      --list-retry TIMES  set list retry times
      
      --  directly pass options to parse_video
  
  -d, --debug  set log level to debug
      
      --help     display this help and exit
      --version  output version information and exit
      --license  show license information and exit

More information online: <https://github.com/sceext2/parse_video> \
''')

def p_version():
    print(VERSION_STR + '''

    pvdl  Copyright (C) 2016  sceext <sceext@foxmail.com>
    This program comes with ABSOLUTELY NO WARRANTY. This is free software, and 
    you are welcome to redistribute it under certain conditions. 

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>. 
Please use "--license" or read LICENSE for more details. \
''')

def p_license():
    print('''\
    pvdl : A reference implemention of a downloader which uses parse_video. 
    Copyright (C) 2016 sceext <sceext@foxmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. \
''')

def p_cline_err():
    log.e('bad command line format, please try \"--help\". ')

# NOTE main function
def main(args):
    try:
        p_args(args)
    except Exception:
        p_cline_err()
        raise
    # check main start mode
    mode_list = {
        'normal' : start_normal, 
        'list' : start_list, 
        '--help' : p_help, 
        '--version' : p_version, 
        '--license' : p_license, 
    }
    worker = mode_list[etc['start_mode']]
    worker()
    # end main

# process command line args
def p_args(args):
    rest = args.copy()
    while len(rest) > 0:
        one, rest = rest[0], rest[1:]
        # --help, --version, --license
        if one in ['--help', '--version', '--license']:
            if etc['start_mode'] == '--help':
                log.e('already set start_mode to \"' + etc['start_mode'] + '\", can not set to \"' + one + '\" ')
                continue
            elif etc['start_mode'] != 'normal':
                log.w('already set start_mode to \"' + etc['start_mode'] + '\", now set to \"' + one + '\" ')
            etc['start_mode'] = one
        # enable disable features
        elif one in ['--disable', '--enable']:
            text_to_enable = {
                '--disable' : False, 
                '--enable' : True, 
            }
            raw, rest = rest[0], rest[1:]
            disable_enable_features(raw, text_to_enable[one])
        # directly pass args to parse_video
        elif one == '--':
            conf.raw_args = rest
            break	# NOTE stop parse args
        # set config
        elif one == '--hd':
            hd, rest = rest[0], rest[1:]
            hd = float(hd)
            if conf.select_hd != None:
                log.w('already set hd to ' + str(conf.select_hd) + ', now set to ' + str(hd) + ' ')
            conf.select_hd = hd
        elif one in ['-o', '--output']:
            output, rest = rest[0], rest[1:]
            if conf.set_output != conf.output_dir:
                log.w('already set output to \"' + conf.set_output + '\", now set to \"' + output + '\" ')
            conf.set_output = output
        elif one == '--title-suffix':
            suffix, rest = rest[0], rest[1:]
            if conf.title_suffix != None:
                log.w('already set suffix to \"' + conf.title_suffix + '\", now set to \"' + suffix + '\" ')
            conf.title_suffix = suffix
        elif one == '--title-no':
            no, rest = rest[0], rest[1:]
            no = int(no)
            if conf.title_no != None:
                log.w('already set title_no to ' + str(conf.title_no) + '\", now set to \"' + str(no) + '\" ')
            conf.title_no = no
        elif one == '--retry':
            retry, rest = rest[0], rest[1:]
            retry = int(retry)
            if conf.set_retry != conf.error_retry:
                log.w('already set retry to ' + str(conf.set_retry) + ', now set to ' + str(retry) + ' ')
            conf.set_retry = retry
        elif one == '--retry-wait':
            wait, rest = rest[0], rest[1:]
            wait = float(wait)
            if conf.set_retry_wait != conf.retry_wait_time_s:
                log.w('already set retry_wait to ' + str(conf.set_retry_wait) + ', now set to ' + str(wait) + ' ')
            conf.set_retry_wait = wait
        # DEBUG mode
        elif one in ['-d', '--debug']:
            if conf.flag_debug:
                log.w('already set debug mode ')
            conf.flag_debug = True
        # --limit-kb
        elif one == '--limit-kb':
            limit, rest = rest[0], rest[1:]
            limit = float(limit)
            if conf.limit_kb != None:
                log.w('already set limit_kb to ' + str(conf.limit_kb) + ', now set to ' + str(limit) + ' ')
            conf.limit_kb = limit
        # --parse-timeout
        elif one == '--parse-timeout':
            timeout, rest = rest[0], rest[1:]
            timeout = float(timeout)
            if conf.set_parse_timeout != conf.parse_timeout_s:
                log.w('already set parse_timeout_s to ' + str(conf.set_parse_timeout) + ', now set to ' + str(timeout) + ' ')
            conf.set_parse_timeout = timeout
        # --list
        elif one == '--list':
            fname, rest = rest[0], rest[1:]
            if etc['list_file'] != '':
                log.w('already set list file to \"' + etc['list_file'] + '\", now set to \"' + fname + '\" ')
            etc['list_file'] = fname
            # NOTE set start mode to list
            etc['start_mode'] = 'list'
        # --list-retry
        elif one == '--list-retry':
            retry, rest = rest[0], rest[1:]
            retry = int(retry)
            if etc['list_retry'] != conf.list_retry_times:
                log.w('already set list retry to ' + str(etc['list_retry']) + ', now set to ' + str(retry) + ' ')
            etc['list_retry'] = retry
        else:	# NOTE set URL
            if conf.raw_url != '':
                log.w('already set raw_url to \"' + conf.raw_url + '\", now set to \"' + one + '\" ')
            conf.raw_url = one
    # end p_args

def disable_enable_features(raw, enable=False):
    enable_to_text = {
        False : 'disable', 
        True : 'enable', 
    }
    feature_list = raw.split(',')
    for f in feature_list:
        if not f in conf.FEATURES:
            log.e('can not ' + enable_to_text[enable] + ' feature [' + f + '], no such feature ')
            raise err.ConfigError('no such feature', f)
        elif conf.FEATURES[f] == enable:
            log.w('already ' + enable_to_text[enable] + ' feature [' + f + '] ')
        conf.FEATURES[f] = enable
    # end disable_enable_features


# normal start mode
def start_normal():
    # check input_url
    if conf.raw_url == '':
        conf.raw_url = input_url()
    # NOTE set pvdl version info
    conf.pvdl_version = VERSION_STR
    # just start pvdl
    try:
        entry.start()
    except err.PvdlError:
        raise
    except Exception as e:
        log.e('unknow pvdl Error ')	# TODO improve output here
        er = err.UnknowError('unknow pvdl error')
        raise er from e

def input_url():
    log.p(b.color_reset() + b.color_light_yellow(), end='')
    log.p('pvdl:: please input URL of a video play page: ', end='')
    log.p(b.color_reset() + b.color_white() + b.color_bold(), end='')
    raw = input()
    log.p(b.color_reset(), end='')
    # check input URL
    out = raw.strip()
    if out == '':
        log.e('can not input empty URL ')
        raise err.ConfigError('input empty URL', out)
    return out

# --list mode
def start_list():
    # TODO support read list file from stdin
    todo = _load_list_file()
    # [ OK ] log
    log.o('got ' + str(len(todo)) + ' URLs ')
    # do list with retry
    _do_with_retry(todo)
    # end start_list

def _load_list_file():
    fpath = etc['list_file']
    log.i('loading list file \"' + fpath + '\" ')
    try:
        with open(fpath, 'rb') as f:
            blob = f.read()
        text = blob.decode('utf-8', 'ignore')	# NOTE ignore decoding Error
        info = _parse_list_file(text)
    except Exception as e:
        log.e('can not load list file \"' + fpath + '\" ')
        er = err.ConfigError('load list_file', fpath)
        raise er from e
    return info

def _parse_list_file(text):
    line = text.splitlines()
    out = []
    for l in line:	# process each line
        if l.startswith('#'):
            continue	# ignore line startswith '#', comment line
        elif l.strip() == '':
            continue	# ignore null line
        out.append(l)	# add URL line
    return out

def _do_with_retry(raw):
    # NOTE in list mode, will ignore all Errors
    retry_max = etc['list_retry']
    retry_count = 0
    def check_should_retry():
        if retry_max < 0:	# -1 means retry forever
            return True
        if retry_count <= retry_max:
            return True
    while check_should_retry():
        retry_info = str(retry_count) + '/' + str(retry_max)
        # print retry info
        if retry_count > 0:
            log.i('[list] start retry ' + retry_info)
        # count info
        count = len(raw)
        count_ok = 0
        count_err = 0
        # do each task
        log.i('[list] start ' + str(count) + ' task ')
        for i in range(count):
            task_info = str(i + 1) + ' / ' + str(count)
            item = raw[i]
            log.p('')	# NOTE for better print
            log.i('[list] (ok ' + str(count_ok) + ', err ' + str(count_err) + ') start task ' + task_info + ', ' + item + ' ')
            try:
                _do_one_task(item)
            except Exception as e:
                log.e('[list] task ' + task_info + ' failed, ' + str(e) + ' \n')
                # NOTE ignore Error in list mode
                count_err += 1
            else:
                log.o('[list] task ' + task_info + ' finished \n')
                count_ok += 1
        # check retry
        retry_text = ''
        if retry_count > 0:
            retry_text = ', retry ' + retry_info
        if count_err == 0:	# no Error, not retry
            log.o('[list] all task finished ' + str(count_ok) + ' / ' + str(count) + retry_text + ' ')
            break	# not retry
        # should retry
        log.e('[list] task failed ' + str(count_err) + ' / ' + str(count) + retry_text + ' ')
        # update retry count
        retry_count += 1
        # check should retry
        if check_should_retry():
            log.i('[list] before next retry wait ' + str(conf.list_retry_wait_s) + ' seconds ')
            time.sleep(conf.list_retry_wait_s)
        else:
            log.e('[list] task retry failed' + retry_text + ' ')
    # end _do_with_retry

def _do_one_task(url):
    # NOTE just set URL and call entry
    conf.raw_url = url
    # NOTE just start_normal
    start_normal()


# end pvdl.py


