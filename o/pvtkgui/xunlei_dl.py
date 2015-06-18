# xunlei_dl.py, part for parse_video : a fork from parseVideo. 
# xunlei_dl: o/pvtkgui/xunlei_dl: parse_video Tk GUI, add download tasks to xunlei with windows com ThunderAgent. 
# version 0.0.16.0 test201506182128
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

import imp

from .b import run_sub
from . import xunlei_agent

from ..output import easy_text
from ..easy import make_name

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
comtypes = None	# comtypes

INSTALL_COMTYPES_BIN = '.\\o\\easy\\install.bat'

xunlei_agent = None

# functions

# import comtypes.client as cc
def import_cc():
    global cc
    global comtypes
    try:
        # not reload, fix com error BUG
        if comtypes == None:
            import comtypes as comtypes0
            comtypes = comtypes0
        
        # do import cc
        if cc == None:
            import comtypes.client as cc0
            cc = cc0
    except Exception as e:
        raise ComTypesError(e)
    # done

# create ThunderAgent.Agent com object
def create_thunder_agent():
    try:
        ta = cc.CreateObject(xunlei_agent.AGENT1)
    except Exception as e1:
        try:	# try Agent64
            ta = cc.CreateObject(xunlei_agent.AGENT2)
        except Exception as e2:
            raise CreateComObjError(e1, e2)
    # done
    return ta

# main function
def create_agent():
    # init
    import_cc()
    ta = create_thunder_agent()	# thunder_agent
    global xunlei_agent
    xunlei_agent = ta
    # done

def add_task(tlist, xunlei_dl_path=None):
    ta = xunlei_agent
    # check tlist length
    if len(tlist) < 1:
        return 0	# just return 0
    # reset task_count
    task_count = 0
    # add each task
    for t in tlist:
        # check xunlei_dl_path
        if xunlei_dl_path != None:
            ta.AddTask(t['url'], t['file'], xunlei_dl_path)
        else:
            ta.AddTask(t['url'], t['file'])
        task_count += 1
    # add tasks done, commit task
    ta.CommitTasks()
    # done
    return task_count

# make task list
def make_task_list(evinfo):
    make_num_len = make_rename_list_.make_num_len
    # make file name before
    inf = evinfo['info']
    title = inf['title']
    title_sub = inf['title_sub']
    title_no = inf['title_no']
    title_short = inf['title_short']
    site_name = inf['site_name']
    # get url list
    i = 0
    tlist = []
    for v in evinfo['video']:
        ext_name = '.' + v['format']
        for f in v['file']:
            one = {}
            one['url'] = f['url']
            i += 1
            # use make_name_host to make final file name
            one['file'] = make_name_host(title=title, title_sub=title_sub, title_no=title_no, title_short=title_short, part_i=i, ext=ext_name, site=site_name)
            # add one task done
            tlist.append(one)
    # done
    return tlist

# auto install comtypes support
def install_comtypes():
    # just run install.bat to install comtypes
    run_sub.run_sub([INSTALL_COMTYPES_BIN], shell=True)
    # auto reload comtypes after install
    global comtypes
    if comtypes == None:
        import comtypes as comtypes0
        comtypes = comtypes0
    else:
        imp.reload(comtypes)
    # done

# make_name host function
def make_name_host(title='', title_short='', title_sub='', title_no='', part_i=0, ext='', site=''):
    raw_name = make_name.make(title, title_sub, title_no, title_short, site, part_i, make_name_host_num_len, ext)
    # clean file name
    fname = easy_text.clean_file_name(fname)
    return fname

def make_name_host_num_len(title_no=-1, num_len=4):
    make_num_len = easy_text.make_num_len
    if title_no < 1:
        return ''
    else:
        return make_num_len(title_no, num_len)
    # done

# end xunlei_dl.py


