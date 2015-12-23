# network.py, parse_video/lib/_b/

# TODO support proxy

import json
import urllib.request
import xml.etree.ElementTree as ET

from .. import err, conf

def dl_blob(url, header={}):
    '''
    do http GET to download a file, just return the binary data
    '''
    # set default user_agent
    if not 'User-Agent' in header:
        header['User-Agent'] = conf.DEFAULT_USER_AGENT
    try:
        req = urllib.request.Request(url, headers=header, method='GET')
        res = urllib.request.urlopen(req)
        blob = res.read()
        return blob
    except Exception as e:
        er = err.NetworkError('can not http GET ', url)
        er.header = header
        raise er from e

def dl_html(url, header={}, encoding='utf-8', ignore_decode_err=False):
    '''
    http GET download a file, and decode it to text
    '''
    blob = dl_blob(url, header=header)
    try:
        if ignore_decode_err:
            text = blob.decode(encoding, 'ignore')
        else:
            text = blob.decode(encoding)
        return text
    except Exception as e:
        er = err.DecodingError('decode with \"' + encoding + '\" failed on URL ', url)
        er.blob = blob
        raise er from e

def dl_json(url, header={}):
    '''
    http GET one file, and parse json text. return json info result
    '''
    # NOTE json must use 'utf-8' encoding
    blob = dl_blob(url, header=header)
    try:
        text = blob.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('decode blob to json text with \"utf-8\" failed, URL ', url)
        er.blob = blob
        raise er from e
    try:
        info = json.loads(text)
        return info
    except Exception as e:
        er = err.ParseJSONError('parse json text failed, URL ', url)
        er.text = text
        raise er from e

# TODO now only support 'utf-8' encoding
def dl_xml(url, header={}, encoding='utf-8'):
    '''
    http GET download one file, parse xml text with xml.etree.ElementTree, return result
    '''
    text = dl_html(url, header=header, encoding=encoding)
    try:
        root = ET.fromstring(text)
        return root
    except Exception as e:
        er = err.ParseXMLError('parse xml text failed, URL ', url)
        er.text = text
        raise er from e

# http POST function
def post(url, method='POST', post_data=None, header={}):
    '''
    do http POST, return raw blob data
    '''
    try:
        req = urllib.request.Request(url, headers=header, method=method, data=post_data)
        res = urllib.request.urlopen(req)
        blob = res.read()
        return blob
    except Exception as e:
        er = err.NetworkError('post failed, method:URL ', method, url)
        er.post_data = post_data
        er.header = header
        raise er from e

# post with 'application/x-www-form-urlencoded' data
def post_form(url, header={}, post_data={}):
    post_data = make_post_str(post_data).encode('utf-8')
    header['Content-Type'] = 'application/x-www-form-urlencoded'
    return post(url, header=header, post_data=post_data)

# make post text for form
def make_post_str(post_data):
    s = ''
    for key, value in post_data.items():
        s += '&' + str(key) + '=' + str(value)	# TODO use form encode
    return s[1:]	# remove first '&' char

# end network.py


