# call_sub.py, parse_video/pvdl/lib/

import os, sys
import json
import subprocess

from . import err, b, conf, log
from . import lan


def call_parsev(args, data=None):
    py_bin = sys.executable
    pv_bin = _make_bin_path(conf.SUB_BIN['parsev'])
    a = [py_bin, pv_bin] + args
    # DEBUG log
    log.d(lan.cs_d_call_pv(args), add_check_log_prefix=True)
    
    # call parse_video to do parse
    PIPE = subprocess.PIPE
    try:	# NOTE wirte data to stdin
        p = subprocess.run(a, stdout=PIPE, input=data)
    except Exception as e:
        log.e(lan.cs_err_can_not_exe('parse_video'), add_check_log_prefix=True)
        er = err.CallError('parse_video', py_bin, pv_bin, args)
        raise er from e
    # check exit code
    exit_code = p.returncode
    if exit_code != 0:
        log.e(lan.cs_err_pv_ret(exit_code), add_check_log_prefix=True)
        raise err.ExitCodeError('parse_video', exit_code, args)
    # parse stdout
    try:
        stdout = p.stdout.decode('utf-8')
    except Exception as e:
        log.e(lan.cs_err_pv_decode_stdout(), add_check_log_prefix=True)
        er = err.DecodingError('parse_video', 'stdout', args)
        er.blob = p.stdout
        raise er from e
    # parse parse_video output json
    try:
        out = json.loads(stdout)
    except Exception as e:
        log.e(lan.cs_err_pv_parse_json(), add_check_log_prefix=True)
        er = err.ParseJSONError('parse_video', stdout, args)
        raise er from e
    return out, stdout	# everything OK

def call_wget(args):
    wget_bin = _make_bin_path(conf.SUB_BIN['wget'])
    _call_and_check(wget_bin, args, name='wget', action='download')

def call_ffmpeg(args):
    ffmpeg_bin = _make_bin_path(conf.SUB_BIN['ffmpeg'])
    _call_and_check(ffmpeg_bin, args, name='ffmpeg', action='merge')

def call_mediainfo(args, ignore_decoding_error=True):
    mediainfo_bin = _make_bin_path(conf.SUB_BIN['mediainfo'])
    a = [mediainfo_bin] + args
    # DEBUG log
    log.d(lan.cs_d_call_mediainfo(args), add_check_log_prefix=True)
    
    # call mediainfo
    PIPE = subprocess.PIPE
    try:
        p = subprocess.run(a, stdout=PIPE)
    except Exception as e:
        log.e(lan.cs_err_can_not_exe('mediainfo'), add_check_log_prefix=True)
        er = err.CallError('mediainfo', mediainfo_bin, args)
        raise er from e
    # check exit code
    exit_code = p.returncode
    if exit_code != 0:
        log.e(lan.cs_err_mediainfo_ret(exit_code), add_check_log_prefix=True)
        raise err.ExitCodeError('mediainfo', exit_code, args)
    # decode stdout, NOTE just with utf-8
    try:
        stdout = p.stdout.decode('utf-8')
    except Exception as e:
        if not ignore_decoding_error:
            log.e(lan.cs_err_mediainfo_decode_stdout(), add_check_log_prefix=True)
            er = err.DecodingError('mediainfo', 'stdout', args)
            er.blob = p.stdout
            raise er from e
        # just ignore decoding Error here
        stdout = p.stdout.decode('utf-8', 'ignore')
    return stdout	# end call mediainfo

def call_sub_downloader(sub, args):
    pass	# TODO

# gen bin path from config
def _make_bin_path(info):
    raw, check = info
    # check startswith ./ or ../
    if (raw.startswith('./')) or (raw.startswith('../')):
        out = b.pjoin(b.get_root_path(), raw)
    else:
        out = raw
    # check bin file exists
    if check and (not os.path.isfile(out)):
        log.e(lan.cs_err_bin_file_gone(out), add_check_log_prefix=True)
        raise err.ConfigError('bin file not exist', out)
    return out

# call and check exit_code
def _call_and_check(call_bin, args, name='', action='', ok_code=0):
    # DEBUG log
    log.d(lan.cs_d_call_to(name, action, args), add_check_log_prefix=True)
    try:
        p = subprocess.run([call_bin] + args)
    except Exception as e:
        log.e(lan.cs_err_can_not_exe(name), add_check_log_prefix=True)
        er = err.CallError(name, call_bin, args)
        raise er from e
    # check exit code
    exit_code = p.returncode
    if exit_code != ok_code:
        log.e(lan.cs_err_action_failed(action, name, exit_code), add_check_log_prefix=True)
        raise err.ExitCodeError(name, exit_code)
    # everything OK


# end call_sub.py


