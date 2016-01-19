# make_title.py, parse_video/pvdl/lib/

from . import b
from . import err, conf

# main pvdl video 'title' format
def gen_title():
    pass

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


