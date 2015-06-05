#!/usr/bin/env python
# -*- coding: utf-8 -*-
# a.py, for parse_video win vesion
# used on windows, with python3

# import
import sys
import subprocess

# main function
def main():
    print('parse_video 简单测试 a.py 0.py')
    url = input('请输入 URL: ')
    # get python bin
    pybin = sys.executable
    # start parsev
    arg = [pybin, 'parsev', '--output-easy', '--make-ffmpeg-list', url]
    exit_code = subprocess.call(arg, shell=False)
    return exit_code

# start from main
if __name__ == '__main__':
    exit(main())

# end a.py


