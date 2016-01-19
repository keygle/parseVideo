# make_title.py, parse_video/pvdl/lib/

from . import b
from . import err, conf

# main pvdl video 'title' format
def gen_title():	# TODO
    # TODO get needed info
    title = ''
    quality = ''
    site = ''
    title_no = 0
    title_sub = ''
    
    raw = _do_gen_title(title, quality, site, title_no=title_no, title_sub=title_sub)
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
    out = ('.').join(['pvdl', 'tmp', title, 'part', index, ext])
    return out

def gen_ffmpeg_list_file_name(title):	# pvdl.tmp.TITLE.ffmpeg.list
    out = ('.').join(['pvdl', 'tmp', title, 'ffmpeg', 'list'])
    return out

def gen_merged_file_name(title, ext):	# TITLE.EXT
    out = ('.').join([title, ext])
    return out

# make format labels
def make_label():
    pass

# end make_title.py


