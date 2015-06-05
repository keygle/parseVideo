# -*- coding: utf-8 -*-
# 0.py, for parse_video win vesion

# import
import sys
import subprocess

# main function
def main():
    print('parse_video 简单测试 0.py')
    url = raw_input('请输入 URL: ')
    # get python bin
    pybin = sys.executable
    # start parsev
    arg = [pybin, 'parsev', '--output-easy', url]
    exit_code = subprocess.call(arg, shell=False)
    return exit_code

# start from main
if __name__ == '__main__':
    exit(main())

# end 0.py


