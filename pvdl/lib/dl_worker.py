# dl_worker.py, parse_video/pvdl/lib/

import os
import math

from . import err, conf, log
from . import b
from . import call_sub

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
    
    # TODO support no f['size'] value, or f['size'] == 0
    
    # TODO may be clean check_size code
    # check size
    err = local_size - f['size']
    err_k = (err / f['size']) * 1e2	# %
    if local_size != f['size']:
        if (math.abs(err / pow(1024, 2)) >= conf.CHECK_ERR_K['local_size_mb']) or (math.abs(err_k) >= conf.CHECK_ERR_K['local_size']):
            return False	# not skip
        err_info = b.byte_to_size(err) + ' ' + str(err_k) + ' % '
    else:
        err_info = '0'
    # log skip info
    log.i('skip local file \"' + f['_part_name'] + '\", size ' + b.byte_to_size(local_size) + ' err ' + err_info + ' ')
    return True

# return True if check failed
def _check_file_size(f):
    if not conf.FEATURES['check_file_size']:
        return False
    # get file info
    try:
        s = os.stat(f['path'])
    except Exception as e:
        log.e('can not check_file_size \"' + f['_part_name'] + '\", ' + str(e))
        return True	# NOTE not raise here
    local_size = s.st_size
    # TODO support no f['size'] or f['size'] == 0
    # TODO may clean check err code here
    # make err
    err = local_size - f['size']
    err_k = (err / f['size']) * 1e2	# %
    if local_size != f['size']:
        err_info = b.byte_to_size(err) + ' ' + str(err_k) + ' % '
        if (math.abs(err / pow(1024, 2)) >= conf.CHECK) or ():
            # ERROR log
            log.e('check part file size failed: \"' + f['_part_name'] + '\", size ' + b.byte_to_size(local_size) + ' err ' + err_info + ' ')
            return True
    else:
        err_info = '0'
    # log check pass
    log.o('check part file size pass: \"' + f['_part_name'] + '\", size ' + b.byte_to_size(local_size) + ' err ' + err_info + ' ')
    return False


# return True if check failed
def _check_file_md5(f):
    if not conf.FEATURES['check_file_md5']:
        return False
    # TODO do check
    log.w('dl_worker._check_file_md5() not finished ')

# download with wget
def _dl_wget(f):
    # TODO support more http headers
    # gen wget args, NOTE enable -c by default
    arg = ['-c', '-O', f['path'], f['url']]
    # just call wget to do download
    call_sub.call_wget(arg)

# TODO support more dl_worker

# end dl_worker.py


