# conf.py, parse_video/lib/


# config file path
e_bks1_vv_conf = 'private.bks1_vv_conf.json'

# default method for extractors
DEFAULT_METHOD = {
    'bks1' : 'pc_flash_gate', 
}

# URL (RE) to extractor_id
URL_TO_EXTRACTOR = {
    '^http://[a-z]+\.iqiyi\.com/.+\.html' : 'bks1', 
}


PV_LOG_PREFIX = 'pv::'

# firefox/43.0 on Windows 7 (64bit)
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'

# end conf.py


