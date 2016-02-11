# side_up.py, parse_video/lib/bridge/sandwich_bridge/sandwich_host/
# up_side of sandwich_bridge 2 (sandwich_host)

import os, sys
import threading
import subprocess
import time

from . import win_pipe, side_down
from .sandwich_io import io_one_line_json as iooj
from .sandwich_io import io_one_line_colon as iooc

# TODO Error process here
# TODO support host_core

# global config
etc = {}
# sandwich_core config
etc['adl'] = ['adl']	# start adl args
etc['bridge_host'] = '../bridge_host/sandwich_bridge_host.xml'
etc['down_side'] = './side_down.py'
etc['bridge_core'] = None	# TODO

etc['connect_dl_pipe_wait_s'] = 0.1	# 0.1 s
etc['connect_dl_pipe_retry_time'] = 50	# 0.1s * 50 = 5s
# NamedPipe objects
etc['up_pipe'] = None
etc['dl_pipe'] = None
# sandwich_core sub process (adl AIR)
etc['p'] = None
# runtime vars
etc['pipe_name'] = None
etc['pipe'] = None
# TODO

# init functions
def init_up_side():
    # NOTE up_side only use 1 thread
    
    # TODO create up_pipe
    pipe_name, pipe = side_down.create_pipe_name()
    etc['pipe_name'] = pipe_name
    etc['pipe'] = pipe
    up_name, dl_name = pipe_name
    
    etc['up_pipe'] = win_pipe.NamedPipeServer(up_name)
    
    # start sandwich_core
    _start_sandwich_core()
    # connect dl_pipe
    _connect_dl_pipe()
    
    # TODO load bridge_core
    # TODO NOTE not support load bridge_core here now
    
    # FIXME DEBUG here
    print('DEBUG: init_up_side done ')
    # up_side init done

def _start_sandwich_core():
    raw_args, bridge_host = _make_sandwich_core_args()
    # gen adl args
    args = etc['adl'] + [bridge_host, '--'] + raw_args
    # FIXME DEBUG here
    print('DEBUG: start core ' + str(args) + ' ')
    # TODO prevent re-init
    # start sub process
    etc['p'] = subprocess.Popen(args, shell=False)
    # done

def _make_sandwich_core_args():
    out = []
    # --py-bin
    python_bin = sys.executable
    out += ['--py-bin', python_bin]
    # --down-side
    now_dir = os.path.dirname(__file__)
    down_side = os.path.realpath(os.path.join(now_dir, etc['down_side']))
    out += ['--down-side', down_side]
    # --pipe
    out += ['--pipe', etc['pipe']]
    # bridge_host
    bridge_host = os.path.realpath(os.path.join(now_dir, etc['bridge_host']))
    return out, bridge_host

def _connect_dl_pipe():
    # TODO Error process
    # accept up_pipe
    etc['up_pipe'].accept()
    
    # FIXME DEBUG log here
    print('DEBUG: connect dl_pipe ')
    
    # try many times to connect dl_pipe
    retry = 0
    retry_max = etc['connect_dl_pipe_retry_time']
    wait_s = etc['connect_dl_pipe_wait_s']
    dl_pipe = etc['pipe_name'][1]
    
    while True:
        try:
            etc['dl_pipe'] = win_pipe.open_named_pipe(dl_pipe)
            break
        except Exception as e:
            retry += 1
            # check retry
            if retry >= retry_max:
                # FIXME Error log
                print('ERROR: retry connect dl_pipe failed ')
                er = Exception('side_up._connect_dl_pipe, retry', retry_max)
                raise er from e
            # NOTE ignore Error to retry here
        # sleep before next retry
        time.sleep(wait_s)
    # done

def _load_bridge_core():
    # TODO
    pass

# sandwich_bridge base io functions
def sandwich_write(raw):
    # encode with io_one_line_json
    text = iooj.encode(raw)
    blob = text.encode('utf-8')
    etc['dl_pipe'].write(blob)

def sandwich_read():
    blob = etc['up_pipe'].readline()
    text = blob.decode('utf-8')
    # decode with io_one_line_json
    out = iooj.decode(text)
    return out

# TODO support host_core

# passthrough stdin/stdout to sandwich_bridge (for DEBUG)
def _bin_stdio():
    # TODO support exit
    while True:
        # read input line
        raw = input()
        # decode with io_one_line_colon
        info = iooc.decode(raw)
        
        # write to sub
        sandwich_write(info)
        # wait response
        raw = sandwich_read()
        
        # encode with io_one_line_colon
        out = iooc.encode(raw)
        print(out)
    # end _bin_stdio

# main
def main(argv):
    _p_args(argv)
    init_up_side()
    _bin_stdio()

def _p_args(argv):
    pass	# TODO support more config

# end side_up.py


