# -*- coding: utf-8 -*-
# __init__.py, parse_video/lib/e :: extractors' entry
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509232045

'''
extractors' entry for parse_video
'''

from . import e_list

def call(extractor_id, raw_url, raw_arg='', raw_method=''):
    '''
    call a extractor's parse() function with given info
        extractor_id	id of the extractor
        raw_url		raw_url to pass to the parse() function
        raw_arg		raw string after --extractor option's extractor_id
        		used to pass extractor args to the extractor
        raw_method	raw string of --method option
        		used to pass method and method args to the extractor
    return what the extractor's parse() function return
    '''
    
    pass

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


