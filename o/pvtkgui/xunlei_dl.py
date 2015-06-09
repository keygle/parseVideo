# xunlei_dl.py, part for parse_video : a fork from parseVideo. 
# xunlei_dl: o/pvtkgui/xunlei_dl: parse_video Tk GUI, add download tasks to xunlei with windows com ThunderAgent. 
# version 0.0.3.0 test201506092138
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.06. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# import

from . import run_sub

make_rename_list_ = None
output_text_ = None

# set import
def set_import(make_rename_list=None, output_text=None):
    global make_rename_list_
    global output_text_
    make_rename_list_ = make_rename_list
    output_text_ = output_text
    # set import done

# Error definition
class XunleiDlError(Exception):
    pass

# can not import comtypes lib of python3
class ComTypesError(XunleiDlError):
    pass

# can not create com obj ThunderAgent.Agent, ThunderAgent.Agent64
class CreateComObjError(XunleiDlError):
    pass

# global vars
cc = None	# comtypes.client

INSTALL_COMTYPES_BIN = 'install.bat'

# functions

# import comtypes.client as cc
def import_cc():
    global cc
    try:
        import comtypes.client as cc0
    except Exception as e:
        raise ComTypesError(e)
    # done
    cc = cc0

# create ThunderAgent.Agent com object
def create_thunder_agent():
    try:
        ta = cc.CreateObject('ThunderAgent.Agent')
    except Exception as e1:
        try:	# try Agent64
            ta = cc.CreateObject('ThunderAgent.Agent64')
        except Exception as e2:
            raise CreateComObjError(e1, e2)
    # done
    return ta

# main function
def add_task(evinfo):
    # init
    import_cc()
    ta = create_thunder_agent()	# thunder_agent
    
    # make task list
    tlist = make_task_list(evinfo)
    # check tlist length
    if len(tlist) < 1:
        return 0	# just return 0
    # reset task_count
    task_count = 0
    # add each task
    for t in tlist:
        ta.AddTask(t['url'], t['file'])
        task_count += 1
    # add tasks done, commit task
    ta.CommitTasks()
    # done
    return task_count

# make task list
def make_task_list(evinfo):
    make_num_len = make_rename_list_.make_num_len
    # make file name
    inf = evinfo['info']
    fname = inf['title'] + '_' + inf['title_sub'] + '_'
    if inf['title_no'] > 0:
        fname = make_num_len(inf['title_no']) + '_' + fname
    # get url list
    i = 0
    tlist = []
    for v in evinfo['video']:
        ext_name = '.' + v['format']
        for f in v['file']:
            one = {}
            one['url'] = f['url']
            i += 1
            one['file'] = fname + make_num_len(i) + ext_name
            # add one task done
            tlist.append(one)
    # done
    return tlist

# auto install comtypes support
def install_comtypes():
    run_sub.run_sub([INSTALL_COMTYEPS_BIN], shell=True)
    # done

# end xunlei_dl.py


