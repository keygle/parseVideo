# common.py, parse_video/o/plist/lib/, extractor common code

from . import err, b, conf, log

class ExtractorVar(object):
    pass

class ExtractorEntry(object):
    
    def __init__(self, var):
        self.var = var
    
    # parse entry function
    def parse(self, url):
        plinfo = self._do_parse(url)
        # add more info
        plinfo['extractor'] = self.var.EXTRACTOR_ID
        plinfo['info']['site'] = self.var.SITE
        plinfo['info']['site_name'] = self.var.SITE_NAME
        plinfo['info']['url'] = url	# add raw_url
        
        return plinfo	# done
    
    def _do_parse(self, url):
        raise NotImplementedError
    # end Extractor class

def load_page(url):
    log.i('loading page \"' + url + '\" ')
    out = b.dl_html(url)
    return out

# end common.py


