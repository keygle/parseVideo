# conf.py, parse_video/o/plist/lib/, config file for plist

output_dir = '../../list'


URL_TO_EXTRACTOR = {
    # http://www.iqiyi.com/a_19rrha9kmt.html
    '^http://www\.iqiyi\.com/a_[0-9a-z]+\.html' : 'iqiyi', 
    #'^http://[a-z]+\.iqiyi\.com/.+\.html' : 'iqiyi', 
    
    # http://www.letv.com/tv/10016481.html
    '^http://www\.letv\.com/tv/[0-9]+\.html' : 'letv', 
}

DEFAULT_METHOD = {
    'iqiyi' : 'html', 
    'letv' : 'html', 
}


PLIST_LOG_PREFIX = 'plist::'
FILENAME_BAD_CHAR = ' \\:"/|?*<>'
FILENAME_REPLACE = '-'

# for PLINFO
PLINFO_MARK_UUID = 'b0b0e371-df34-45cb-b625-626a54621180'
PLINFO_PORT_VERSION = '0.1.0'

# NOTE runtime data
plist_version = None

flag_debug = False
_extractor_id = None

# end conf.py


