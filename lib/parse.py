# parse.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509271744

'''
parse_video lib/ main parse entry
'''

from . import b
from .b import log
from . import var, err, e

def parse(raw_url='', raw_extractor='', raw_method=''):
    # check to auto-select extractor
    if raw_extractor == '':
        e_list = e.get_list(url=raw_url)
        # DEBUG log here
        log.d('got available extractor list ' + str(e_list) + ' ')
        # check support it
        if len(e_list) < 1:
            er = err.NotSupportURLError('no extractor can process this URL ', raw_url)
            er.raw_info = e_list
            raise er
        # auto select first extractor
        e_id = e_list[0]
        # check extractor exist
        e_full_list = e.get_list()
        if not e_id in e_full_list:
            raise err.ConfigError('extractor \"' + e_id + '\" not exist')
    else:	# get extractor_id and args
        raw_e = raw_extractor.split(';', 1)
        if len(raw_e) < 2:
            raw_e.append('')
        e_id, e_arg = raw_e
        # NOTE not check extractor exist here
    # DEBUG log here
    log.d('use extractor \"' + e_id + '\" with arg \"' + e_arg + '\" ')
    # check to set default method
    if raw_method == '':
        default_list = var._['default_method']
        if not e_id in default_list:
            er = err.ConfigError('no default method for extractor \"' + e_id + '\" in config file ')
            er.raw_info = default_list
            raise er
        e_method = default_list[e_id]
    else:
        e_method = raw_method
    # DEBUG log here
    log.d('use method \"' + e_method + '\" ')
    log.d('call extractor with raw_url \"' + raw_url + '\" ')
    # just call the extractor's parse() function
    raw_evinfo = e.call(e_id, raw_url, raw_arg=e_arg, raw_method=e_method)
    # more process to raw_evinfo
    evinfo = _process_raw_evinfo(raw_evinfo)
    return evinfo	# process done

def _process_raw_evinfo(raw):
    # add info
    # TODO
    # add quality to video
    # TODO
    # check and use restruct
    # TODO
    pass

# end parse.py


