#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# side_down.py, parse_video/lib/bridge/sandwich_bridge/sandwich_host/
# down_side of sandwich_bridge 2
#
# run side_down.py with:
#	--pipe PIPE
#

import os, sys
import threading
import random, uuid
import json

# NOTE try to import win_pipe
try:
    from . import win_pipe
except Exception:
    now_dir = os.path.dirname(__file__)
    sys.path.insert(0, now_dir)
    import win_pipe

# global config
etc = {}
etc['pipe'] = None	# --pipe
etc['pipe_uuid'] = '247ebab1-f8cf-4bc2-a7e5-2123f6a89eef'	# for create_pipe_name
etc['pipe_file'] = 'kill_cmodule.sandwich_bridge.pipe'	# save pipe_name here
# NamedPipe objects
etc['up_pipe'] = None
etc['dl_pipe'] = None

# common code with side_up

def create_pipe_name():
    random_uuid = uuid.uuid4().hex
    random_str = str(random.random())
    
    # up_pipe
    up_name = ('_').join(['', etc['pipe_uuid'], random_uuid, random_str])
    dl_name = up_name + '_'
    
    pipe_name = [up_name, dl_name]
    # save to pipe_file
    pipe_path, pipe = _gen_pipe_path()
    blob = json.dumps(pipe_name).encode('utf-8')
    with open(pipe_path, 'wb') as f:
        f.write(blob)
    # done
    return pipe_name, pipe

def get_pipe_name(pipe):
    pipe_path, pipe_file = _gen_pipe_path(pipe)
    with open(pipe_path, 'rb') as f:
        blob = f.read()
    pipe_name = json.loads(blob.decode('utf-8'))
    return pipe_name

def _gen_pipe_path(pipe_file=None):
    now_dir = os.path.dirname(__file__)
    if pipe_file == None:
        pipe_file = etc['pipe_file']
    out = os.path.normpath(os.path.join(now_dir, pipe_file))
    return out, pipe_file

def create_daemon_thread(worker, args=(None, )):
    t = threading.Thread(target=worker, args=args, daemon=True)
    t.start()
    return t

# worker threads

def dl_thread(*k, **kk):
    pipe = etc['dl_pipe']
    # accept dl_pipe
    pipe.accept()
    # TODO Error process
    
    # do download, read from pipe and print to stdout
    while True:
        blob = pipe.readline()
        text = blob.decode('utf-8')
        if (len(text) > 0) and (text[-1] == '\n'):
            text = text[:-1]
        print(text)
        # DO NOT forget flush !!!
        sys.stdout.flush()
    # end dl_thread

def up_thread(*k, **kk):
    pipe = etc['up_pipe']
    # do upload, read from stdin and write to pipe
    while True:
        text = input()
        if len(text) < 1:
            text = '\n'
        elif text[-1] != '\n':
            text += '\n'
        blob = text.encode('utf-8')
        pipe.write(blob)
    # end up_thread

def init_down_side():
    up_name, dl_name = pipe_name = get_pipe_name(etc['pipe'])
    # create dl_pipe
    etc['dl_pipe'] = win_pipe.NamedPipeServer(dl_name)
    
    # start dl_thread
    create_daemon_thread(dl_thread)
    
    # connect up_pipe
    etc['up_pipe'] = win_pipe.open_named_pipe(up_name)
    
    up_thread()	# do upload
    # end init_down_side

# main
def main(argv):
    p_args(argv)
    init_down_side()

def p_args(argv):
    rest = argv
    while len(rest) > 0:
        one, rest = rest[0], rest[1:]
        if one == '--pipe':
            etc['pipe'], rest = rest[0], rest[1:]
        else:
            pass	# TODO ignore Error here
    # end p_args

# start from main
if __name__ == '__main__':
    main(sys.argv[1:])
# end side_down.py


