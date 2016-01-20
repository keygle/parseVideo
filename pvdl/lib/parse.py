# parse.py, parse_video/pvdl/lib/

import os
import json

from . import err, conf, log
from . import b
from . import call_sub, make_title

def parse(hd=None, enable_more=False):
    raw_url = conf.raw_url
    # INFO log
    if hd == None:
        log.i('first parse, call parse_video to parse URL \"' + raw_url + '\" ')
    pvinfo, raw_text = _do_parse(raw_url, hd=hd, enable_more=enable_more)
    # check print parse_video output
    if conf.FEATURES['print_parse_video_output']:
        print(raw_text)	# print raw output
    # check fix_size
    if conf.FEATURES['fix_size']:
        pvinfo = _fix_size(pvinfo)
    conf.pvinfo = pvinfo	# save raw pvinfo
    return pvinfo	# done

def _do_parse(raw_url, hd=None, enable_more=False):
    # make parse_video args
    arg = []
    # check fix_unicode
    if conf.FEATURES['fix_unicode']:
        arg += ['--fix-unicode']	# TODO parse_video now not support this option
    # check hd
    if hd == None:	# parse formats
        arg += ['--min', str(1), '--max', str(0)]
    else:	# parse URLs
        arg += ['--min', str(hd), '--max', str(hd)]
    # check add more raw args
    if len(conf.raw_args) > 0:
        arg += ['--options-overwrite-once'] + conf.raw_args	# TODO parse_video now not support this option
    # check add enable_more
    if enable_more:
        arg = _check_add_enable_more(arg)
    # add raw_url at last
    arg += [raw_url]
    
    # call parse_video to do parse
    try:
        pvinfo, raw_text = call_sub.call_parsev(arg)
    except (err.CallError, err.DecodingError) as e:
        er = err.ConfigError('call', 'parse_video')
        raise er from e
    except err.PvdlError as e:
        log.e('call parse_video to do parse failed ')
        er = err.ParseError('call parse_video', arg)
        raise er from e
    except Exception as e:
        log.e('unknow call parse_video Error ')
        er = err.UnknowError('call', 'parse_video')
        raise er from e
    return pvinfo, raw_text	# OK

def _check_add_enable_more(raw):
    log.w('parse._check_add_enable_more() not finished ')
    # TODO
    return raw

def _fix_size(pvinfo):
    log.w('parse._fix_size() not finished ')
    # TODO
    return pvinfo

def create_task(pvinfo, hd):
    ## create task_info, based on pvinfo
    task_info = b.json_clone(pvinfo)	# deep clone pvinfo object
    # replace video with hd
    v = None
    for vi in task_info['video']:
        if vi['hd'] == hd:
            v = vi
            break
    if v == None:
        raise err.UnknowError('can not select hd from pvinfo', hd, pvinfo)
    task_info['video'] = v
    # gen task_title
    title = make_title.gen_title(task_info)
    task_info['title'] = title
    ## add more to task_info
    task_info['path'] = {}
    # gen base_path, will save final merged file in base_path
    task_info['path']['base_path'] = os.path.normpath(conf.set_output)
    # gen tmp_name and tmp_path
    task_info['path']['tmp_name'] = make_title.gen_tmp_dir_name(title)
    tmp_path = b.pjoin(task_info['path']['base_path'], task_info['path']['tmp_name'])
    task_info['path']['tmp_path'] = tmp_path
    
    # gen log file, lock file, name
    task_info['path']['log_file'] = make_title.gen_log_file_name(title)
    task_info['path']['lock_file'] = make_title.gen_lock_file_name(title)
    # gen each part file name and file path
    ext = task_info['video']['format']
    for i in range(len(task_info['video']['file'])):
        f = task_info['video']['file'][i]
        f['_part_name'] = make_title.gen_part_file_name(title, i + 1, ext)
        f['path'] = b.pjoin(tmp_path, f['_part_name'])	# NOTE gen final part file path here
    # gen merge list, merged file name
    task_info['path']['ffmpeg_list'] = make_title.gen_ffmpeg_list_file_name(title)
    task_info['path']['merged_file'] = make_title.gen_merged_file_name(title, conf.merge_output_format)
    # create task_info done
    _check_log_file(task_info)	# some checks
    
    _write_log_file(pvinfo, task_info)
    return task_info	# end create_task

def _write_log_file(pvinfo, task_info):
    # create log file path
    tmp_path = task_info['path']['tmp_path']
    log_path = b.pjoin(tmp_path, task_info['path']['log_file'])
    task_info['path']['log_path'] = log_path
    
    # clone task_info to prevent modify it
    task_info = b.json_clone(task_info)
    # add pvinfo for DEBUG
    task_info['_pvinfo'] = pvinfo
    # create json blob, with utf-8 encode
    text = json.dumps(task_info, indent=4, sort_keys=True, ensure_ascii=False)
    blob = text.encode('utf-8')
    # NOTE try to create tmp_path
    try:
        if not os.path.isdir(tmp_path):
            os.makedirs(tmp_path)
    except Exception as e:
        log.e('can not create tmp dir \"' + tmp_path + '\" ')
        er = err.ConfigError('create tmp_dir', tmp_path)
        raise er from e
    # NOTE use write-replace to write log file
    tmp_log_file = log_path + '.tmp'
    try:
        with open(tmp_log_file, 'wb') as f:
            f.write(blob)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_log_file, log_path)
    except Exception as e:
        log.e('can not write log file \"' + log_path + '\" (\"' + tmp_log_file + '\") ')
        er = err.ConfigError('write log_file', log_path, tmp_log_file)
        raise er from e

def _check_log_file(task_info):
    if not conf.FEATURES['check_log_file']:
        return
    # TODO do check
    log.w('parse._check_log_file() not finished ')


# end parse.py


