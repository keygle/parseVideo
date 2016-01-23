# merge.py, parse_video/pvdl/lib/, merge video part files with ffmpeg

import os

from . import err, b, conf, log
from . import call_sub, ui


def merge(task_info):
    # checks before merge
    _check_force_merge(task_info)
    # INFO log
    log.i('call ffmpeg to merge part files ', add_check_log_prefix=True)
    # TODO Error process
    _do_merge(task_info)
    # some checks after merge
    _check_merged_size(task_info)
    _check_merged_time(task_info)
    # merged OK
    log.o('merge video succeed ', add_check_log_prefix=True)

def _do_merge(task_info):
    # gen ffmpeg_list file and write it
    raw_text = _gen_ffmpeg_merge_list(task_info)
    blob = raw_text.encode('utf-8')	# NOTE utf-8 encoding may got Error
    list_file = task_info['path']['list_path']
    try:
        with open(list_file, 'wb') as f:
            f.write(blob)
    except Exception as e:
        log.e('can not write ffmpeg list file \"' + list_file + '\" ', add_check_log_prefix=True)
        er = err.ConfigError('write ffmpeg_list_file', list_file)
        raise er from e
    # make ffmpeg args
    merged_file = task_info['path']['merged_path']
    arg = ['-f', 'concat', '-i', list_file, '-c', 'copy', merged_file]
    # TODO fix_ffmpeg_args
    # TODO Error process
    # just call ffmpeg to merge
    call_sub.call_ffmpeg(arg)

def _check_force_merge(task_info):
    base_path = task_info['path']['base_path']
    tmp_path = task_info['path']['tmp_path']
    list_file = task_info['path']['ffmpeg_list']
    merged_file = task_info['path']['merged_file']
    
    list_path = b.pjoin(tmp_path, list_file)
    merged_path = b.pjoin(base_path, merged_file)
    task_info['path']['list_path'] = list_path
    task_info['path']['merged_path'] = merged_path
    # TODO check permission
    # check final file exists
    if not os.path.isfile(merged_path):
        return	# check pass
    if conf.FEATURES['force_merge']:
        # TODO do force merge, remove file
        log.w('merge._check_force_merge() not finished ')
        return
    log.e('can not merge \"' + merged_path + '\", this output file already exists ', add_check_log_prefix=True)
    raise err.CheckError('output merged_file', merged_path)

def _gen_ffmpeg_merge_list(task_info):
    # NOTE should fix path here
    list_file = task_info['path']['list_path']
    from_path = os.path.dirname(list_file)
    out = ''
    for f in task_info['video']['file']:
        # fix path
        rel_path = os.path.relpath(f['path'], from_path)
        one = 'file \'' + rel_path + '\'\n'
        out += one
    return out


# TODO
def _fix_ffmpeg_args():
    pass

def _check_merged_size(task_info):
    if not conf.FEATURES['check_merged_size']:
        log.d('disabled feature check_merged_size ', add_check_log_prefix=True)
        return
    # get file info
    merged_path = task_info['path']['merged_path']
    try:
        s = os.stat(merged_path)
    except Exception as e:
        log.e('can not check_merged_size \"' + merged_path + '\", can not get file info ', add_check_log_prefix=True)
        er = err.CheckError('merged_size', 'stat file', merged_path)
        raise er from e
    local_size = s.st_size
    # NOTE check no video['size_byte'] info
    v = task_info['video']
    if (not 'size_byte' in v) or (v['size_byte'] <= 0):
        log.d('local merged file size ' + b.byte_to_size(local_size) + ' ', add_check_log_prefix=True)
        log.w('can not check_merged_size, no video size_byte info ', add_check_log_prefix=True)
        return
    # check size
    err_s, err_k, er, err_u = b.check_size(local_size, v['size_byte'], b.CHECK_SIZE_MB)
    if er:
        if (abs(err_u) >= conf.CHECK_ERR_K['merged_size_mb']) or (abs(err_k) >= conf.CHECK_ERR_K['merged_size']):
            ui.merge_print_check_merged_size_error(err_s, err_k, merged_path, local_size)
            raise err.CheckError('merged_size', local_size, v['size_byte'], merged_path)
    ui.merge_print_check_merged_size_pass(err_s, err_k, er, task_info['path']['merged_file'], local_size)

def _check_merged_time(task_info):
    if not conf.FEATURES['check_merged_time']:
        return
    # get merged file time_s
    merged_path = task_info['path']['merged_path']
    try:
        local_time = _get_file_time_s(merged_path)
    except Exception as e:
        log.e('can not check_merged_time \"' + merged_path + '\", can not get file time_s ', add_check_log_prefix=True)
        er = err.CheckError('merged_time', 'get time_s', merged_path)
        raise er from e
    # NOTE check no video['time_s'] info
    v = task_info['video']
    if (not 'time_s' in v) or (v['time_s'] <= 0):
        log.d('local merged file time_s ' + b.second_to_time(local_time) + ' ', add_check_log_prefix=True)
        log.w('can to check_merged_time, no video time_s info ', add_check_log_prefix=True)
        return
    # check time
    err_s, err_k, er, err_u = b.check_size(local_time, v['time_s'], 1)	# NOTE unit is second
    if er:
        if (abs(err_u) >= conf.CHECK_ERR_K['merged_time_s']) or (abs(err_k) >= conf.CHECK_ERR_K['merged_time']):
            ui.merge_print_check_merged_time_error(err_s, err_k, merged_path, local_time)
            raise err.CheckError('merged_time', local_time, v['time_s'], merged_path)
    ui.merge_print_check_merged_time_pass(err_s, err_k, er, task_info['path']['merged_file'], local_time)

# TODO check merged size_px
def _get_file_time_s(fpath):
    # make mediainfo args
    arg = ['--full', '--language=raw', fpath]
    # call mediainfo
    stdout = call_sub.call_mediainfo(arg)
    # process lines to get time_s
    line = stdout.splitlines()
    for l in line:
        if not ':' in l:
            continue	# skip this line
        key, value = l.split(':', 1)
        key, value = key.strip(), value.strip()
        # check Duration
        if key == 'Duration':	# NOTE unit of value is ms
            time_s = float(value) / 1e3
            return time_s	# got time_s
    log.e('no Duration info in mediainfo output ', add_check_log_prefix=True)
    raise err.CheckError('merged_time', 'mediainfo output Duration', stdout)


# end merge.py


