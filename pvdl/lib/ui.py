# ui.py, parse_video/pvdl/lib/

import math
from colored import fg, bg, attr

from . import b, log
from . import make_title

# global styles
_reset = attr('reset')
_bold = attr('bold')

_white = fg('white')
_grey = fg('grey_50')
_blue = fg('blue')
_light_blue = fg('light_blue')
_yellow = fg('yellow')
_light_yellow = fg('light_yellow')
_red = fg('red')
_light_red = fg('light_red')


# ui print functions

## entry.py

def entry_print_pvinfo(pvinfo):
    labels = make_title.gen_labels(pvinfo)	# video formats labels
    # [ OK ] log here
    log.o('got ' + str(len(labels)) + ' video formats ')
    for i in range(len(labels) -1, -1, -1):	# NOTE print labels reverse
        log.p(labels[i])
    common_title = make_title.gen_common_title(pvinfo)
    # print video name (title)
    t = _blue + 'video ' + _light_blue + _bold + common_title + _reset + ' '
    log.p(t)

def entry_print_create_task(hd, title, log_path, merged_path):
    # TODO maybe improve output style here
    t = 'select hd ' + str(hd) + ', create_task \"' + title + '\" '
    log.o(t, add_check_log_prefix=True)
    log.d('log file \"' + log_path + '\" ')
    log.i('output file \"' + merged_path + '\" ')

def entry_print_start_download(count, size, time):
    size = b.byte_to_size(size)
    time = b.second_to_time(time)
    t = 'start download ' + str(count) + ' files, ' + size + ' ' + time + ' '
    log.i(t, add_check_log_prefix=True)

def entry_print_before_download(i, count, part_name, size, time):
    size = b.byte_to_size(size, flag_add_grey=True)
    time = b.second_to_time(time)
    log.p('', add_check_log_prefix=True)	# NOTE for better print
    t = ' ' + _yellow + str(i + 1) + _grey + '/' + str(count) + ' '
    t += _white + 'download ' + _light_yellow + part_name + _grey + ', '
    t += _blue + size + ' ' + _grey + time + ' '
    log.r(t, add_check_log_prefix=True)

def entry_print_download_status(count_err, count_ok, done_size, all_size, done_time, all_time, rest_size, rest_time):
    done_per = (done_size / all_size) * 1e2
    if done_size == all_size:
        done_per = '100'
    else:
        done_per = str(math.floor(done_per * 1e1) / 1e1)
    if count_err > 0:
        err_info = _light_red + str(count_err)
    else:
        err_info = _grey + str(count_err)
    done_size = b.byte_to_size(done_size, flag_add_grey=True)
    all_size = b.byte_to_size(all_size, flag_add_grey=True)
    done_time = b.second_to_time(done_time)
    all_time = b.second_to_time(all_time)
    rest_time = b.second_to_time(rest_time)
    
    t = ' ' + _light_yellow + done_per + _yellow + ' % '
    t += _grey + '[ok ' + _yellow + str(count_ok) + _grey + ' err ' + err_info + _grey + '] '
    t += _white + done_size + _grey + '/' + all_size + ', ' + done_time + '/' + all_time + '; rest '
    if rest_size > 0:
        rest_size = b.byte_to_size(rest_size, flag_add_grey=True)
        t += _yellow + rest_size
    else:
        t += '0'
    t += ' ' + _grey + rest_time + ' '
    log.r(t, add_check_log_prefix=True)

# TODO maybe clean check print code

## dl_worker.py

def dl_worker_print_skip_part_file(err_s, err_k, er, part_name, local_size):
    err_info = make_err_size_info(err_s, err_k, er)
    local_size = b.byte_to_size(local_size, flag_add_grey=True)
    t = _light_blue + 'skip' + _grey + ' \"' + part_name + '\", ' + local_size
    t += ' err ' + _blue + err_info + ' '
    log.o(t, add_check_log_prefix=True)

def dl_worker_print_check_file_size_error(err_s, err_k, part_name, local_size):
    err_info = b.byte_to_size(err_s) + ' ' + str(err_k) + ' %'
    local_size = b.byte_to_size(local_size)
    # ERROR log
    t = 'check part file size failed: \"' + f['_part_name'] + '\", size ' + local_size
    t += ' err ' + err_info + ' '
    log.e(t, add_check_log_prefix=True)

def dl_worker_print_check_file_size_pass(err_s, err_k, er, part_name, local_size):
    err_info = make_err_size_info(err_s, err_k, er)
    local_size = b.byte_to_size(local_size, flag_add_grey=True)
    # [ OK ] log
    t = 'check part file size pass' + _grey + ': \"' + part_name + '\", size '
    t += _white + local_size + _grey + ' err ' + _blue + err_info + ' '
    log.o(t, add_check_log_prefix=True)

## merge.py

def merge_print_check_merged_size_error(err_s, err_k, merged_path, local_size):
    err_info = b.byte_to_size(err_s) + ' ' + str(err_k) + ' %'
    local_size = b.byte_to_size(local_size)
    # ERROR log
    t = 'check merged file size failed: \"' + merged_path + '\", size ' + local_size
    t += ' err ' + err_info + ' '
    log.e(t, add_check_log_prefix=True)

def merge_print_check_merged_size_pass(err_s, err_k, er, merged_name, local_size):
    err_info = make_err_size_info(err_s, err_k, er)
    local_size = b.byte_to_size(local_size, flag_add_grey=True)
    # [ OK ] log
    t = 'check merged file size pass' + _grey + ': \"' + merged_name + '\", size '
    t += _white + local_size + _grey + ' err ' + _blue + err_info + ' '
    log.o(t, add_check_log_prefix=True)

def merge_print_check_merged_time_error(err_s, err_k, merged_path, local_time):
    err_info = b.second_to_time(err_s) + ' ' + str(err_k) + ' %'
    local_time = b.second_to_time(local_time)
    # ERROR log
    t = 'check merged file time_s failed: \"' + merged_path + '\", time_s ' + local_time
    t += ' err ' + err_info + ' '
    log.e(t, add_check_log_prefix=True)

def merge_print_check_merged_time_pass(err_s, err_k, er, merged_name, local_time):
    if er:
        err_info = b.second_to_time(err_s) + ' ' + str(err_k) + ' %'
    else:
        err_info = _grey + '0'
    local_time = b.second_to_time(local_time)
    # [ OK ]  log
    t = 'check merged file time_s pass' + _grey + ': \"' + merged_name + '\", time_s '
    t += _white + local_time + _grey + ' err ' + _blue + err_info + ' '
    log.o(t, add_check_log_prefix=True)

## error checks

def make_err_size_info(err_s, err_k, er):
    if er:
        err_info = b.byte_to_size(err_s, flag_add_grey=True) + ' ' + str(err_k) + ' %'
    else:
        err_info = _grey + '0'
    return err_info


# end ui.py


