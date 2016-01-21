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

from . import err, b, conf, log
from . import parse, dl_worker, merge, ui
from . import lan

# TODO
def _retry_error():
    pass



def start():
    # TODO support retry
    
    # TODO support parse_twice
    # TODO support parse_twice_enable_more
    
    # TODO support enable_more, support retry parse_once
    
    # do first parse to get video formats
    pvinfo = parse.parse()
    ui.entry_print_pvinfo(pvinfo)
    # select hd
    hd = _select_hd(pvinfo)
    
    # INFO log
    log.i('second parse, call parse_video to get file URLs ')
    pvinfo = parse.parse(hd=hd)
    # create task
    task_info = parse.create_task(pvinfo, hd)
    _print_task_info(task_info)
    
    # TODO support lock
    
    # do some checks before start download
    _check_lock_file(task_info)
    _check_disk_space(task_info)
    
    # TODO download Error process
    _do_download(task_info)
    # TODO merge Error process
    merge.merge(task_info)
    
    # NOTE check auto_remove_tmp_files
    _auto_remove_tmp_files(task_info)
    # end entry.start()

def _select_hd(pvinfo):
    # get hd list
    hd_list = []
    for v in pvinfo['video']:
        hd_list.append(v['hd'])
    hd_list.sort(reverse=True)	# sort hd
    # try to select by --hd
    if conf.select_hd != None:
        if conf.select_hd in hd_list:
            return conf.select_hd
        # WARNING log
        log.w('can not select --hd ' + str(b.number(conf.select_hd)) + ', no such hd ')
    # select max hd in hd range
    hdr = conf.auto_select_hd
    out = None
    for hd in hd_list:
        if (hd >= hdr[0]) and (hd <= hdr[1]):
            out = hd
            break
    if out != None:
        return b.number(hd)
    # WARNING log
    log.w('can not select hd in range ' + str(hdr) + ', no hd available ')
    # just select max hd
    return b.number(hd_list[0])

def _print_task_info(task_info):
    merged_path = b.pjoin(task_info['path']['base_path'], task_info['path']['merged_file'])
    ui.entry_print_create_task(task_info['video']['hd'], task_info['title'], task_info['path']['log_path'], merged_path)

def _check_lock_file(task_info):
    if not conf.FEATURES['check_lock_file']:
        return
    # TODO create lock_file and remove it
    log.w('entry._check_lock_file() not finished ')
    # TODO do check

def _check_disk_space(task_info):
    if not conf.FEATURES['check_disk_space']:
        return
    # TODO do check
    log.w('entry._check_disk_space() not finished ')


## main download works

def _do_download(task_info):
    # TODO fix task_info video count info before download
    v = task_info['video']
    count = len(v['file'])
    ui.entry_print_start_download(count, v['size_byte'], v['time_s'])
    # reset count
    count_ok = 0
    count_err = 0
    done_size = 0
    rest_size = v['size_byte']
    done_time = 0
    rest_time = v['time_s']
    # download each file
    for i in range(count):
        f = v['file'][i]
        # TODO print download speed, rest time, etc. 
        ui.entry_print_before_download(i, count, f['_part_name'], f['size'], f['time_s'])
        if dl_worker.dl_one_file(f):	# do download one file
            count_ok += 1
            # NOTE support task_info without size_byte, size, time_s, etc. 
            if f['size'] >= 0:	# -1 means None
                done_size += f['size']
            if f['time_s'] >= 0:
                done_time += f['time_s']
        else:
            count_err += 1
        # update count, NOTE support no info
        if f['size'] >= 0:
            rest_size -= f['size']
        if f['time_s'] >= 0:
            rest_time -= f['time_s']
        ui.entry_print_download_status(count_err, count_ok, done_size, v['size_byte'], done_time, v['time_s'], rest_size, rest_time)
    # download done, check download succeed
    if count_err > 0:
        log.e('download part files failed, err ' + str(count_err) + '/' + str(count) + ' ')
        raise err.DownloadError('part file', count_err, count)
    # download OK
    log.o('download part files finished, OK ' + str(count_ok) + '/' + str(count) + ' ')


def _auto_remove_tmp_files(task_info):
    if not conf.FEATURES['auto_remove_tmp_files']:
        return
    # check required features
    if not conf.FEATURES['check_merged_time']:
        log.e('disabled feature auto_remove_tmp_files. To enable this, feature check_merged_time must be enabled ')
        return
    if not conf.FEATURES['merge_single_file']:
        log.e('disabled feature auto_remove_tmp_files. To enable this, feature merge_single_file must be enabled ')
        return
    # TODO do remove
    log.w('entry._auto_remove_tmp_files() not finished ')


# end entry.py


