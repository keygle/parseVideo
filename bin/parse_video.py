# -*- coding: utf-8 -*-
# parse_video.py, parse_video/bin
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509272230
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
parse_video main bin entry file
'''

import json

from . import about

# NOTE should be set, as import
lib = None

# global data
etc = {}
# options support config
etc['hd_min'] = None	# support option --min <hd>
etc['hd_max'] = None	# support option --max <hd>
etc['i_min'] = None	# support option --min-i <file_index>
etc['i_max'] = None	# support option --max-i <file_index>
etc['extractor'] = ''	# support option --extractor <>
etc['method'] = ''	# support option --method <>
etc['output'] = '-'	# support option --output <file>; default value - means stdout
etc['log_level'] = None	# support option --debug --quiet; support '--debug' and '--quiet'
etc['flag_output_no_restruct'] = False	# support option --output-no-restruct
# default option is raw_url
etc['raw_url'] = None
# options for start mode
etc['flag_start_version'] = False		# support option --version
etc['flag_start_help'] = False			# support option --help
etc['flag_start_extractor_list'] = False	# support option --extractor-list
# for help extactor id
etc['help_extractor_id'] = None	# support --help <extractor_id>

# main show version, show help, show extractor list functions
def _show_version():
    print('TODO: show version info not finished. ')

def _show_help():
    # get extractor id
    extractor_id = etc['help_extractor_id']
    # TODO FIXME not finished
    print('TODO: show help info for extractor_id \"' + str(extractor_id) + '\" not finished. ')
    pass

def _show_extractor_list():
    print('TODO: show extractor_list info not finished. ')

# main parse entry function
def _parse():
    raw_url = etc['raw_url']
    # check raw_url
    if not raw_url:
        _p_cline_err('(not input raw_url)')
        return True
    # get lib functions
    var = lib.var
    err = lib.err
    log = lib.log
    # init lib.var
    var.push()
    var._ = var.init()
    # set lib for parse
    var._['hd_min'] = etc['hd_min']
    var._['hd_max'] = etc['hd_max']
    var._['i_min'] = etc['i_min']
    var._['i_max'] = etc['i_max']
    var._['flag_output_no_restruct'] = etc['flag_output_no_restruct']
    # set debug filter flag
    if etc['log_level'] == '--debug':
        var.log_filter['DEBUG:'] = True
    elif etc['log_level'] == '--quiet':
        var.log_filter['DEBUG:'] = False
        var.log_filter[''] = False
        var.log_filter['INFO:'] = False
        var.log_filter['[ OK ]'] = False
        var.log_filter['WARNING:'] = False
    # get options
    raw_extractor = etc['extractor']
    raw_method = etc['method']
    # try to parse
    try:
        evinfo = _do_parse(raw_url, raw_extractor, raw_method)
    except err.PVError as e:
        log.e('parse failed ')
        raise
    except Exception as e:	# TODO make better print for ERRORs
        log.e('parse unknow ERROR ')
        er = err.UnknowError('parse unknow ERROR ')
        raise er from e
    finally:	# recovery lib.var
        var._ = var.pop()
    # output result
    if etc['flag_output_no_restruct']:
        out_text = json.dumps(evinfo, indent=None, sort_keys=False, ensure_ascii=True)
    else:
        out_text = json.dumps(evinfo, indent=4, sort_keys=False, ensure_ascii=False)
    # check output file
    output_file = etc['output']
    if output_file == '-':	# just print it
        print(out_text)
        return	# done
    # try to open output file
    out_data = out_text.encode('utf-8')
    try:
        f = open(output_file, 'wb')
    except Exception as e:
        er = Exception('can not open output file \"' + output_file + '\" ')
        raise er from e
    try:
        f.write(out_data)
    except Exception as e:
        er = Exception('can not write output file \"' + output_file + '\" ')
        er.raw_data = out_data
        raise er from e
    finally:	# just close file
        f.close()
    # parse process done

def _do_parse(raw_url, raw_extractor, raw_method):
    return lib.parse(raw_url, raw_extractor=raw_extractor, raw_method=raw_method)

# main process args function
# NOTE will check more on command line args and options
def _pargs(argv):
    log = lib.log
    
    rest = argv.copy()
    # check args length
    if len(rest) < 1:
        _p_cline_err()
        raise Exception('cline error')
    # process each arg
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        # easy flag options
        if one == '--version':
            # check already set flag
            if etc['flag_start_version']:
                log.w('already set ' + one + ' ')
            etc['flag_start_version'] = True
        elif one == '--extractor-list':
            if etc['flag_start_extractor_list']:
                log.w('already set ' + one + ' ')
            etc['flag_start_extractor_list'] = True
        elif one == '--output-no-restruct':
            if etc['flag_output_no_restruct']:
                log.w('already set ' + one + ' ')
            etc['flag_output_no_restruct'] = True
        elif one in ['--debug', '--quiet']:
            # check log_level
            if etc['log_level'] != None:
                log.w('already set log_level to \"' + etc['log_level'] + '\", now set log_level to \"' + one + '\" ')
            etc['log_level'] = one
        # option with values or none
        elif one == '--help':	# --help or --help <extractor_id>
            # try to get extractor id
            if len(rest) > 0:
                extractor_id, rest = _try_get_next(rest)
            else:
                extractor_id = None
            # check already set flag
            if etc['flag_start_help']:
                log.w('already set ' + one + ' ')
            # check extractor_id
            if extractor_id:
                if etc['help_extractor_id']:
                    log.w('already set --help extractor_id to \"' + etc['help_extractor_id'] + '\", now set to \"' + extractor_id + '\" ')
                etc['help_extractor_id'] = extractor_id
        # option with values
        elif one in ['-e', '--extractor']:	# --extractor <>
            extractor, rest = _try_get_next(rest, one)
            # check already set value
            if etc['extractor']:
                log.w('already set extractor to \"' + etc['extractor'] + '\", now set to \"' + extractor + '\" ')
            etc['extractor'] = extractor
        elif one == '--method':	# --method <>
            method, rest = _try_get_next(rest, one)
            if etc['method']:
                log.w('already set method to \"' + etc['method'] + '\", now set to \"' + method + '\" ')
            etc['method'] = method
        elif one == '--output':	# --output <file>
            output, rest = _try_get_next(rest, one)
            if etc['output'] != '-':	# default value of output is '-'
                log.w('already set output to \"' + etc['output'] + '\", now set to \"' + output + '\" ')
            etc['output'] = output
        # should parse option values
        elif one == '--min':	# --min <hd>
            hd, rest = _try_get_next(rest, one)
            try:
                hd = int(hd)
            except Exception as e:
                _p_cline_err('(can not parse hd value \"' + hd + '\" to int for --min ')
                raise
            # check value already set
            if etc['hd_min'] != None:
                log.w('already set hd_min to ' + str(etc['hd_min']) + ', now set to ' + str(hd) + ' ')
            etc['hd_min'] = hd
        elif one == '--max':	# --max <hd>
            hd, rest = _try_get_next(rest, one)
            try:
                hd = int(hd)
            except Exception as e:
                _p_cline_err('(can not parse hd value \"' + hd + '\" to int for --max ')
                raise
            if etc['hd_max'] != None:
                log.w('already set hd_max to ' + str(etc['hd_max']) + ', now set to ' + str(hd) + ' ')
            etc['hd_max'] = hd
        elif one == '--min-i':	# --min-i <i>
            i, rest = _try_get_next(rest, one)
            try:
                i = int(i)
            except Exception as e:
                _p_cline_err('(can not parse value \"' + i + '\" to int for --min-i ')
                raise
            if etc['i_min'] != None:
                log.w('already set i_min to ' + str(etc['i_min']) + ', now set to ' + str(i) + ' ')
            etc['i_min'] = i
        elif one == '--max-i':	# --max-i <i>
            i, rest = _try_get_next(rest, one)
            try:
                i = int(i)
            except Exception as e:
                _p_cline_err('(can not parse value \"' + i + '\" to int for --max-i ')
                raise
            if etc['i_max'] != None:
                log.w('already set i_max to ' + str(etc['i_max']) + ', now set to ' + str(i) + ' ')
            etc['i_max'] = i
        # default option
        else:	# this should be raw_url
            # check value already set
            if etc['raw_url'] != None:
                log.w('already set raw_url to \"' + etc['raw_url'] + '\", now set to \"' + one + '\" ')
            etc['raw_url'] = one
    # process args done

# try to get next args
def _try_get_next(rest, option_info=''):
    if len(rest) < 1:
        _p_cline_err('(no value after ' + option_info + ' )')
        raise Exception('cline error')
    return rest[0], rest[1:]

# print command line ERROR
def _p_cline_err(err_info=''):
    lib.log.e('command line ERROR. ' + err_info + '\n    please try --help to show help info. ')

# NOTE main function
def main(argv):
    # try to parse args
    try:
        _pargs(argv)
    except Exception as e:	# process command line options failed
        return True	# if got here, already printed error msg; should just exit
    # check start flag
    if etc['flag_start_help']:	# check for --help
        _show_help()
    elif etc['flag_start_version']:	# check for --version
        _show_version()
    elif etc['flag_start_extractor_list']:	# check for --extractor-list
        _show_extractor_list()
    else:	# should start in normal mode, parse
        _parse()
    # done

# end parse_video.py


