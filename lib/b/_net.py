# _net.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509232327

'''
network operations
'''

import json
import urllib
import xml.etree.ElementTree as ET

from .. import err

# easy download functions

def dl_blob(url):
    '''
    download the URL with http GET method without decoding
    return just the raw blob data
    '''
    try:
        r = urllib.request.urlopen(url)
        blob = r.read()
        return r
    except Exception as e:
        raise err.NetworkError('can not download with http GET on this url', url) from e

# TODO just support 'utf-8' encoding now
def dl_html(url, encoding='utf-8'):
    '''
    download the URL and 
    return the raw html text
    '''
    blob = dl_blob(url)
    try:
        html_text = blob.decode(encoding)
        return html_text
    except Exception as e:
        er = err.DecodingError('decode html_text failed on this url', url)
        er.raw_blob = blob
        raise er from e

def dl_json(url):
    '''
    download the URL and 
    return info from the json text
    '''
    blob = dl_blob(url)
    try:
        raw_text = blob.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('decode raw json text failed on this url', url)
        er.raw_blob = blob
        raise er from e
    try:
        info = json.loads(raw_text)
        return info
    except Exception as e:
        er = err.ParseJSONError('parse json text failed on this url', url)
        er.raw_text = raw_text
        raise er from e

# TODO just support 'utf-8' encoding now
def dl_xml(url, encoding='utf-8'):
    '''
    download the URL and 
    return info from the xml text
    '''
    blob = dl_blob(url)
    try:
        raw_text = blob.decode(encoding)
    except Exception as e:
        er = err.DecodingError('decode raw xml text failed on this url', url)
        er.raw_blob = blob
        raise er from e
    try:
        root = ET.fromstring(raw_text)
        return root
    except Exception as e:
        er = err.ParseXMLError('parse xml text failed on this url', url)
        er.raw_text = raw_text
        raise er from e

# rich POST function
def post(url, method='POST', post_data=None, header={}):
    pass	# TODO

# end _net.py


