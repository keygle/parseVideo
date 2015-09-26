# _parse.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509261456

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
    # NOTE auto-count video files info
    video_info = auto_count(video_info)
    # select and ignore videos
    hd_min = var._['hd_min']
    hd_max = var._['hd_max']
    for v in video_info:
        hd = v['hd']
        flag_ignore = False
        if (hd_min != None) and (hd < hd_min):
            flag_ignore = True
        if (hd_max != None) and (hd > hd_max):
            flag_ignore = True
        if flag_ignore:
            v['file'] = []
    return video_info

def select_file_index(video_info):
    '''
    auto-select file with index for --min-i and --max-i
    will mark no-need file's url to '' (null string)
    '''
    i_min = var._['i_min']
    i_max = var._['i_max']
    for v in video_info:
        for i in range(len(v['file'])):
            f = v['file'][i]
            flag_ignore = False
            if (i_min != None) and (i < i_min):
                flag_ignore = True
            if (i_max != None) and (i > i_max):
                flag_ignore = True
            if flag_ignore:
                f['url'] = ''
    return video_info

def auto_count(video_info):
    '''
    auto-count info of video items
    will auto-ignore count-ed items
    '''
    for v in video_info:
        # set count
        count = len(v['file'])
        if not 'count' in v:
            v['count'] = count
        # count items
        size_byte = 0
        time_s = 0
        for f in v['file']:
            if f['size'] < 0:
                size_byte = -1
            elif size_byte >= 0:
                size_byte += f['size']
            if f['time_s'] < 0:
                time_s = -1
            elif time_s >= 0:
                time_s += f['time_s']
        # set size_byte and time_s
        if not 'size_byte' in v:
            v['size_byte'] = size_byte
        if not 'time_s' in v:
            v['time_s'] = time_s
    return video_info

# end _parse.py


