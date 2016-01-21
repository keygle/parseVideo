# parse.py, parse_video/pvdl/lib/

import os
import json

from . import err, b, conf, log
from . import call_sub, make_title


# TODO support enable_more
def parse(hd=None, enable_more=False):
    raw_url = conf.raw_url
    # INFO log
    if hd == None:
        log.i('first parse, call parse_video to parse URL \"' + raw_url + '\" ')
    pvinfo, raw_text = _do_parse(raw_url, hd=hd, enable_more=enable_more)
    # check print parse_video output
    if conf.FEATURES['print_parse_video_output']:
        print(raw_text)	# print raw output
    else:	# DEBUG log
        log.d('disabled feature print_parse_video_output ')
    # TODO check parse_video output mark_uuid and port_version
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


# NOTE do fix_size before create_task
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
    # NOTE check --title-no
    if conf.title_no != None:
        log.i('fix title_no to ' + str(conf.title_no) + ' ')
        task_info['info']['title_no'] = conf.title_no
    # TODO support fix_title_no
    # gen task_title
    title = make_title.gen_title(task_info)
    # NOTE check --title-suffix
    if conf.title_suffix != None:
        log.d('add title_suffix \"' + conf.title_suffix + '\" ')
        title += '.' + conf.title_suffix
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
    pvinfo = b.json_clone(pvinfo)
    # NOTE add task_info in pvinfo by default to write log file, will be used for parse_video --more
    pvinfo['_pvdl_task_info'] = task_info
    # create json blob, with utf-8 encode
    text = json.dumps(pvinfo, indent=4, sort_keys=True, ensure_ascii=False)
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
        log.d('disabled feature check_log_file ')
        return
    # check log file exist
    log_path = b.pjoin(task_info['path']['tmp_path'], task_info['path']['log_file'])
    if not os.path.isfile(log_path):
        log.d('log file not exist, \"' + log_path + '\" ')
        return
    # read log file
    try:
        with open(log_path, 'rb') as f:
            blob = f.read()
    except Exception as e:
        log.e('can not read log file \"' + log_path + '\" ')
        er = err.ConfigError('read log_file', log_path)
        raise er from e
    # parse json
    try:
        text = blob.decode('utf-8')
        log_info = json.loads(text)
    except Exception as e:
        # TODO print more error info
        log.w('can not parse json text of log file \"' + log_path + '\", ' + str(e))
    # do check
    try:	# NOTE get task_info from pvdl log file
        old, now = log_info['_pvdl_task_info'], task_info
        # base check
        def print_check_err(value, new, old):	# base check error print function
            t = 'check log failed, new ' + value + ' ' + str(new) + ' != old ' + str(old) + ' '
            log.e(t)
            return err.CheckError('check log_file', value, old, new)
        now_v, old_v = now['video'], old['video']
        # check hd match
        now_hd, old_hd = now_v['hd'], old_v['hd']
        if now_hd != old_hd:
            raise print_check_err('hd', now_hd, old_hd)
        # check format match
        now_format, old_format = now_v['format'], old_v['format']
        if now_format != old_format:
            raise print_check_err('format', now_format, old_format)
        # check part file count
        now_f, old_f = now_v['file'], old_v['file']
        now_count, old_count = len(now_f), len(old_f)
        if now_count != old_count:
            raise print_check_err('count', now_count, old_count)
        # check each part file size, time_s match
        for i in range(now_count):
            f, o = now_f[i], old_f[i]
            now_size, old_size = f['size'], o['size']
            now_time, old_time = f['time_s'], o['time_s']
            t = 'check log failed, part file ' + str(i + 1) + ': '
            if now_size != old_size:
                t += 'new size ' + str(now_size) + ' != old ' + str(old_size) + ' '
                log.e(t)
                raise err.CheckError('check log_file part_file', i, 'size', old_size, now_size)
            if now_time != old_time:
                t += 'new time_s ' + str(now_time) + ' != old ' + str(old_time) + ' '
                log.e(t)
                raise err.CheckError('check log_file part_file', i, 'time_s', old_time, now_time)
            # check checksum
            if not 'checksum' in o:
                continue	# no checksum info
            if not 'checksum' in f:
                t += 'no checksum in new file info '
                log.e(t)
                raise err.CheckError('check log_file part_file', i, 'no checksum', o['checksum'])
            now_checksum, old_checksum = f['checksum'], o['checksum']
            if now_checksum != old_checksum:
                t += 'new checksum ' + str(now_checksum) + ' != old ' + str(old_checksum) + ' '
                log.e(t)
                raise err.CheckError('check log_file part_file', i, 'checksum', old_checksum, now_checksum)
        ## strict check (more checks)
        if conf.FEATURES['check_log_file_strict']:
            log.i('enabled feature check_log_file_strict ')
            def print_strict_err(value, new, old):
                t = 'strict check log failed, new ' + value + ' ' + str(new) + ' != old ' + str(old) + ' '
                log.e(t)
                return err.CheckError('check log_file strict', value, old, new)
            # check title match
            now_title, old_title = now['title'], old['title']
            if now_title != old_title:
                raise print_strict_err('title', '[' + now_title + ']', '[' + old_title + ']')
            now_info, old_info = now['info'], old['info']
            # check extractor, method match
            now_extractor, old_extractor = now['extractor'], old['extractor']
            now_method, old_method = now['method'], old['method']
            if now_extractor != old_extractor:
                raise print_strict_err('extractor', '[' + now_extractor + ']', '[' + old_extractor + ']')
            if now_method != old_method:
                raise print_strict_err('method', '[' + now_method + ']', '[' + old_method + ']')
            # check URL match
            now_url, old_url = now_info['url'], old_info['url']
            if now_url != old_url:
                raise print_strict_err('url', '\"' + now_url + '\"', '\"' + old_url + '\"')
            # check size_px match
            now_size_px, old_size_px = now_v['size_px'], old_v['size_px']
            if now_size_px != old_size_px:
                raise print_strict_err('size_px', now_size_px, old_size_px)
            # TODO check each part file download type
            # TODO maybe add more strict check items
        # end strict check
    except err.CheckError:
        raise
    except Exception as e:
        log.w('bad log file \"' + log_path + '\", ' + str(e))
        # TODO print more error info
    log.o('check log file pass ')


# end parse.py


