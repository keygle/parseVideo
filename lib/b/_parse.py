# _parse.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.0.2 test201509251757

'''
base and common parse function support, based on standard parse_video video_info format
'''

from .. import var

def select_hd(video_info):
    '''
    auto-select videos and mark the file, with var._ hd_min and hd_max data
    before remove files' info, will auto count items, such as size_byte
    will mark no-need video's file to [] (no items)
    '''
    pass	# TODO

def select_file_index(video_info):
    '''
    auto-select file with index for --min-i and --max-i
    will mark no-need file's url to '' (null string)
    '''
    pass	# TODO

def auto_count(video_info):
    '''
    auto-count info of video items
    '''
    pass	# TODO

# end _parse.py


