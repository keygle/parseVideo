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

import os, sys
import time
import functools
import shutil

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
            log.i(lan.e_task_retry(retry_info))
        try:
            _do_can_retry()
            # print retry OK info
            if retry_count > 0:
                log.o(lan.e_retry_ok(retry_info))
            break	# no more retry
        except err.RetryableError as e:	# ignore this Error
            # ERROR log
            if retry_count > 0:
                log.e(lan.e_retry_err(retry_info))
            else:
                log.e(lan.e_err_task())
            # update retry count
            retry_count += 1
            # NOTE sleep before retry
            if check_should_retry():
                log.i(lan.e_wait_retry(conf.set_retry_wait))
                time.sleep(conf.set_retry_wait)
        except Exception:
            raise	# not process other Errors
    # end entry.start()

# NOTE this works can be retry
def _do_can_retry():
    # TODO support parse_once
    
    # NOTE check parse_twice_enbale_more
    enable_more = conf.FEATURES['parse_twice_enable_more']
    if not enable_more:
        log.d(lan.e_d_disable_parse_twice_enable_more())
    # do first parse to get video formats
    pvinfo = parse.parse(enable_more=enable_more)
    ui.entry_print_pvinfo(pvinfo)
    # select hd
    hd = _select_hd(pvinfo)
    
    # INFO log
    log.i(lan.e_second_parse())
    # check parse_twice_enable_more again, to input more info
    more_info = None
    if enable_more:
        more_info = pvinfo
    pvinfo = parse.parse(hd=hd, pvinfo=more_info)
    # create task
    task_info = parse.create_task(pvinfo, hd)
    
    tmp_path = task_info['path']['tmp_path']
    lock_file = task_info['path']['lock_file']
    lock_path = b.pjoin(tmp_path, lock_file)
    task_info['path']['lock_path'] = lock_path	# NOTE save lock_path here
    # NOTE try to create tmp_path
    try:
        if not os.path.isdir(tmp_path):
            os.makedirs(tmp_path)
    except Exception as e:
        log.e(lan.e_err_mk_tmp_dir(tmp_path))
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
        log.d(lan.e_got_lock(lock_file))
    except Exception as e:	# get lock failed
        # check skip_lock_err
        if conf.FEATURES['skip_lock_err']:
            log.i(lan.e_skip_lock(lock_file))
            return	# NOTE with no Error
        log.e(lan.e_err_get_lock(lock_file, e))
        if conf.FEATURES['check_lock_file']:
            log.i(lan.e_i_rm_lock())
            er = err.ConfigError('check_lock_file', lock_file)
            raise er from e
        else:	# just ignore it
            log.d(lan.e_d_disable_check_lock_file())
    # NOTE reset keep_lock file to fix list download BUG
    conf.keep_lock_file = False
    # do with lock
    try:
        return f()
    finally:
        # NOTE close check_log file
        if conf.check_log_file != None:
            try:
                # NOTE write close info
                log.d('normal closing check_log file ', add_check_log_prefix=True, fix_check_log_file=True)
                conf.check_log_file.close()
            except Exception as e:
                log.w(lan.e_err_close_check_log(conf.check_log_file_path, e))
            finally:	# NOTE reset check_log file after try close it
                conf.check_log_file = None
        try:	# close lock file
            os.close(lock_fd)
        except Exception as e:	# ignore close Error
            log.w(lan.e_err_close_lock_file(lock_fd, lock_file, e))
        # NOTE check keep_lock_file
        if conf.keep_lock_file:
            log.i(lan.e_keep_lock_file(lock_file))
            return	# NOTE not remove lock file
        try:	# remove lock file
            os.remove(lock_file)
        except Exception as e:	# ignore remove Error
            log.w(lan.e_err_rm_lock_file(lock_file, e))
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
        log.w(lan.e_err_select_hd(b.number(conf.select_hd)))
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
    log.w(lan.e_err_select_hd_range(hdr))
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
    _check_keep_lock(task_info)	# NOTE check keep_lock_file here

def _create_check_log(task_info):
    # gen check_log file path
    tmp_path = task_info['path']['tmp_path']
    check_log_file = task_info['path']['check_log']
    check_log_path = b.pjoin(tmp_path, check_log_file)
    conf.check_log_file_path = check_log_path
    # open check log file
    try:	# NOTE open with append blob mode
        conf.check_log_file = open(conf.check_log_file_path, 'ab')
    except Exception as e:
        log.e(lan.e_err_open_check_log(conf.check_log_file_path))
        er = err.ConfigError('open check_log file', conf.check_log_file_path)
        raise er from e
    f = conf.check_log_file
    # write more info to check_log file
    def p(t):	# DEBUG log to fix check_log file info
        log.d(t, add_check_log_prefix=True, fix_check_log_file=True)
    # add \n for better print
    f.write(b'\n\n')
    # create check_log file info
    p('[fix check_log] create check_log file \"' + check_log_path + '\" ')
    # print program info
    args = sys.argv
    pvdl_version = conf.pvdl_version
    p('[fix check_log] pvdl_version ' + str(pvdl_version) + ' ---> args ' + str(args) + ' ')
    # add lock file info
    p('[fix check_log] lock file \"' + task_info['path']['lock_path'] + '\" ')
    # create check_log file and fix check_log info, done
    log.d(lan.e_create_check_log(check_log_path))


def _print_task_info(task_info):
    merged_path = b.pjoin(task_info['path']['base_path'], task_info['path']['merged_file'])
    ui.entry_print_create_task(task_info['video']['hd'], task_info['title'], task_info['path']['log_path'], merged_path)

def _check_disk_space(task_info):
    if not conf.FEATURES['check_disk_space']:
        log.d(lan.e_d_disable_check_disk_space())
        return
    # get tmp path
    tmp_path = task_info['path']['tmp_path']
    info = shutil.disk_usage(tmp_path)
    free_byte = info.free
    free_size = b.byte_to_size(free_byte)
    # NOTE need to get size_byte info first
    dl_byte = task_info['video'].get('size_byte', -1)
    if dl_byte <= 0:
        log.w(lan.e_err_check_disk_space_no_info(free_size))
        return
    # check and give result
    needed_byte = dl_byte * conf.disk_space_needed_k
    needed_size = b.byte_to_size(needed_byte)
    if needed_byte < free_byte:
        log.o(lan.e_pass_check_disk_space(needed_size, free_size))
        return	# check pass
    # disk space not enough
    log.e(lan.e_no_enough_disk_space(needed_size, free_size))
    raise err.ConfigError('check_disk_space', needed_size, free_size)

def _check_keep_lock(task_info):
    if not conf.FEATURES['keep_lock_file']:
        return
    # NOTE no more checks here now, not strict check like auto_remove_tmp_part_files
    conf.keep_lock_file = True	# NOTE just set flag here


## main download works

def _do_download(task_info):
    # NOTE task_info video count info fixed before download
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
        log.e(lan.e_err_dl_part_files(count_err, count), add_check_log_prefix=True)
        raise err.DownloadError('part file', count_err, count)
    # download OK
    log.o(lan.e_ok_dl_part_files(count_ok, count), add_check_log_prefix=True)

def _auto_remove_tmp_part_files(task_info):
    if not conf.FEATURES['auto_remove_tmp_part_files']:
        return
    # do needed checks to pass
    
    # check enabled features
    need_enable_feature_list = [
        'fix_size', 
        'check_log_file', 
        'check_lock_file', 
        'check_file_size', 
        'check_file_md5', 
        'check_merged_size', 
        'check_merged_time', 
        'merge_single_file', 
    ]
    for f in need_enable_feature_list:
        if not conf.FEATURES[f]:
            log.e(lan.e_err_auto_remove_tmp_part_feature_disable(f))
            return	# check failed
    # check skip checks
    can_not_skip_check_list = [
        'check_file_size', 
        'check_merged_size', 
        'check_merged_time', 
    ]
    for c in can_not_skip_check_list:
        if conf.skip_check_list[c]:
            log.e(lan.e_err_auto_remove_tmp_part_pass_check(c))
            return	# check failed
    # all checks passed, do auto remove
    f = task_info['video']['file']
    log.w(lan.e_w_before_auto_remove_tmp_part_files(len(f)))
    for i in f:
        p = i['path']
        try:
            log.d(lan.e_d_remove_tmp_part_file(p))
            os.remove(p)
        except Exception as e:	# ignore remove Error
            log.e(lan.e_err_rm_tmp_part(fpath, e))
    # auto remove done


# end entry.py


