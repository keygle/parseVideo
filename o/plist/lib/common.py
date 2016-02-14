# common.py, parse_video/o/plist/lib/, extractor common code

from . import err, b, conf, log

class ExtractorVar(object):
    
    # runtime vars data
    _extractor = None
    _method = None
    
    # keep for sub class
    EXTRACTOR_ID = None
    EXTRACTOR_NAME = None
    SITE = None
    SITE_NAME = None
    # end ExtractorVar class

class ExtractorEntry(object):
    
    def __init__(self, var):
        self.var = var
    
    # parse entry function
    def parse(self, url, extractor=None, method=None):
        # parse method args
        self.var._extractor = extractor
        self.var._method = method
        method_name = self._parse_method_args()
        
        plinfo = self._do_parse(url, method_name=method_name)
        # add more info
        plinfo['extractor'] = self.var.EXTRACTOR_ID
        plinfo['info']['site'] = self.var.SITE
        plinfo['info']['site_name'] = self.var.SITE_NAME
        plinfo['info']['url'] = url	# add raw_url
        
        return plinfo	# done
    
    def _parse_method_args(self):
        method_name, raw_args = b.split_method(self.var._method)
        if raw_args != None:
            args = raw_args.split(',')
            for a in args:
                if self._parse_rest_arg(a):
                    log.w('unknow method arg \"' + a + '\" ')
        return method_name
    
    def _parse_rest_arg(self, r):
        return True	# default nothing todo
    
    def _do_parse(self, url, method_name=None):
        raise NotImplementedError
    # end Extractor class

def load_page(url):
    log.i('loading page \"' + url + '\" ')
    out = b.dl_html(url)
    return out

# end common.py


