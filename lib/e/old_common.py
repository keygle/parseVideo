# common.py, parse_video/lib/e/

import re

from .. import err, b
from ..b import log
from . import log_text

# extractor common parts
class ExtractorVar(object):
    def __init__(self):
        self.__ = {}	# NOTE this object not change
        self._old = []
        
        self.init_flag = False
    @property
    def _(self):
        return self.__
    @_.setter
    def _(self, value):
        self.__.clear()
        self.__.update(value)
    
    # base var functions
    def push(self):
        self._old.append(self._.copy())
    def pop(self):
        return self._old.pop()
    
    # extractor.var common data
    def init(self):
        out = {}
        # set default values
        out['raw_arg'] = ''
        out['raw_method'] = ''
        
        out['more'] = None
        # config items
        out['hd_min'] = None
        out['hd_max'] = None
        out['i_min'] = None
        out['i_max'] = None
        
        out['pool_size'] = {}
        out['enable_more'] = False	# add more info in output pvinfo
        out['_use_more'] = False	# --more mode enabled flag
        # private data
        out['_raw_url'] = ''
        out['_raw_page_html'] = ''
        out['_vid_info'] = None
        
        # add data done
        return out
    # end ExtractorVar class

class ExtractorEntry(object):
    def __init__(self, var_):
        self.var = var_
    # init extractor.var
    def init(self):
        self.var.var.push()
        self.var._ = self.var.var.init()
        self.var.var.init_flag = True
    
    # extractor parse entry function, return lyyc_parsev struct
    def parse(self, raw_url, raw_arg='', raw_method=''):
        if not self.var.var.init_flag:
            self.init()
        # set var data
        self.var._['raw_arg'] = raw_arg
        self.var._['raw_method'] = raw_method
        self.var._['_raw_url'] = raw_url
        # DEBUG log
        log.d('extractor ' + self.var.EXTRACTOR_ID + ': parse, raw_url = \"' + raw_url + '\", raw_arg = \"' + raw_arg + '\", raw_method = \"' + raw_method + '\" ')
        try:
            pvinfo = self._do_parse(raw_method)
        except err.PVError:
            raise
        except Exception as e:
            er = err.UnknowError('unknow extractor Error', self.var.EXTRACTOR_ID)
            raise er from e
        finally:
            self.var.var.pop()	# clean var data
            self.var.var.init_flag = False
        return pvinfo
    
    # should be implemented by extractor
    def _do_parse(self, raw_method):
        raise NotImplementedError
    # end ExtractorEntry class

## extractor common functions

# extractor.entry

def entry_add_more_info(pvinfo, var):
    # add more info to pvinfo
    pvinfo['extractor_name'] = var.EXTRACTOR_NAME
    # NOTE use raw extractor args
    pvinfo['extractor'] = var._['raw_arg']
    pvinfo['method'] = var._['raw_method']
    
    pvinfo['info']['site'] = var.SITE
    pvinfo['info']['site_name'] = var.SITE_NAME
    pvinfo['info']['url'] = var._['_raw_url']
    return pvinfo

# extractor.method_pc_flash_gate

def method_parse_method_args(method_arg_text, var, rest):
    if method_arg_text != None:
        args = method_arg_text.split(',')
        for r in args:
            # process common method args
            if r == 'enable_more':
                var._['enable_more'] = True
            else:	# use rest to process args
                if rest(r):	# unknow args
                    log.w('unknow method arg \"' + r + '\" ')
    # done parse method arg_text

# check use more mode
def method_check_use_more(var, data_list=[]):
    try:
        return _method_do_check_use_more(var, data_list)
    except Exception as e:
        # TODO more Error process
        return False

def _method_do_check_use_more(var, data_list):
    # check more data exist
    if var._['more'] == None:
        return False	# no more data
    raw_more = var._['more']
    if not '_data' in raw_more:
        return False
    # check extractor match
    extractor_id = b.split_raw_extractor(raw_more['extractor'])[0]
    if extractor_id != var.EXTRACTOR_ID:
        return False	# not this extractor
    # check url match
    if var._['_raw_url'] != raw_more['info']['url']:
        return False
    # check needed data exist
    raw_data = raw_more['_data']
    for d in data_list:
        if not d in raw_data:
            return False
    return True	# check pass, use more mode

def method_more_check_method(method_arg_text, raw_more):
    # TODO check method match
    # check method args match
    raw_method_arg = b.split_raw_method(raw_more['method'])[1]
    if raw_method_arg != method_arg_text:	# WARNING log
        log.w('now method args ' + b.str_or_str(method_arg_text) + ' is different from old method args ' + b.str_or_str(raw_method_arg) + ' in more info ')

def method_simple_check_use_more(var, method_arg_text, data_list=[]):
    if not method_check_use_more(var, data_list):
        return None	# not use more
    # set flags
    var._['_use_more'] = True
    raw_more = var._['more']
    # [ OK ] log
    log.o(log_text.method_enable_more())
    # check method
    method_more_check_method(method_arg_text, raw_more)
    return raw_more

def method_more_simple_get_vid_info(var, f):
    raw_more = var._['more']
    if not var._['_use_more']:
        vid_info = f()
    else:
        raw_data = raw_more['_data']
        vid_info = raw_data['vid_info']
        # set var._
        var._['_vid_info'] = vid_info
    return vid_info

# get vid info
def method_get_vid_info(raw_html_text, var, do_get):
    try:
        return do_get(raw_html_text)
    except Exception as e:
        er = err.NotSupportURLError('get vid info failed', var._['_raw_url'])
        raise er from e

def method_vid_re_get(raw_html_text, re_list):
    out = {}
    for key, r in re_list.items():
        one = re.findall(r, raw_html_text)[0]
        # check empty result
        if (one == None) or (one == ''):
            raise err.ParseError('vid_info \"' + key + '\" empty', one)
        out[key] = one
    return out

def method_get_size_px(x=-1, y=-1):
    out = [-1, -1]
    try:
        out[0] = int(x)
    except Exception:
        pass
    try:
        out[1] = int(y)
    except Exception:
        pass
    return out

# count and select

def method_simple_count_and_select(pvinfo, var):
    method_sort_video(pvinfo)
    method_simple_count(pvinfo)
    method_select_hd(pvinfo, var)
    method_select_file(pvinfo, var)
    return pvinfo

def method_sort_video(pvinfo):
    # sort video by hd
    pvinfo['video'].sort(key= lambda x: x['hd'], reverse=True)

def method_simple_count(pvinfo):
    for v in pvinfo['video']:
        method_count_one_video(v)

# NOTE this count method does not much Error process
def method_count_one_video(v):
    v['size_byte'] = 0
    v['time_s'] = 0
    v['count'] = len(v['file'])
    for f in v['file']:
        v['size_byte'] += f['size']
        v['time_s'] += f['time_s']
    v['time_s'] = round(v['time_s'], 3)

def method_select_hd(pvinfo, var):
    hd_min = var._['hd_min']
    hd_max = var._['hd_max']
    for v in pvinfo['video']:
        if ((hd_min != None) and (v['hd'] < hd_min)) or ((hd_max != None) and (v['hd'] > hd_max)):
            v['file'] = []	# clear video file list

def method_select_file(pvinfo, var):
    i_min = var._['i_min']
    i_max = var._['i_max']
    for v in pvinfo['video']:
        for i in range(len(v['file'])):
            if ((i_min != None) and (i < i_min)) or ((i_max != None) and (i > i_max)):
                v['file'][i]['url'] = ''	# clear file URL

# extractor.method.parse, common parse functions

def parse_load_page_and_get_vid(var, get_vid_info=None):
    raw_url = var._['_raw_url']
    # INFO log, loading raw html page
    log.i(log_text.method_loading_page(raw_url))
    raw_html_text = b.dl_html(raw_url)
    var._['_raw_page_html'] = raw_html_text
    
    if get_vid_info == None:
        vid_info = parse_simple_get_vid_info(raw_html_text, var)
    else:
        vid_info = get_vid_info(raw_html_text)
    var._['_vid_info'] = vid_info
    log.d(log_text.method_got_vid_info(vid_info))
    return vid_info

def parse_simple_get_vid_info(raw_html_text, var):
    def do_get(raw_html_text):
        return method_vid_re_get(raw_html_text, var.RE_VID_LIST)
    return method_get_vid_info(raw_html_text, var, do_get)

def parse_raw_first(first, do_parse):
    try:
        pvinfo = do_parse(first)
    except Exception as e:
        er = err.MethodError(log_text.method_err_parse_raw_first())
        raise er from e
    method_sort_video(pvinfo)
    return pvinfo

# map_do() network functions

def simple_get_file_urls(pvinfo, worker, msg='', pool_size=1):
    # TODO maybe retry here
    # make todo list
    todo = []
    i = 0
    for v in pvinfo['video']:
        for f in v['file']:
            if f['url'] != '':
                one = {}
                one['i'], i = i, i + 1	# add index number for DEBUG
                one['f'] = f
                todo.append(one)
    # INFO log
    log.i(msg + ', count ' + str(len(todo)) + ', pool_size = ' + str(pool_size) + ' ')
    def _worker(raw):
        i = raw['i']
        log.d('start get index ' + str(i) + ', url \"' + raw['f']['url'] + '\" ')
        result = worker(raw['f'], i)
        log.d('[done] got index ' + str(i) + ' ')
        return result
    result = b.map_do(todo, worker=_worker, pool_size=pool_size)
    log.d('got files done. ')
    # set back result
    i = 0
    for v in pvinfo['video']:
        for j in range(len(v['file'])):
            if v['file'][j]['url'] != '':
                v['file'][j], i = result[i], i + 1
    return pvinfo	# done

# end common.py


