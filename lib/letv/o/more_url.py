# -*- coding: utf-8 -*-
# more_url.py, part for parse_video : a fork from parseVideo. 
# lib/letv/o: parse more letv final url, by method from piaopiao. 

# import

from ... import base

# function

def parse_more_url(domain, dispatch_format_id, format_type, flag_debug=False):
    # make more json info url
    raw_url = get_more_json_url(domain[0], dispatch_format_id[0], format_type)
    # DEBUG info
    if flag_debug:
        print('lib.letv.o: DEBUG: more_url: get one more url [' + format_type + '] \"' + raw_url + '\"')
    
    # parse_more info json
    more_info = parse_more_json(raw_url)
    # done
    return more_info

def get_more_json_url(domain, dispatch_format_id, format_type):
    # modify dispatch_format_id
    dispatch_s = dispatch_format_id.split('?', 1)
    
    # split options
    options = dispatch_s[1].split('&')
    option_a = {}
    for o in options:
        o_s = o.split('=', 1)
        option_a[o_s[0]] = o_s[1]
    
    # modify options
    option_a['tss'] = 'no'
    option_a['splatid'] = '1401'
    
    # concat url
    before = domain + dispatch_s[0] + '?'
    after = ''
    for o in option_a:
        after += '&' + o + '=' + option_a[o]
    # remove first &
    after = after[1:]
    
    out = before + after
    
    # add more options
    # NOTE add &format=1&sign=letv&expect=3000&rateid=1080p
    out += '&format=1&sign=letv&expect=3000&rateid=' + format_type
    
    # done
    return out

def parse_more_json(raw_url):
    
    # add headers
    header = {}
    header['Content-Type'] = 'application/x-www-form-urlencoded'
    header['Accept'] = 'application/json'
    user_agent0 = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1) Web-Sniffer/1.0.24'
    
    # load json
    raw = base.get_json_info(raw_url, header=header, user_agent=user_agent0, method='POST')
    
    out = {}
    # translate info struct
    out['ext'] = 'mp4'	# NOTE letv format should be mp4
    
    out['url'] = raw['location']
    
    # add more url
    out['url_more'] = []
    more = out['url_more']
    
    for i in raw['nodelist']:
        one = {}
        one['name'] = i['name']
        one['url'] = i['location']
        more.append(one)
    
    # done
    return out

# end more_url.py


