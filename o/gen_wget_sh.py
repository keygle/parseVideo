#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# gen_wget_sh.py, gen wget .sh script for parse_video
# version 0.0.2.0 test201510222117

import os, sys
import json
import subprocess

# global data
etc = {}
etc['pre_args'] = [
    '../parsev', 
    '--method', 
    'pc_flash_gate;set_um,set_flag_v', 
    '--min', 
    '3', 
]

# num len
def num_len(n, l=2):
    t = str(n)
    while len(t) < l:
        t = '0' + t
    return t

# main function
def main(argv):
    # make args
    args = etc['pre_args'] + argv
    # start parse_video process
    PIPE = subprocess.PIPE
    p = subprocess.Popen(args, stdout=PIPE, stderr=sys.stderr, shell=False)
    # get result
    blob, stderr = p.communicate()
    raw_text = blob.decode('utf-8')
    info = json.loads(raw_text)
    
    # get video urls
    video = None
    for v in info['video']:
        if len(v['file']) > 0:
            video = v
            break
    url_list = []
    for f in video['file']:
        url_list.append(f['url'])
    title = info['info']['title']
    # gen wget sh
    line = []
    for i in range(len(url_list)):
        # make file name
        file_name = title + '_' + num_len(i) + '_.mp4'
        
        one = 'wget -O ' + file_name + ' \"' + url_list[i] + '\" '
        line.append(one)
    line.append('')
    text = ('\n').join(line)
    # make sh name
    sh_name = title + '_pv_wget.sh'
    # write file
    with open(sh_name, 'w') as f:
        f.write(text)
    # print raw text
    print()
    print(raw_text)
    # done

# start from main
if __name__ == '__main__':
    main(sys.argv[1:])

# end gen_wget_sh.py


