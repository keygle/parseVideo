# merge.py, parse_video/pvdl/lib/, merge video part files with ffmpeg

import os

from . import err, conf, log
from . import b
from . import call_sub

def merge(task_info):
    # checks before merge
    _check_force_merge(task_info)
    # INFO log
    log.i('call ffmpeg to merge part files ')
    # TODO Error process
    _do_merge(task_info)
    # some checks after merge
    _check_merged_size(task_info)
    _check_merged_time(task_info)
    # merged OK
    log.o('merge video succeed ')

def _do_merge(task_info):
    # gen ffmpeg_list file and write it
    raw_text = _gen_ffmpeg_merge_list(task_info)
    blob = raw_text.encode('utf-8')	# NOTE utf-8 encoding may got Error
    list_file = task_info['path']['list_path']
    try:
        with open(list_file, 'wb') as f:
            f.write(blob)
    except Exception as e:
        log.e('can not write ffmpeg list file \"' + list_file + '\" ')
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
    merged_path = b.pjoin(base_path, merged_path)
    task_info['path']['list_path'] = list_path
    task_info['path']['merged_path'] = merged_path
    # TODO check permission
    
    # check final file exists
    if os.path.isfile(merged_path) and (not conf.FEATURES['force_merge']):
        log.e('can not output merged file \"' + merged_path + '\", already exists ')
        raise err.CheckError('output merged_file', merged_path)
    # TODO do force merge, remove file
    log.w('merge._check_force_merge() not finished ')

def _gen_ffmpeg_merge_list(task_info):
    # TODO maybe need to fix path
    out = ''
    for f in task_info['video']['file']:
        one = 'file \'' + f['path'] + '\'\n'
        out += one
    return out


# TODO
def _fix_ffmpeg_args():
    pass

def _check_merged_size(task_info):
    if not conf.FEATURES['check_merged_size']:
        return
    # TODO do check
    log.w('merge._check_merged_size() not finished ')

def _check_merged_time(task_info):
    if not conf.FEATURES['check_merged_time']:
        return
    # TODO do check
    log.w('merge._check_merged_time() not finished ')


# end merge.py


