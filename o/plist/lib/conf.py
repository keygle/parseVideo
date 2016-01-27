# conf.py, parse_video/o/plist/lib/, config file for plist

output_dir = '../../list'


URL_TO_EXTRACTOR = {
    '^http://[a-z]+\.iqiyi\.com/.+\.html' : 'iqiyi', 
}


PLIST_LOG_PREFIX = 'plist::'

# for PLINFO
PLINFO_MARK_UUID = 'b0b0e371-df34-45cb-b625-626a54621180'
PLINFO_PORT_VERSION = '0.1.0'

# NOTE runtime data
plist_version = None

_extractor_id = None

# end conf.py


