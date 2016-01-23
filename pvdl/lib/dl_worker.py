# dl_worker.py, parse_video/pvdl/lib/

import os

from . import err, b, conf, log
from . import call_sub, ui

# download only one file, return True if download succeed
def dl_one_file(f):
    # checks before download
    if _check_remote_size(f):
        return False	# check failed
    if _check_local_size(f):
        return True	# skip this file
    # do download
    try:
        _do_dl(f)
    except (err.ExitCodeError, err.CheckError) as e:
        log.e('download part file \"' + f['_part_name'] + '\" failed ')
        return False
    except err.PvdlError:
        raise
    except Exception as e:
        log.e('download part file, unknow error ')
        er = err.UnknowError('download part file', f)
        raise er from e
    # checks after download
    if _check_file_size(f):
        return False
    if _check_file_md5(f):
        return False
    return True	# download OK

def _do_dl(f):
    # TODO support more dl_workers, not only wget
    _dl_wget(f)

# return True if check failed
def _check_remote_size(f):
    if not conf.FEATURES['check_remote_size']:
        return
    # TODO do check
    log.w('dl_worker._check_remote_size() not finished ')


# return True to skip file
def _check_local_size(f):
    if not conf.FEATURES['check_local_size']:
        return False
    # TODO check permission
    # check file exists
    if not os.path.isfile(f['path']):
        return False	# file not exist
    # get local file info
    s = os.stat(f['path'])
    local_size = s.st_size
    # NOTE check falied if no f['size'] info
    if (not 'size' in f) or (f['size'] <= 0):
        log.d('local file size ' + b.byte_to_size(local_size) + ' ')
        log.w('can not check_local_size, no file size info ')
        return False	# not skip
    # check size
    err_s, err_k, er, err_u = b.check_size(local_size, f['size'], b.CHECK_SIZE_MB)
    if er:
        if (abs(err_u) >= conf.CHECK_ERR_K['local_size_mb']) or (abs(err_k) >= conf.CHECK_ERR_K['local_size']):
            # check skip_local_larger_file
            if not conf.FEATURES['skip_local_larger_file']:
                return False	# not skip
            log.w('enabled feature skip_local_larger_file ')
    ui.dl_worker_print_skip_part_file(err_s, err_k, er, f['_part_name'], local_size)
    return True

# return True if check failed
def _check_file_size(f):
    if not conf.FEATURES['check_file_size']:
        log.d('disabled feature check_file_size ')
        return False
    # get file info
    try:
        s = os.stat(f['path'])
    except Exception as e:
        log.e('can not check_file_size \"' + f['_part_name'] + '\", ' + str(e))
        return True	# NOTE not raise here
    local_size = s.st_size
    # NOTE check no f['size'] info
    if (not 'size' in f) or (f['size'] <= 0):
        log.d('local file_size ' + b.byte_to_size(local_size) + ' ')
        log.w('can not check_file_size, no file size info ')
        return
    # check size
    err_s, err_k, er, err_u = b.check_size(local_size, f['size'], b.CHECK_SIZE_MB)
    if er:
        if (abs(err_u) >= conf.CHECK_ERR_K['file_size_mb']) or (abs(err_k) >= conf.CHECK_ERR_K['file_size']):
            ui.dl_worker_print_check_file_size_error(err_s, err_k, f['_part_name'], local_size)
            return True
    ui.dl_worker_print_check_file_size_pass(err_s, err_k, er, f['_part_name'], local_size)
    return False


# return True if check failed
def _check_file_md5(f):
    if not conf.FEATURES['check_file_md5']:
        return False
    # check md5 info
    if not 'checksum' in f:
        log.d('no checksum info for this file ')
        return False
    if not 'md5' in f['checksum']:
        log.d('no checksum.md5 info for this file ')
        return False
    ok_md5 = f['checksum']['md5']
    # INFO log
    log.i('checking checksum.md5 for file \"' + f['_part_name'] + '\" ')
    try:	# check file md5
        file_md5 = b.md5sum(f['path'])
    except Exception as e:
        log.e('can not check md5, ' + str(e))
        # TODO print Error info here
        return True	# check failed
    # check md5 match
    if file_md5 != ok_md5:
        log.e('checksum.md5 failed, file ' + file_md5 + ', OK ' + ok_md5 + ' ')
        return True
    log.o('checksum.md5 OK ' + ok_md5 + ' ')
    return False


# download with wget
def _dl_wget(f):
    # TODO support more http headers
    # gen wget args, NOTE enable -c by default
    arg = ['-c', '-O', f['path'], f['url']]
    # just call wget to do download
    call_sub.call_wget(arg)

# TODO support more dl_worker

# end dl_worker.py


