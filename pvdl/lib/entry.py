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

import os
import time
import functools

from . import err, b, conf, log
from . import parse, dl_worker, merge, ui
from . import lan


# pvdl core entry function
def start():
    # NOTE support retry here
    retry_count = 0
    # check to retry
    def check_should_retry():
        if conf.set_retry < 0:	# NOTE -1 means retry forever
            return True
        if retry_count <= conf.set_retry:
            return True
    # NOTE -1 means retry forever
    while check_should_retry():
        retry_info = str(retry_count) + ' / ' + str(conf.set_retry)
        # print retry info
        if retry_count > 0:
            log.i('pvdl task retry ' + retry_info)
        try:
            _do_can_retry()
            # print retry OK info
            if retry_count > 0:
                log.o('pvdl task finished at retry ' + retry_info + ' ')
            break	# no more retry
        except err.RetryableError as e:	# ignore this Error
            # ERROR log
            if retry_count > 0:
                log.e('pvdl task failed at retry ' + retry_info + ' ')
            else:
                log.e('pvdl task failed ')
            # update retry count
            retry_count += 1
            # NOTE sleep before retry
            if check_should_retry():
                log.i('wait ' + str(conf.set_retry_wait) + ' s before next retry ')
                time.sleep(conf.set_retry_wait)
        except Exception:
            raise	# not process other Errors
    # end entry.start()

# NOTE this works can be retry
def _do_can_retry():
    # TODO maybe not support parse_twice_enable_more, for lock file
    # TODO support parse_once
    # TODO support parse_twice enable_more
    
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
    
    tmp_path = task_info['path']['tmp_path']
    lock_file = task_info['path']['lock_file']
    lock_path = b.pjoin(tmp_path, lock_file)
    # NOTE try to create tmp_path
    try:
        if not os.path.isdir(tmp_path):
            os.makedirs(tmp_path)
    except Exception as e:
        log.e('can not create tmp dir \"' + tmp_path + '\" ')
        er = err.ConfigError('create tmp_dir', tmp_path)
        raise er from e
    # NOTE run _do_with_lock() in _do_in_lock()
    f = functools.partial(_do_with_lock, task_info, pvinfo)
    _do_in_lock(f, lock_path)

def _do_in_lock(f, lock_file):
    lock_fd = None
    # get lock (create lock file)
    try:
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_TRUNC, mode=0o666)
        log.d('got lock \"' + lock_file + '\" ')
    except Exception as e:	# get lock failed
        # check skip_lock_err
        if conf.FEATURES['skip_lock_err']:
            log.i('skip lock file \"' + lock_file + '\" ')
            return	# NOTE with no Error
        log.e('can not get lock \"' + lock_file + '\", ' + str(e))
        if conf.FEATURES['check_lock_file']:
            log.i('if you are sure that no pvdl instance is operating this directory, you can remove the lock file ')
            er = err.ConfigError('check_lock_file', lock_file)
            raise er from e
        else:	# just ignore it
            log.d('disabled feature check_lock_file ')
    # do with lock
    try:
        return f()
    finally:
        # NOTE close check_log file
        if conf.check_log_file != None:
            try:
                conf.check_log_file.close()
            except Exception as e:
                log.w('can not close check_log file \"' + str(conf.check_log_file_path) + '\", ' + str(e) + ' ')
        try:	# close lock file
            os.close(lock_fd)
        except Exception as e:	# ignore close Error
            log.w('can not close lock file [' + str(lock_fd) + '] \"' + lock_file + '\", ' + str(e))
        # NOTE check keep_lock_file
        if conf.keep_lock_file:
            log.i('keep lock file \"' + lock_file + '\" ')
            return	# NOTE not remove lock file
        try:	# remove lock file
            os.remove(lock_file)
        except Exception as e:	# ignore remove Error
            log.w('can not remove lock file \"' + lock_file + '\", ' + str(e))
    # end _do_in_lock


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

# NOTE these works is protected by the lock file
def _do_with_lock(task_info, pvinfo):
    _create_check_log(task_info)
    
    parse.create_log_file(task_info, pvinfo)	# write log file
    _print_task_info(task_info)
    # do some checks before start download
    _check_disk_space(task_info)
    # download part files
    _do_download(task_info)
    merge.merge(task_info)	# merge video part files
    _auto_remove_tmp_part_files(task_info)	# check auto_remove_tmp_part_files

def _create_check_log(task_info):
    # TODO
    log.w('entry._create_check_log() not finished ')

def _print_task_info(task_info):
    merged_path = b.pjoin(task_info['path']['base_path'], task_info['path']['merged_file'])
    ui.entry_print_create_task(task_info['video']['hd'], task_info['title'], task_info['path']['log_path'], merged_path)

def _check_disk_space(task_info):
    if not conf.FEATURES['check_disk_space']:
        return
    # TODO do check
    log.w('entry._check_disk_space() not finished ')

def _check_keep_lock(task_info):
    if not conf.FEATURES['keep_lock_file']:
        return
    # NOTE no more checks here now, not strict check like auto_remove_tmp_part_files
    conf.keep_lock_file = True	# NOTE just set flag here


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

def _auto_remove_tmp_part_files(task_info):
    if not conf.FEATURES['auto_remove_tmp_part_files']:
        return
    # TODO more check on checks' status
    # check required features
    if not conf.FEATURES['check_merged_time']:
        log.e('disabled feature auto_remove_tmp_files. To enable this, feature check_merged_time must be enabled ')
        return
    if not conf.FEATURES['merge_single_file']:
        log.e('disabled feature auto_remove_tmp_files. To enable this, feature merge_single_file must be enabled ')
        return
    # TODO do remove
    log.w('entry._auto_remove_tmp_part_files() not finished ')

# end entry.py


