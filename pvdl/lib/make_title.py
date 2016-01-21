# make_title.py, parse_video/pvdl/lib/

import math
from . import err, b, conf


# gen video common title
def gen_common_title(pvinfo):
    info = pvinfo['info']
    title_no = info.get('title_no', -1)
    title_sub = info.get('title_sub', '')
    raw = _do_gen_title(info['title'], '', info['site_name'], title_no=title_no, title_sub=title_sub)
    out = b.replace_filename_bad_char(raw)
    return out


# main pvdl video 'title' format
def gen_title(task_info):
    info = task_info['info']
    # get needed info
    title_no = info.get('title_no', -1)
    title_sub = info.get('title_sub', '')
    quality = task_info['video']['quality']
    
    raw = _do_gen_title(info['title'], quality, info['site_name'], title_no=title_no, title_sub=title_sub)
    out = b.replace_filename_bad_char(raw)
    return out

def _do_gen_title(title, quality, site, title_no=-1, title_sub=''):
    if title_no < 0:
        title_no = ''
    else:
        title_no = b.num_len(title_no, 4)
    out = ('_').join([title_no, title, title_sub, quality, site])
    return out

# gen pvdl download filename and paths

def gen_tmp_dir_name(title):	# pvdl.TITLE.tmp/
    out = ('.').join(['pvdl', title, 'tmp'])
    return out

def gen_log_file_name(title):	# pvdl.tmp.TITLE.log.json
    out = ('.').join(['pvdl', 'tmp', title, 'log', 'json'])
    return out

def gen_lock_file_name(title):	# pvdl.tmp.TITLE.lock
    out = ('.').join(['pvdl', 'tmp', title, 'lock'])
    return out

def gen_part_file_name(title, index, ext):	# pvdl.tmp.TITLE.part.INDEX.EXT
    out = ('.').join(['pvdl', 'tmp', title, 'part', str(index), ext])
    return out

def gen_ffmpeg_list_file_name(title):	# pvdl.tmp.TITLE.ffmpeg.list
    out = ('.').join(['pvdl', 'tmp', title, 'ffmpeg', 'list'])
    return out

def gen_merged_file_name(title, ext):	# TITLE.EXT
    out = ('.').join([title, ext])
    return out

## make format labels

def gen_labels(pvinfo):
    out = _make_label(pvinfo['video'])
    return out	# TODO code may be clean

# do make label text
def _make_label(video):
    # gen base label info
    label_info = []
    for v in video:
        label_info.append(_gen_label_info(v))
    # add label index
    video_len = len(video)
    n_len = math.floor(math.log(video_len, 10)) + 1
    out = []
    for i in range(video_len):
        index = '(' + b.num_len(i + 1, n_len) + ') '
        out.append(index)
    
    # add hd
    for i in range(video_len):	# process hd text like -1
        if not label_info[i][0].startswith('-'):
            label_info[i][0] = ' ' + label_info[i][0]
    out = _label_just_str(0, out, label_info, fill=' ')
    # add quality
    quality_max_len = 0
    for i in range(video_len):
        l = _quality_str_len(label_info[i][1])
        if l > quality_max_len:
            quality_max_len = l
    quality_max_len += 1
    for i in range(video_len):
        out[i] += _quality_ljust(label_info[i][1], quality_max_len, fill=' ')
    # add px and bitrate
    for i in [2, 3]:
        out = _label_just_str(i, out, label_info, rjust=True, fill=' ')
    # add time
    out = _label_just_str(4, out, label_info, fill=' ')
    # add count and format
    for i in [5, 6]:
        out = _label_just_str(i, out, label_info, rjust=True, fill=' ')
    # add size_byte
    out = _label_just_str(7, out, label_info, rjust=True, fill=' ')
    # remove last _ char
    for i in range(len(out)):
        out[i] = out[i][:-1]
    return out	# gen label text done

# TODO may be move text functions to b.py

def _label_just_str(i, out, info, rjust=False, fill='_'):
    # check fill
    if len(fill) < 1:
        fill = '_'
    elif len(fill) > 1:
        fill = fill[0]
    
    max_len = 0
    for j in range(len(info)):
        l = len(info[j][i])
        if l > max_len:
            max_len = l
    for j in range(len(out)):
        raw = info[j][i]
        if rjust:
            t = raw.rjust(max_len, fill) + fill
        else:
            t = raw.ljust(max_len + 1, fill)
        out[j] += t
    return out

# process no-ascii chars
def _quality_str_len(raw, max_ascii=128):
    i = 0
    for c in raw:
        if ord(c) > max_ascii:
            i += 2
        else:
            i += 1
    return i

def _quality_ljust(raw, l=0, fill='_'):
    while _quality_str_len(raw) < l:
        raw += fill
    return raw

def _gen_label_info(v):
    p = v['size_px']
    px = str(p[0]) + 'x' + str(p[1])
    bitrate = b.gen_bitrate(v['size_byte'], v['time_s'])
    time = b.second_to_time(v['time_s'])
    size = b.byte_to_size(v['size_byte'])
    out = [str(v['hd']), v['quality'], px, bitrate, time, str(v['count']), v['format'], size]
    return out


# end make_title.py


