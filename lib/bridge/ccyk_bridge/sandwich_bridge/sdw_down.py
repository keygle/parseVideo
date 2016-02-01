#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sdw_down.py, wuyan4/sandwich_bridge/, the down side of the sandwich 
# LICENSE GNU GPLv3+, sceext <sceext@foxmail.com> 
# version 0.1.0.0 test201510042112

# TODO auto-check windows on linux, use different actions

import os, sys
import threading

# import win_pipe
now_dir = os.path.dirname(__file__)
sys.path.insert(0, now_dir)

import win_pipe

# download thread, pipe_ --> stdout
def download_thread(pipe_name):
    # create a new pipe for download
    real_pipe_name = pipe_name + '_'
    pipe = win_pipe.NamedPipeServer(real_pipe_name)
    # NOTE accept it first
    try:
        pipe.accept()
    except Exception as e:
        pass	# just ignore it
    
    while True:
        blob = pipe.readline()
        text = blob.decode('utf-8')
        if (len(text) > 0) and (text[-1] == '\n'):
            text = text[:-1]
        print(text)
        # NOTE DO NOT forget flush !!! 
        sys.stdout.flush()
    # done

# main function
def main(argv):
    # process args
    pipe_name = None
    rest = argv
    while len(rest) > 0:
        one = rest[0]
        rest = rest[1:]
        if one == '--pipe-name':
            pipe_name = rest[0]
            rest = rest[1:]
        else:	# just ignore it
            pass
    # start download thread, pipe --> stdout
    t = threading.Thread(target=download_thread, args=(pipe_name, ), daemon=True)
    t.start()
    # NOTE start download_thread before open given pipe
    # connect to the pipe
    f = win_pipe.open_named_pipe(pipe_name)
    # do upload, stdin --> pipe
    while True:
        raw_text = input()
        if len(raw_text) < 1:
            raw_text = '\n'
        elif raw_text[-1] != '\n':
            raw_text += '\n'
        blob = raw_text.encode('utf-8')
        f.write(blob)
    # done

# start from main
if __name__ == '__main__':
    main(sys.argv[1:])

# end sdw_down.py


