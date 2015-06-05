# make_ffmpeg_list.py, part for parse_video : a fork from parseVideo. 
# make_ffmpeg_list: bin/make_ffmpeg_list: write ffmpeg concat list files, for output file name. 
# version 0.0.2.0 test201506060051
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

# global vars
list_file_i = 0
LIST_FILE_AFTER = '_.list.txt'

# functions
def write_list_file(fname, content):
    with open(fname, 'w') as f:
        f.write(content)
    # done

def clean_file_name(text, remove_chars='/|\\ ?	*<>:\'\"', replace_char='_'):
    to = remove_chars
    out = ''
    for i in text:
        if i in to:
            out += replace_char
        else:
            out += i
    # done
    return out

def make_list_file_name(title, vinfo):
    # get quality, hd, format info
    quality = vinfo['quality']
    format_info = vinfo['format']
    # make file name
    global list_file_i
    fname = str(list_file_i) + '_' + quality + '_' + format_info + '_' + title + LIST_FILE_AFTER
    # add list_file_i
    list_file_i += 1
    # clean it
    fname = clean_file_name(fname)
    # done
    return fname

def make_one_list(flist, before='file \'', after='\''):
    t = []	# final output text
    # process each file url
    for f in flist:
        fname = get_file_name_from_url(f['url'])
        t.append(before + fname + after)
    # make output text
    t = ('\n').join(t)
    # done
    return t

def get_file_name_from_url(raw_url):
    # process remove '?' and after text
    url = raw_url.split('?')[0]
    # file name is before last '/'
    fname = url.split('/')[-1]
    # done
    return fname

def make_list(evinfo):
    # get title info
    title = evinfo['info']['title']
    # make each list
    for v in evinfo['video']:
        # make list file name
        fname = make_list_file_name(title, v)
        # make list
        list_content = make_one_list(v['file'])
        # write it
        write_list_file(fname, list_content)
    # done

# end make_ffmpeg_list.py


