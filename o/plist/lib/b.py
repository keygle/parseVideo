# b.py, parse_video/o/plist/lib/

import os, sys
import math, json
import datetime
import urllib.request
import xml.etree.ElementTree as ET

import htmldom.htmldom

from . import err, conf


# deep clone a object with json
def json_clone(raw):
    out = json.loads(json.dumps(raw))
    return out

# decoding functions
def decode_utf8(blob, ignore_err=False):
    try:
        if ignore_err:
            out = blob.decode('utf-8', 'ignore')
        else:
            out = blob.decode('utf-8')
    except Exception as e:
        er = err.DecodingError('decode blob to text with utf-8 failed')
        er.blob = blob
        raise er from e
    return out

# parse functions
def parse_json(text):
    try:
        out = json.loads(text)
    except Exception as e:
        er = err.ParseJSONError('parse json text failed')
        er.text = text
        raise er from e
    return out

def parse_xml(text):
    try:
        out = ET.fromstring(text)
    except Exception as e:
        er = err.ParseXMLError('parse xml text failed')
        er.text = text
        raise er from e
    return out

def parse_html(text):	# use htmldom to create dom object
    try:
        dom = htmldom.htmldom.HtmlDom()
        root = dom.createDom(text)
    except Exception as e:
        er = err.ParseHTMLError('use htmldom to parse html text failed')
        er.text = text
        raise er from e
    return root

# network functions
def dl_blob(url, header=None):
    headers={}
    if header != None:
        headers=header
    req = urllib.request.Request(url, headers=headers, method='GET')
    # TODO support timeout
    try:
        res = urllib.request.urlopen(req)
        out = res.read()
    except Exception as e:
        er = err.NetworkError('can not http GET', url)
        er.header = header
        raise er from e
    return out	# return raw blob

# exports network functions
def dl_html(url, header=None):
    try:
        blob = dl_blob(url, header=header)
        text = decode_utf8(blob, ignore_err=True)
        dom = parse_html(text)
    except Exception as e:
        er = err.NetworkError('dl html failed', url)
        er.header=header
        raise er from e
    out = {
        'blob' : blob, 
        'text' : text, 
        'dom' : dom, 
    }
    return out

def dl_json(url, header=None):
    try:
        blob = dl_blob(url, header=header)
        text = decode_utf8(blob)
        out = parse_json(text)
    except Exception as e:
        er = err.NetworkError('dl json failed', url)
        er.header=header
        raise er from e
    return out

def dl_xml(url, header=None):
    try:
        blob = dl_blob(url, header=header)
        text = decode_utf8(blob)
        out = parse_xml(text)
    except Exception as e:
        er = err.NetworkError('dl xml failed', url)
        er.header=header
        raise er from e
    return out


# time functions
def get_now():
    return datetime.datetime.today().utcnow()

def print_iso_time(now=None):
    if now == None:
        now = get_now()
    out = now.isoformat() + 'Z'
    return out

# path functions

# join paths
def pjoin(*k, **kk):
    raw = os.path.join(*k, **kk)
    out = os.path.normpath(raw)
    return out

def replace_filename_bad_char(raw, replace=conf.FILENAME_REPLACE):
    bad_chars = conf.FILENAME_BAD_CHAR
    out = ('').join([i if not i in bad_chars else replace for i in raw])
    return out


# end b.py


