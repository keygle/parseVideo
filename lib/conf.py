# conf.py, parse_video/lib/

# config file path
e_bks1_vv_conf = 'private.e_bks1_vv.conf.json'
e_letv_vv_conf = 'private.e_letv_vv.conf.json'

# default method for extractors
DEFAULT_METHOD = {
    'bks1' : 'pc_flash_gate;fix_4k', 
    'letv' : 'pc_flash_gate', 
    'hunantv' : 'flvsp', 
    'tvsohu' : 'flvsp', 
    'pptv' : 'pc_flash_gate', 
    'vqq' : 'pc_flash_gate;enable_fmt_black_list,fix_1080p,ignore_fix_1080p_error', 
    'youku' : 'pc_flash_gate', 
}

# URL (RE) to extractor_id
URL_TO_EXTRACTOR = {
    # http://www.le.com/ptv/vplay/1903731.html
    '^http://www\.le\.com/.+\.html' : 'letv', 
    # http://www.mgtv.com/v/2/168868/f/2992014.html
    '^http://www\.mgtv\.com/.+\.html' : 'hunantv', 
    
    '^http://[a-z]+\.iqiyi\.com/.+\.html' : 'bks1', 
    '^http://tv\.sohu\.com/.+\.shtml' : 'tvsohu', 
    '^http://v\.pptv\.com/.+\.html' : 'pptv', 
    '^http://v\.qq\.com/.+' : 'vqq', 
    # NOTE for extractor letv method m3u8
    '^file:///.+\.m3u8$' : 'letv', 	# TODO may be not stable
    '^http://.+/letv-uts/.+/ver_.+\.m3u8?' : 'letv', 
    
    # youku TODO support more URL types
    '^http://v\.youku\.com/v_show/id_[A-Za-z0-9]+\.html' : 'youku', 
}

# overwrite extractor default method by URL RE match
OVERWRITE_EXTRACTOR_METHOD = {
    'letv' : {
        '^file:///.+\.m3u8$' : 'm3u8',
        '^http://.+/letv-uts/.+/ver_.+\.m3u8?' : 'm3u8', 
    }, 
}

# used for --fix-enable-more
METHOD_ENABLE_MORE = {
    'youku' : None, 	# NOTE extractor youku not support --more
}


PV_LOG_PREFIX = 'pv::'

# firefox/43.0 on Windows 7 (64bit)
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'

# network timeout second, -1 means disabled
network_timeout_s = 5


## extractor config

# extractor vqq
E_VQQ_FMT_BLACK_LIST = [
    'mp4', 
    'flv', 
]


# NOTE config of handwich_bridge is not here

# end conf.py


