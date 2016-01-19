# conf.py, parse_video/pvdl/lib/, config file for pvdl


# auto-select hd in this range, will always select max hd
auto_select_hd = [-1, 8]

# save downloaded file here
output_dir = './dl/'	# --output

# error retry times
error_retry = 3		# -1 means retry forever; --retry
# before error_retry, first sleep some time
retry_wait_time_s = 1	# --retry-wait



## !!! WARNING !!! ADVANCED OPTIONS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#  DO NOT touch unless you know what you are doing. 


# output merged video file format
merge_output_format = 'mp4'	# NOTE other formats may not work

# enable and disable pvdl features
FEATURES = {	# --enable, --disable
    ## parse stage
    'fix_size' : True, 	# if parse_video not get part file size, try to fix it here
    'force_enable_more' : False, 	# each time use log file to enable_more
    
    # create task
    'check_log_file' : True, 	# check log file if exists, and stop if not match
    'check_lock_file' : True, 	# use lock file to prevent two instance of pvdl to work in same directory at the same time
    
    ## download stage
    
    # before download
    'check_remote_size' : False, 	# check network file size
    'check_local_size' : True, 		# check local file size and skip finished files
    'skip_local_lager_file' : False, 	# if local file is too large, just skip it (ignore Error)
    
    # after download
    'check_file_size' : True, 	# check part file size
    'check_file_md5' : True, 	# check part file md5 checksum if possible
    
    ## merge stage
    'check_merged_size' : True, 	# check merged file size
    'check_merged_time' : True, 	# check merged video time, if possible (requires mediainfo)
    
    'force_merge' : False, 	# remove output file and continue merge, if output file already exists
    
    ## other options
    'parse_twice' : True, 	# (TODO support it) first parse only to get video formats, second parse to get file URLs
    'parse_twice_enable_more' : True, 	# enable_more to speed up second parse
    'merge_single_file' : True, 	# do merge with single file (only one part file) (This is required for check_merged_time)
    
    'check_disk_space' : False, 	# before download to check disk space, and stop when space is not enough
    'check_permission' : False, 	# check permission to write files
    
    'fix_unicode' : False, 	# fix_unicode is only for Windows
    
    ## DANGER options
    'auto_remove_tmp_files' : False, 	# remove pvdl tmp files after download succeed; require enable check_merged_time and merge_single_file
}


# allowed no error mismatch
CHECK_ERR_K = {	# NOTE -1 means unlimit
    # check_remote_size
    'remote_size' : 1, 		# 1 %
    'remote_size_mb' : 64, 	# 64 MB
    # check_local_size
    'local_size' : 1, 		# 1 %
    'local_size_mb' : 64, 	# 64 MB
    # check_file_size
    'file_size' : 1, 		# 1 %
    'file_size_mb' : 64, 	# 64 MB
    # check_merged_size
    'merged_size' : 5, 		# 5 %
    'merged_size_mb' : 256, 	# 256 MB
    # check_merged_time
    'merged_time' : 1, 		# 1 %
    'merged_time_min' : 1, 	# 1 minute
}


# pvdl call subprocess bin file
SUB_BIN = {	# NOTE paths starts with ./ or ../ is from pvdl root path (pvdl/)
    'parsev' : '../parsev', 
    'wget' : 'wget', 
    'ffmpeg' : 'ffmpeg', 
    'mediainfo' : 'mediainfo', 
}


PVDL_LOG_PREFIX = 'pvdl::'
FILENAME_BAD_CHAR = ' \\:"/|?*<>'


## more data here, global common data
raw_url = ''
raw_args = []	# --, raw args passed to parse_video
pvinfo = None
task_info = None

select_hd = None	# --hd
title_suffix = None	# --title-suffix

flag_debug = False	# --debug

# end conf.py


