# _net.py, parse_video/lib/b
# LICENSE GNU GPLv3+ sceext 
# version 0.0.4.0 test201509242242

'''
network operations
'''

# TODO support proxy

import json
import urllib.request
import xml.etree.ElementTree as ET

from .. import err, var

# easy download functions

def dl_blob(url, user_agent='__default__', referer=None):
    '''
    download the URL with http GET method without decoding
    support User-Agent and Referer http headers
    return just the raw blob data
    '''
    if user_agent == '__default__':
        user_agent = var._['user_agent']
    header = {}	# make headers
    header['User-Agent'] = user_agent
    if referer != None:
        header['Referer'] = referer
    try:
        req = urllib.request.Request(url, headers=header, method='GET')
        res = urllib.request.urlopen(req)
        blob = res.read()
        return blob
    except Exception as e:
        raise err.NetworkError('can not download with http GET on this url', url) from e

# TODO just support 'utf-8' encoding now
def dl_html(url, encoding='utf-8', user_agent='__default__', referer=None):
    '''
    download the URL and 
    return the raw html text
    '''
    blob = dl_blob(url, user_agent=user_agent, referer=referer)
    try:
        html_text = blob.decode(encoding)
        return html_text
    except Exception as e:
        er = err.DecodingError('decode html_text failed on this url', url)
        er.raw_blob = blob
        raise er from e

def dl_json(url, user_agent='__default__', referer=None):
    '''
    download the URL and 
    return info from the json text
    '''
    blob = dl_blob(url, user_agent=user_agent, referer=referer)
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
def dl_xml(url, encoding='utf-8', user_agent='__default__', referer=None):
    '''
    download the URL and 
    return info from the xml text
    '''
    blob = dl_blob(url, user_agent=user_agent, referer=referer)
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
    try:
        req = urllib.request.Request(url, headers=header, method=method, data=post_data)
        res = urllib.request.urlopen(req)
        blob = res.read()
        return blob	# without decode
    except Exception as e:
        er = err.NetworkError(method + ' to the url failed', url)
        er.post_data = post_data
        er.req_header = header
        raise er from e

# make post string for application/x-www-form-urlencoded
def make_post_str(post_data):
    s = ''
    for key, value in post_data.items():
        s += '&' + str(key) + '=' + str(value)
    return s[1:]	# remove first &

# end _net.py


