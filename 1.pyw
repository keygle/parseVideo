#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 1.py, for parse_video win vesion
# used on windows, with python3

# import
from o.pvtkgui import entry
from bin import make_rename_list as make_rename_list0
from bin import output_text as output_text0

# set import
entry.set_import(make_rename_list=make_rename_list0, output_text=output_text0)

# main function
def main():
    # just start entry
    entry.init()
    # TODO FIXME debug here
    return 0

# start from main
if __name__ == '__main__':
    exit(main())

# end 1.py


