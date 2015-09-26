# _thread.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509261800

import threading
import multiprocessing.dummy as multiprocessing

def map_do(todo_list, worker=lambda x:x, pool_size=1):
    pool = multiprocessing.Pool(processes=pool_size)
    pool_output = pool.map(worker, todo_list)
    pool.close()
    pool.join()
    return pool_output

# end _thread.py


