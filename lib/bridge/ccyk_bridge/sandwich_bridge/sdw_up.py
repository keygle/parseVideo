# -*- coding: utf-8 -*-
# sdw_up.py, kill_ccyouku, kill_cmodule/sandwich_bridge/, the up side of the sandwich 
# version 0.0.2.0 test201602011930

import os, sys
import json
import subprocess, threading
import random, uuid

# import win_pipe
now_dir = os.path.dirname(__file__)
sys.path.insert(0, now_dir)

import win_pipe
import io_one_line_only as _ioo

# global data
etc = {}
etc['sandwich_bridge_uuid'] = '_a093c7d0-9f80-4c13-9601-745ad486aa14'
etc['this_uuid'] = None
etc['down_path'] = './sdw_down.py'
#etc['sub_pre_args'] = []
etc['adl'] = ['adl']
etc['bridge_core'] = './bin/kcyk.xml'
etc['sub_after_args'] = ['--swf-file']
etc['swf_file'] = './player/player_yknpsv_.swf'

# global instance data
etc['p'] = None	# subprocess object
etc['pipe_name'] = None
etc['dl_pipe'] = None	# download named pipe
etc['up_pipe'] = None	# upload named pipe

# make pipe name
def _make_pipe_name():
    # create a this uuid
    if not etc['this_uuid']:
        etc['this_uuid'] = uuid.uuid4().hex
    # concat the name
    name = ('_').join([etc['sandwich_bridge_uuid'], etc['this_uuid'], str(random.random())])
    return name

# start sub process
def _start_sub(pipe_name, more_args=[]):
    down_path = os.path.normpath(os.path.join(now_dir, etc['down_path']))
    py_bin = sys.executable
    # make sub args
    bridge_arg = ['--pipe-name', pipe_name, '--bridge-host', py_bin, '--bridge-worker', down_path]
    args = etc['adl'] + [etc['bridge_core'], '--'] + bridge_arg + more_args
    
    # FIXME DEBUG here
    print('DEBUG: start sub with ' + str(args) + ' ', file=sys.stderr)
    # just start sub
    p = subprocess.Popen(args, shell=False)
    # start sub done
    return p

# write to sub
def _write_to_sub(info=['']):
    # encode with io_one_line_only
    text = _ioo.encode(info)
    text += '\n'
    blob = text.encode('utf-8')
    # just write it
    etc['up_pipe'].write(blob)

# get sub output
def _get_sub_out():
    line = etc['dl_pipe'].readline()
    text = line.decode('utf-8')
    # TODO error process
    # decode with io_one_line_only
    info = _ioo.decode(text)
    return info

# exports function

# start sub function
def start():
    # TODO check sub exited
    # check started
    if etc['p']:
        return ['error', 'already started']
    # make pipe name
    pipe_name = _make_pipe_name()
    etc['pipe_name'] = pipe_name
    # create named pipe
    dl_pipe = win_pipe.NamedPipeServer(pipe_name)
    etc['dl_pipe'] = dl_pipe
    # FIXME DEBUG here
    # FIXME try to fix swf_file with realpath
    swf_file = etc['swf_file']
    swf_file = os.path.realpath(swf_file)
    
    # start sub process
    p = _start_sub(pipe_name, more_args=(etc['sub_after_args'] + [swf_file]))
    etc['p'] = p
    # accept sub
    try:
        dl_pipe.accept()
    except Exception as e:
        pass	# NOTE just ignore it
    # connect to upload pipe
    up_pipe = win_pipe.open_named_pipe(pipe_name + '_')
    etc['up_pipe'] = up_pipe
    # wait for sub init
    return _get_sub_out()

# call sub functions

# exit
def exit():
    info = ['exit']
    _write_to_sub(info)
    # wait sub to exit
    etc['p'].wait()
    # clean etc
    etc['p'] = None
    # close pipes
    etc['dl_pipe'].close()
    etc['up_pipe'].close()
    # done

# main export functions

def _do_call(name, raw):
    info = ['call', name, raw]
    _write_to_sub(info)
    # get result
    result = _get_sub_out()
    # check result
    if result[0] != 'ret':
        raise Exception('sub return Error ' + str(result) + ' ')
    # done
    return result[1]

def set_size(raw):
    return _do_call('set_size', raw)

def get_size(raw):
    return _do_call('get_size', raw)

def change_size(raw):
    return _do_call('change_size', raw)


# end sdw_up.py


