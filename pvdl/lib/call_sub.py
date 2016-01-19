# call_sub.py, parse_video/pvdl/lib/

import os, sys
import json
import subprocess

from . import err, conf, log
from . import b


def call_parsev(args):
    py_bin = sys.executable
    pv_bin = _make_bin_path(conf.SUB_BIN['parsev'])
    a = [py_bin, pv_bin] + args
    # DEBUG log
    log.d('call parse_video to parse, with args ' + str(args) + ' ')
    
    # call parse_video to do parse
    PIPE = subprocess.PIPE
    try:
        p = subprocess.run(a, stdout=PIPE)
    except Exception as e:
        log.e('can not execute parse_video ')
        er = err.CallError('parse_video', py_bin, pv_bin, args)
        raise er from e
    # check exit code
    exit_code = p.returncode
    if exit_code != 0:
        log.e('parse failed, parse_video return ' + str(exit_code) + ' ')
        raise err.ExitCodeError('parse_video', exit_code, args)
    # parse stdout
    try:
        stdout = p.stdout.decode('utf-8')
    except Exception as e:
        log.e('parse failed, decode parse_video stdout to text with utf-8 failed ')
        er = err.DecodingError('parse_video', 'stdout', args)
        er.blob = p.stdout
        raise er from e
    # parse parse_video output json
    try:
        out = json.loads(stdout)
    except Exception as e:
        log.e('parse failed, parse parse_video output json text failed ')
        er = err.ParseJSONError('parse_video', stdout, args)
        raise er from e
    return out, stdout	# everything OK

def call_wget(args):
    wget_bin = _make_bin_path(conf.SUB_BIN['wget'])
    _call_and_check(wget_bin, args, name='wget', action='download')

def call_ffmpeg(args):
    ffmpeg_bin = _make_bin_path(conf.SUB_BIN['ffmpeg'])
    _call_and_check(ffmpeg_bin, args, name='ffmpeg', action='merge')

def call_mediainfo(args):
    mediainfo_bin = _make_bin_path(conf.SUB_BIN['mediainfo'])
    _call_and_check(mediainfo_bin, args, name='mediainfo', action='get video file info')

def call_sub_downloader(sub, args):
    pass	# TODO

# gen bin path from config
def _make_bin_path(raw, check=True):
    # check startswith ./ or ../
    if (raw.startswith('./')) or (raw.startswith('../')):
        out = b.pjoin(b.get_root_path(), raw)
    else:
        out = raw
    # check bin file exists
    if check and (not os.path.isfile(out)):
        log.e('bin file not exist, \"' + out + '\" ')
        raise err.ConfigError('bin file not exist', out)
    return out

# call and check exit_code
def _call_and_check(call_bin, args, name='', action='', ok_code=0):
    # DEBUG log
    log.d('call ' + name + ' to ' + action + ', with args ' + str(args) + ' ')
    try:
        p = subprocess.run([call_bin, args])
    except Exception as e:
        log.e('can not execute ' + name + ' ')
        er = err.CallError(name, call_bin, args)
        raise er from e
    # check exit code
    exit_code = p.returncode
    if exit_code != ok:
        log.e(action + ' failed, ' + name + ' return ' + str(exit_code) + ' ')
        raise err.ExitCodeError(name, exit_code)
    # everything OK


# end call_sub.py


