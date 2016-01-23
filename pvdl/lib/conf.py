# conf.py, parse_video/pvdl/lib/, config file for pvdl


# auto-select hd in this range, will always select max hd
auto_select_hd = [-1, 8]

# save downloaded file here
output_dir = './dl/'	# --output

# error retry times
error_retry = 20	# -1 means retry forever; --retry
# before error_retry, first sleep some time
retry_wait_time_s = 1	# --retry-wait

# parse timeout
parse_timeout_s = 180	# TODO -1 means disabled; default 3 minute (180s); after this second, will stop parse (as parse failed)



## !!! WARNING !!! ADVANCED OPTIONS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#  DO NOT touch unless you know what you are doing. 


# output merged video file format
merge_output_format = 'mp4'	# NOTE other formats may not work

# enable and disable pvdl features
FEATURES = {	# --enable, --disable
    ## parse stage
    'print_parse_video_output' : False, # print parse_video raw output for DEBUG
    'fix_size' : True, 		# TODO if parse_video not get part file size, try to fix it here
    
    # create task
    'fix_title_no' : False, 		# TODO try to get check and fix title_no from title text
    'base_path_add_title' : False, 	# TODO if title_no is add to title, add title_short to base_path (for auto group videos)
    
    'check_log_file' : True, 		# check log file if exists, and stop if not match
    'check_log_file_strict' : False, 	# check more values in log file
    
    ## entry works
    'check_lock_file' : True, 		# use lock file to prevent two instance of pvdl to work in same directory at the same time
    'keep_lock_file' : True, 		# not remove lock file when task successfully finished, to prevent re-do this work
    'skip_lock_err' : False, 		# if get lock file failed, just skip it (for list download)
    
    ## download stage
    
    # before download
    'check_remote_size' : False, 	# TODO check network file size
    'check_remote_fix_size' : True, 	# TODO if check_remote_size enabled, fix part file size here
    
    'check_local_size' : True, 		# check local file size and skip finished files
    'skip_local_larger_file' : False, 	# if local file is too large, just skip it (ignore Error)
    
    # after download
    'check_file_size' : True, 		# check part file size
    'check_file_md5' : True, 		# check part file md5 checksum if possible
    
    ## merge stage
    'check_merged_size' : True, 	# check merged file size
    'check_merged_time' : True, 	# check merged video time, if possible (requires mediainfo)
    
    'force_merge' : False, 		# TODO remove output file and continue merge, if output file already exists
    'merge_twice' : False, 		# TODO before final merge, do merge each part file first to fix time_s Errors
    
    ## other options
    'parse_twice' : True, 		# TODO first parse only to get video formats, second parse to get file URLs
    'parse_twice_enable_more' : True, 	# TODO enable_more to speed up second parse
    'merge_single_file' : True, 	# TODO do merge with single file (only one part file) (This is required for check_merged_time)
    
    'check_disk_space' : True, 		# TODO before download to check disk space, and stop when space is not enough
    'check_permission' : False, 	# TODO check permission to write files
    
    'fix_unicode' : False, 		# fix_unicode is only for Windows
    
    ## DANGER options
    'auto_remove_tmp_part_files' : False, 	# TODO remove part files (tmp file) to save disk space after download succeed
    # NOTE this require all needed checks to pass TODO require enable check_merged_time and merge_single_file
}


# TODO TODO support -1 means unlimit
# allowed no error mismatch
CHECK_ERR_K = {	# NOTE -1 means unlimit
    # check_remote_size
    'remote_size' : 1, 		# 1 %
    'remote_size_mb' : 64, 	# 64 MB
    # check_local_size
    'local_size' : 0, 		# 0 %
    'local_size_mb' : 0, 	# 0
    # check_file_size
    'file_size' : 1, 		# 1 %
    'file_size_mb' : 16, 	# 16 MB
    # check_merged_size
    'merged_size' : 1, 		# 1 %
    'merged_size_mb' : 32, 	# 32 MB
    # check_merged_time
    'merged_time' : 0.5, 		# 0.5 %
    'merged_time_s' : 5, 	# 5 second
}


# pvdl call subprocess bin file
SUB_BIN = {	# NOTE paths starts with ./ or ../ is from pvdl root path (pvdl/)
    'parsev' : ('../pv', True), 
    'wget' : ('wget', False), 
    'ffmpeg' : ('ffmpeg', False), 
    'mediainfo' : ('mediainfo', False), 
}


PVDL_LOG_PREFIX = 'pvdl::'
FILENAME_BAD_CHAR = ' \\:"/|?*<>'
FILENAME_REPLACE = '-'

# NOTE add pvdl version info for DEBUG
pvdl_version = None

## more data here, global common data
raw_url = ''
raw_args = []	# --, raw args passed to parse_video

pvinfo = None
task_info = None

select_hd = None	# --hd
title_suffix = None	# --title-suffix
title_no = None		# --title-no
# overwrite default values
set_output = output_dir
set_retry = error_retry
set_retry_wait = retry_wait_time_s
set_parse_timeout = parse_timeout_s

flag_debug = False	# --debug
limit_kb = None		# TODO download speed limit, unit KB

# NOTE save checks status, for final check remove part file
check_status = {
    # TODO
}

keep_lock_file = False		# if True, will not remove lock file
check_log_file = None		# NOTE used for check_log file
check_log_file_path = None	# used for DEBUG

# end conf.py


