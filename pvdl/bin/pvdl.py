# -*- coding: utf-8 -*-
# pvdl.py, parse_video/pvdl/bin/
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


TODO support options (new functions)
  --list  LIST file

TODO support speed limit (only for wget)
  --limit-kb  VALUE  limit download speed to value (unit KB/s)

TODO support parse timeout_s
  --parse-timeout-s

'''

from lib import entry, log, lan, err, conf

VERSION_STR = 'pvdl version 0.0.8.0 test201601232301'

# global data
etc = {}
etc['start_mode'] = 'normal'	# ['normal', '--help', '--version', '--license']


# print functions

def p_help():
    print('''\
Usage: pvdl [OPTION]... URL
pvdl: A reference implemention of a downloader which uses parse_video. 

      --hd HD                set hd to select
  -o, --output DIR           save downloaded file to DIR
      --title-suffix SUFFIX  add suffix to resolve name conflicts
      --title-no NO          set title_no
      --retry TIMES          set retry times
      --retry-wait SECONDS   wait seconds before retry
      
      --enable FEATURE   enable pvdl features
      --disable FEATURE  disable pvdl features
      
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
        # --parse-timeout-s
        elif one == '--parse-timeout-s':
            timeout, rest = rest[0], rest[1:]
            timeout = float(timeout)
            if conf.set_parse_timeout != conf.parse_timeout_s:
                log.w('already set parse_timeout_s to ' + str(conf.set_parse_timeout) + ', now set to ' + str(timeout) + ' ')
            conf.set_parse_timeout = timeout
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
    from colored import fg, attr
    log.p(attr('reset') + fg('light_yellow'), end='')
    log.p('pvdl:: please input URL of a video play page: ', end='')
    log.p(attr('reset') + fg('white') + attr('bold'), end='')
    raw = input()
    log.p(attr('reset'), end='')
    # check input URL
    out = raw.strip()
    if out == '':
        log.e('can not input empty URL ')
        raise err.ConfigError('input empty URL', out)
    return out


# end pvdl.py


