# common.py, parse_video/lib/e/

import re

from .. import err, b
from ..b import log
from . import log_text

# extractor common parts
class ExtractorVar(object):
    # common static data, NOTE should be set by the extractor
    EXTRACTOR_ID = ''
    EXTRACTOR_NAME = ''
    SITE = ''
    SITE_NAME = ''
    
    RE_SUPPORT_URL = []
    METHOD_LIST = []
    RE_VID_LIST = {}
    TO_HD = {}
    
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
        
        out = self._add_more_data(out)
        return out	# add data done
    
    # NOTE do nothing by default
    def _add_more_data(self, raw):
        return raw
    # end ExtractorVar class

class ExtractorEntry(object):
    def __init__(self, var_):
        self.var = var_
    # init extractor.var
    def init(self):
        self.var.push()
        self.var._ = self.var.init()
        self.var.init_flag = True
    
    # extractor parse entry function, return lyyc_parsev struct
    def parse(self, raw_url, raw_arg='', raw_method=''):
        if not self.var.init_flag:
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
            self.var.pop()	# clean var data
            self.var.init_flag = False
        return pvinfo
    
    def _do_parse(self, raw_method):
        method, method_arg_text = b.split_raw_method(raw_method)
        # check method name
        worker = self._check_method(method)
        if worker == None:	# no such method
            raise err.ConfigError(log_text.entry_err_no_method(method))
        log.d(log_text.entry_log_use_method(method, method_arg_text))	# DEBUG log
        
        pvinfo = worker.parse(method_arg_text)
        return entry_add_more_info(pvinfo, self.var)
    
    # should be implemented by extractor
    def _check_method(self, method):
        raise NotImplementedError
    # end ExtractorEntry class


class ExtractorMethod(object):
    def __init__(self, var_):
        self.var = var_
        
        # for check_use_more
        self._more_data_list = [
            'vid_info', 	# default support vid_info for --more mode
        ]
        
        # NOTE do init
        self._init_data()
    
    # init before start parse
    def _init_data(self):
        pass	# default nothing todo
    
    # method parse entry function, default common parse process
    def parse(self, method_arg_text):
        self._check_use_more(method_arg_text)
        self._parse_arg(method_arg_text)
        
        vid_info = self._get_vid_info()
        pvinfo = self._get_video_info(vid_info)
        
        out = self._get_file_urls(pvinfo)
        # NOTE add extra process here
        out = self._extra_process(out)
        
        out = self._check_add_more_info(out)
        return out	# parse done
    
    # main parse stage
    def _check_use_more(self, method_arg_text):
        var = self.var
        def check_more_data(data_list):
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
        # reset flags before check
        var._['_use_more'] = False
        # check use more mode
        try:
            if check_more_data(self._more_data_list):
                # set flags
                var._['_use_more'] = True
                raw_more = var._['more']
        except Exception as e:
            pass	# NOTE ignore check more Error
        if not var._['_use_more']:
            return	# not use more, no more process
        # check method args match
        raw_method_arg = b.split_raw_method(raw_more['method'])[1]
        if raw_method_arg != method_arg_text:
            log.w('now method args ' + b.str_or_str(method_arg_text) + ' is different from old method args ' + b.str_or_str(raw_method_arg) + ' in more info ')
        # TODO check method name match
        log.o(log_text.method_enable_more())
        # end _check_use_more
    
    def _parse_arg(self, method_arg_text):
        # parse common args
        if method_arg_text != None:
            args = method_arg_text.split(',')
            for r in args:
                # process common method args
                if r == 'enable_more':
                    self.var._['enable_more'] = True
                else:	# parse rest args
                    if self._parse_arg_rest(r):	# unknow args
                        log.w('unknow method arg \"' + r + '\" ')
        # end _parse_arg
    
    def _get_vid_info(self):
        # check _use_more and get vid_info
        if self.var._['_use_more']:
            more_data = self.var._['more']['_data']
            vid_info = more_data['vid_info']
        else:
            try:
                vid_info = self._do_get_vid_info()
            except Exception as e:
                er = err.NotSupportURLError('get vid_info failed', self.var._['_raw_url'])
                raise er from e
        # set var._
        self.var._['_vid_info'] = vid_info
        # DEBUG log, got vid_info
        log.d(log_text.method_got_vid_info(vid_info))
        return vid_info
    
    def _do_get_vid_info(self):	# get vid_info from html page, without --more mode
        raw_url = self.var._['_raw_url']
        # INFO log, loading raw html page
        log.i(log_text.method_loading_page(raw_url))
        raw_html_text = self._load_page(raw_url)
        self.var._['_raw_page_html'] = raw_html_text
        
        # use re to get vid list from page html text
        vid_info = self._re_get_vid(raw_html_text)
        # fix vid_info
        out = self._fix_vid_info(vid_info)
        return out
    
    def _get_video_info(self, vid_info):
        raise NotImplementedError	# for sub class
    
    # NOTE by default, do nothing
    def _get_file_urls(self, pvinfo):
        return pvinfo
    def _extra_process(self, raw):
        return raw
    
    def _check_add_more_info(self, raw):
        # check enable_more and add info
        if self.var._['enable_more']:
            raw['_data'] = self._gen_more_data()
        return raw
    
    # sub parse stage
    def _parse_arg_rest(self, r):
        return True	# default nothing todo
    
    def _load_page(self, raw_url):
        # default just download raw page
        text = b.dl_html(raw_url)
        return text
    
    def _re_get_vid(self, raw_text):
        re_list = self.var.RE_VID_LIST
        out = {}
        for key, r in re_list.items():
            one = re.findall(r, raw_text)[0]
            # check empty result
            if (one == None) or (one == ''):
                raise err.ParseError('vid_info \"' + key + '\" empty', one)
            out[key] = one
        return out
    
    def _fix_vid_info(self, raw):
        return raw	# default nothing todo
    
    def _parse_raw_first(self, first):
        # TODO may be more process here
        try:
            pvinfo = self._do_parse_first(first)
        except Exception as e:
            er = err.MethodError(log_text.method_err_parse_raw_first())
            raise er from e
        method_sort_video(pvinfo)
        return pvinfo
    
    # NOTE keep for sub class
    def _make_first_url(self):
        pass
    def _do_parse_first(self, first):
        pass
    
    def _gen_more_data(self):
        out = {}
        # NOTE default should save vid_info
        out['vid_info'] = self.var._['_vid_info']
        return out
    # end ExtractorMethod class


## extractor common functions

# entry

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

# method

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
    method_count_videos(pvinfo)
    method_select_hd(pvinfo, var)
    method_select_file(pvinfo, var)
    return pvinfo

def method_sort_video(pvinfo):
    # sort video by hd
    pvinfo['video'].sort(key= lambda x: x['hd'], reverse=True)

def method_count_videos(pvinfo):
    for v in pvinfo['video']:
        method_count_one_video(v)

# NOTE this count method does not much Error process (simple)
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


# map_do() network functions

# TODO just keep this here
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


