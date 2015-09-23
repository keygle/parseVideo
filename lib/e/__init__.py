# -*- coding: utf-8 -*-
# __init__.py, parse_video/lib/e :: extractors' entry
# LICENSE GNU GPLv3+ sceext 
# version 0.0.3.0 test201509240200

'''
lib/e
    extractors of parse_video
lib/e/__init__.py
    extractors' entry for parse_video
'''

from .. import err
from . import e_list

def call(extractor_id, raw_url, raw_arg='', raw_method=''):
    '''
    call a extractor's parse() function with given info
        extractor_id	id of the extractor
        raw_url		raw_url to pass to the parse() function
        raw_arg		raw string after --extractor option's extractor_id
        		used to pass extractor args to the extractor
        		default value is '', means no arg
        raw_method	raw string of --method option
        		used to pass method and method args to the extractor
        		default value is '', means use the default method
    return what the extractor's parse() function return
    '''
    # TODO import the extractor
    ex = e_list.import_extractor(extractor_id)
    
    # init extractor's global var data
    ex.var.push()
    ex.var._ = ex.var.init()
    ex.var._['raw_arg'] = raw_arg
    ex.var._['raw_method'] = raw_method
    # just call it
    try:
        result = ex.parse(raw_url)
        return result
    except err.ParseError as e:
        # just raise it
        raise
    except Exception as e:
        # TODO
        raise err.UnknowError() from e
    finally:	# recovery var data
        ex.var._ = ex.var.pop()

def get_list():
    '''
    return the list of extractors, with extractor_id and more info
    '''
    
    pass

def get_about_info(extractor_id):
    '''
    return the extractor's info (include help info, extractor version, etc. )
    '''
    
    pass

# end __init__.py


