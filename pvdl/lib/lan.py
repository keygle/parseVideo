# lan.py, parse_video/pvdl/lib/, language text
# language: English (en) 


## log.py

def log_err():
    return ('ERROR: ')

def log_warn():
    return ('WARNING: ')

def log_info():
    return ('INFO: ')

def log_ok():
    return ('[ OK ] ')

def log_debug():
    return ('DEBUG: ')


## call_sub.py

def cs_d_call_pv(args):	# call_sub_debug log
    return ('call parse_video to parse, with args ' + str(args) + ' ')

def cs_err_can_not_exe(name):
    return ('can not execute ' + name + ' ')

def cs_err_pv_ret(exit_code):
    return ('parse failed, parse_video return ' + str(exit_code) + ' ')

def cs_err_pv_decode_stdout():
    return ('parse failed, decode parse_video stdout to text with utf-8 failed ')

def cs_err_pv_parse_json():
    return ('parse failed, parse parse_video output json text failed ')

def cs_d_call_mediainfo(args):
    return ('call mediainfo to get video file info, with args ' + str(args) + ' ')

def cs_err_mediainfo_ret(exit_code):
    return ('get video file info failed, mediainfo return ' + str(exit_code) + ' ')

def cs_err_mediainfo_decode_stdout():
    return ('decode mediainfo stdout to text with utf-8 failed ')

def cs_err_bin_file_gone(fpath):
    return ('bin file not exist, \"' + fpath + '\" ')

def cs_d_call_to(name, action, args):
    # NOTE action can be ['download', 'merge']
    return ('call ' + name + ' to ' + action + ', with args ' + str(args) + ' ')

def cs_err_action_failed(action, name, exit_code):
    return (action + ' failed, ' + name + ' return ' + str(exit_code) + ' ')


## merge.py

def m_call_ffmpeg():
    return ('call ffmpeg to merge part files ')

def m_ok_merge():
    return ('merge video succeed ')

def m_err_write_ffmpeg_list(list_file):
    return ('can not write ffmpeg list file \"' + list_file + '\" ')

def m_w_force_merge(merged_path):
    return ('enabled feature force_merge, now will remove file \"' + merged_path + '\" ')

def m_err_rm_merged_path(merged_path):
    return ('can not remove merged_file \"' + merged_path + '\" ')

def m_err_merge_output_exist(merged_path):
    return ('can not merge \"' + merged_path + '\", this output file already exists ')

def m_d_disable_check_merged_size():
    return ('disabled feature check_merged_size ')

def m_err_check_merged_size_get_info(merged_path):
    return ('can not check_merged_size \"' + merged_path + '\", can not get file info ')

def m_d_merged_size(local_size):
    return ('local merged file size ' + local_size + ' ')

def m_err_check_merged_size_no_info():
    return ('can not check_merged_size, no video size_byte info ')

def m_err_check_merged_time_get_info(merged_path):
    return ('can not check_merged_time \"' + merged_path + '\", can not get file time_s ')

def m_d_merged_time(local_time):
    return ('local merged file time_s ' + local_time + ' ')

def m_err_check_merged_time_no_info():
    return ('can to check_merged_time, no video time_s info ')

def m_err_mediainfo_output_no_duration():
    return ('no Duration info in mediainfo output ')


## dl_worker.py

def dl_err_part_file(part_name):
    return ('download part file \"' + part_name + '\" failed ')

def dl_err_part_file_unknow():
    return ('download part file, unknow error ')

def dl_d_local_size(local_size):
    return ('local file size ' + local_size + ' ')

def dl_err_check_local_size_no_info():
    return ('can not check_local_size, no file size info ')

def dl_w_enable_skip_local_larger_file():
    return ('enabled feature skip_local_larger_file ')

def dl_d_disable_check_file_size():
    return ('disabled feature check_file_size ')

def dl_err_check_file_size_get_info(part_name, e):
    return ('can not check_file_size \"' + part_name + '\", ' + str(e))

def dl_d_file_size(local_size):
    return ('local file_size ' + local_size + ' ')

def dl_err_check_file_size_no_info():
    return ('can not check_file_size, no file size info ')

def dl_no_info_checksum():
    return ('no checksum info for this file ')

def dl_no_info_checksum_md5():
    return ('no checksum.md5 info for this file ')

def dl_checking_md5(part_name):
    return ('checking checksum.md5 for file \"' + part_name + '\" ')

def dl_err_check_md5(e):
    return ('can not check md5, ' + str(e))

def dl_err_md5_match(file_md5, ok_md5):
    return ('checksum.md5 failed, file ' + file_md5 + ', OK ' + ok_md5 + ' ')

def dl_ok_md5(ok_md5):
    return ('checksum.md5 OK ' + ok_md5 + ' ')


## parse.py

def p_first(raw_url):
    return ('first parse, call parse_video to parse URL \"' + raw_url + '\" ')

def p_d_disable_print_parse_video_output():
    return ('disabled feature print_parse_video_output ')

def p_err_pv_parse():
    return ('call parse_video to do parse failed ')

def p_err_pv_unknow():
    return ('unknow call parse_video Error ')

def p_d_start_fix_size(todo, pool_size):
    return ('start fix_size of ' + str(todo) + ' files, pool_size = ' + str(pool_size) + ' ')

def p_set_title_no(title_no, old_title_no):
    return ('set title_no to ' + str(title_no) + ' (old ' + str(old_title_no) + ') ')

def p_fix_title_no(title_no, old_title_no):
    return ('feature fix_title_no, fix title_no to ' + str(title_no) + ' (old ' + str(old_title_no) + ') ')

def p_add_title_suffix(suffix):
    return ('add title_suffix \"' + suffix + '\" ')

def p_change_base_path(base_path):
    return ('feature base_path_add_title, base_path changed to \"' + base_path + '\" ')

def p_err_base_path_add_title():
    return ('feature base_path_add_title, can not add title info ')

def p_err_write_log_file(log_path, tmp_log_file):
    return ('can not write log file \"' + log_path + '\" (\"' + tmp_log_file + '\") ')

def p_d_disable_check_log_file():
    return ('disabled feature check_log_file ')

def p_d_log_file_not_exist(log_path):
    return ('log file not exist, \"' + log_path + '\" ')

def p_err_read_log_file(log_path):
    return ('can not read log file \"' + log_path + '\" ')

def p_err_parse_log_json(log_path, e):
    return ('can not parse json text of log file \"' + log_path + '\", ' + str(e))

def p_err_check_log(value, new, old):
    return ('check log failed, new ' + value + ' ' + str(new) + ' != old ' + str(old) + ' ')

def p_err_check_log_part_file(i):
    return ('check log failed, part file ' + str(i + 1) + ': ')

def p_err_new_is_not_old(name, new, old):
    # NOTE name can be ['size', 'time_s', 'checksum']
    return ('new ' + name + ' ' + str(new) + ' != old ' + str(old) + ' ')

def p_err_check_log_checksum():
    return ('no checksum in new file info ')

def p_d_enable_check_log_file_strict():
    return ('enabled feature check_log_file_strict ')

def p_err_check_log_strict(value, new, old):
    return ('strict check log failed, new ' + value + ' ' + str(new) + ' != old ' + str(old) + ' ')

def p_err_bad_log_file(log_path, e):
    return ('bad log file \"' + log_path + '\", ' + str(e))

def p_ok_check_log_file():
    return ('check log file pass ')


## entry.py

def e_task_retry(retry_info):
    return ('pvdl task retry ' + retry_info)

def e_retry_ok(retry_info):
    return ('pvdl task finished at retry ' + retry_info + ' ')

def e_retry_err(retry_info):
    return ('pvdl task failed at retry ' + retry_info + ' ')

def e_err_task():
    return ('pvdl task failed ')

def e_wait_retry(wait):
    return ('wait ' + str(wait) + ' s before next retry ')

def e_d_disable_parse_twice_enable_more():
    return ('disabled feature parse_twice_enable_more ')

def e_second_parse():
    return ('second parse, call parse_video to get file URLs ')

def e_err_mk_tmp_dir(tmp_path):
    return ('can not create tmp dir \"' + tmp_path + '\" ')

def e_got_lock(lock_file):
    return ('got lock \"' + lock_file + '\" ')

def e_skip_lock(lock_file):
    return ('skip lock file \"' + lock_file + '\" ')

def e_err_get_lock(lock_file, e)
    return ('can not get lock \"' + lock_file + '\", ' + str(e))

def e_i_rm_lock():
    return ('if you are sure that no pvdl instance is operating this directory, you can remove the lock file ')

def e_d_disable_check_lock_file():
    return ('disabled feature check_lock_file ')

def e_err_close_check_log(fpath, e):
    return ('can not close check_log file \"' + str(fpath) + '\", ' + str(e) + ' ')

def e_err_close_lock_file(lock_fd, lock_file, e):
    return ('can not close lock file [' + str(lock_fd) + '] \"' + lock_file + '\", ' + str(e))

def e_keep_lock_file(lock_file):
    return ('keep lock file \"' + lock_file + '\" ')

def e_err_rm_lock_file(lock_file, e):
    return ('can not remove lock file \"' + lock_file + '\", ' + str(e))

def e_err_select_hd(hd):
    return ('can not select --hd ' + str(hd) + ', no such hd ')

def e_err_select_hd_range(hdr):
    return ('can not select hd in range ' + str(hdr) + ', no hd available ')

def e_err_open_check_log(fpath):
    return ('can not open check_log file \"' + fpath + '\" ')

def e_create_check_log(fpath):
    return ('create check_log \"' + fpath + '\" ')

def e_d_disable_check_disk_space():
    return ('disabled feature check_disk_space ')

def e_err_check_disk_space_no_info(free_size):
    return ('can not check_disk_space, no size_byte info in video (free ' + free_size + ') ')

def e_pass_check_disk_space(needed_size, free_size):
    return ('check_disk_space pass, need ' + needed_size + ', free ' + free_size + ' ')

def e_no_enough_disk_space(needed_size, free_size):
    return ('no enough disk space, can not download: need ' + needed_size + ', free ' + free_size + ' ')

def e_err_dl_part_files(count_err, count):
    return ('download part files failed, err ' + str(count_err) + '/' + str(count) + ' ')

def e_ok_dl_part_files(count_ok, count):
    return ('download part files finished, OK ' + str(count_ok) + '/' + str(count) + ' ')

def e_err_auto_remove_tmp_part_feature_disable(feature):
    return ('can not auto_remove_tmp_part_files, feature [' + feature + '] not enabled. To do auto remove, this feature must be enabled! ')

def e_err_auto_remove_tmp_part_pass_check(check):
    return ('can not auto_remove_tmp_part_files, skiped check [' + check + ']. To do auto remove, this check must not be skiped! ')

def e_w_before_auto_remove_tmp_part_files(num):
    return ('enabled feature auto_remove_tmp_part_files: all checks passed, now will do remove ' + str(num) + ' tmp part files ')

def e_d_remove_tmp_part_file(fpath):
    return ('remove tmp part file \"' + fpath + '\" ')

def e_err_rm_tmp_part(fpath, e):
    return ('can not remove tmp part file \"' + fpath + '\", ' + str(e) + ' ')


# end lan.py


