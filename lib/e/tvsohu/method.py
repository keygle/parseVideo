# method.py, parse_video/lib/e/tvsohu/

from ... import err, b
from ...b import log
from .. import common, log_text

from .var import var
from .o import main

class Method(common.ExtractorMethod):   # common method class for extractor tvsohu
    def _init_data(self):
        self._more_data_list += [
            'raw_first_json', 
        ]
        # NOTE for sub class
        self._gen_one_before_url = None # should be a function
    
    def _gen_more_data(self):
        out = super()._gen_more_data()
        # add first_json info
        out['raw_first_json'] = var._['_raw_first_json']
        return out
    
    def _load_page(self, raw_url):
        raw_blob = b.dl_blob(raw_url)
        # NOTE the html encoding is not 'utf-8'
        html_text = raw_blob.decode('utf-8', 'ignore')
        return html_text
    
    def _get_video_info(self, vid_info):
        # TODO support fast_parse here
        # download all raw first jsons
        raw_list = self._get_first_jsons(vid_info)
        # do parse first json info
        out = {}
        out['video'] = []
        for vid, raw in raw_list.items():
            one = self._do_parse_first(raw, vid)
            if not 'info' in out:
                out['info'] = one['info']
            out['video'].append(one['v'])
        common.method_sort_video(out)
        # NOTE count and select here
        return common.method_simple_count_and_select(out, var)
    
    def _make_first_url(self, vid_info):
        first_url = main.gen_first_url(vid_info['vid'])
        log.o(log_text.method_got_first_url(first_url))
        return first_url
    
    def _get_first_jsons(self, vid_info):
        # check use_more to get first_json info
        if var._['_use_more']:
            more_data = var._['more']['_data']
            var._['_raw_first_json'] = more_data['raw_first_json']
            return var._['_raw_first_json']
        # TODO support fast_parse here
        # start download first jsons
        first_url = self._make_first_url(vid_info)
        first = b.dl_json(first_url)
        
        vid = vid_info['vid']
        var._['_raw_first_json'][int(vid)] = first
        # parse raw first, get other vids, and download other first info jsons
        vid_list = self._do_parse_first(first, vid)['vid_list']
        # make todo list
        todo = []
        for name, value in vid_list.items():	# NOTE vid == 0 is null
            if (not int(value) in var._['_raw_first_json']) and (int(value) != 0):
                one = {}
                one['name'] = name
                one['vid'] = value
                one['url'] = main.gen_first_url(value)
                todo.append(one)
        pool_size = var._['pool_size']['get_first']
        # INFO log
        log.i('getting video info, count ' + str(len(todo)) + ', pool_size = ' + str(pool_size) + ' ')
        result = b.map_do(todo, worker=_dl_one_first, pool_size=pool_size)
        log.d('got video info (first) done ')
        # save more raw_first_json
        for r in result:
            var._['_raw_first_json'][int(r['vid'])] = r['json']
        # get first json info done
        return var._['_raw_first_json']
    
    def _do_parse_first(self, first, vid):
        return _do_parse_one_first(first, int(vid), self._gen_one_before_url)
    # end Method class

# base parse functions

def _dl_one_first(info):
    log.d('getting first, name ' + b.str_or_str(info['name']) + ', vid ' + b.str_or_str(info['vid']) + ', url \"' + info['url'] + '\" ')
    raw = b.dl_json(info['url'])
    log.d('[done] got name ' + b.str_or_str(info['name']) + ' ')
    out = {}
    out['vid'] = info['vid']
    out['json'] = raw
    return out

# parse first info

def _do_parse_one_first(raw, vid, gen_one_before_url):
    # check first code
    if raw['status'] != var._FIRST_OK_CODE:
        raise err.MethodError(log_text.method_err_first_code(raw['status'], var))
    out = {}
    data = raw['data']
    # get base video info
    info = {}
    info['title'] = data['tvName']
    info['title_sub'] = data['subName']
    info['title_no'] = data['num']
    out['info'] = info
    # get vid list
    name_list = var._VID_NAME_LIST
    vid_list = {}
    for i in name_list:
        vid_list[i] = data[i]
    out['vid_list'] = vid_list
    # get one video format info
    v = {}
    v['size_px'] = [
        data['width'], 
        data['height'], 
    ]
    v['format'] = 'mp4'	# NOTE the file format should be mp4
    # get hd
    vid_name = None
    for vid_type, vid_value in vid_list.items():
        if vid_value == vid:
            vid_name = vid_type
            break
    if vid_name == None:
        raise err.MethodError('can not get vid_type from vid ' + b.str_or_str(vid) + ' ')
    v['hd'] = var.TO_HD[vid_name]
    # NOTE add quality here
    quality = var._VID_NAME_LIST[vid_name]
    if quality != None:
        v['quality'] = quality
    # gen file before urls
    tvid, ch = raw['tvid'], data['ch']
    su = data['su']
    clipsDuration = data['clipsDuration']
    clipsBytes = data['clipsBytes']
    v['file'] = []
    for i in range(len(su)):
        one = {}
        one['size'] = clipsBytes[i]
        one['time_s'] = clipsDuration[i]
        # gen file before URL
        one['url'] = gen_one_before_url(su[i], vid, tvid, ch)
        v['file'].append(one)
    out['v'] = v
    out['vid'] = vid
    return out

# end method.py


