# parse.py, parse_video/pvdl/lib/

from . import err, conf, log
from . import call_sub

def parse(hd=None, enable_more=False):
    raw_url = conf.raw_url
    # INFO log
    log.i('call parse_video to parse URL \"' + raw_url + '\" ')
    pvinfo, raw_text = _do_parse(raw_url, hd=hd, enable_more=enable_more)
    print(raw_text)	# NOTE print parse_video raw output here
    # check fix_size
    if conf.FEATURES['fix_size']:
        pvinfo = _fix_size(pvinfo)
    conf.pvinfo = pvinfo	# save raw pvinfo
    
    return pvinfo	# done

def _do_parse(raw_url, hd=None, enable_more=False):
    # make parse_video args
    arg = []
    # check fix_unicode
    if conf.FEATURES['fix_unicode']:
        arg += ['--fix-unicode']	# TODO parse_video now not support this option
    # check hd
    if hd == None:	# parse formats
        arg += ['--min', str(1), '--max', str(0)]
    else:	# parse URLs
        arg += ['--min', str(hd), '--max', str(hd)]
    # check add more raw args
    if len(conf.raw_args) > 0:
        arg += ['--options-overwrite-once'] + conf.raw_args	# TODO parse_video now not support this option
    # check add enable_more
    if enable_more:
        arg = _check_add_enable_more(arg)
    # add raw_url at last
    arg += [raw_url]
    
    # call parse_video to do parse
    try:
        pvinfo, raw_text = call_sub.call_parsev(arg)
    except (err.CallError, err.DecodingError) as e:
        er = err.ConfigError('call', 'parse_video')
        raise er from e
    except err.PvdlError as e:
        log.e('call parse_video to do parse failed ')
        er = err.ParseError('call parse_video', arg)
        raise er from e
    except Exception as e:
        log.e('unknow call parse_video Error ')
        er = err.UnknowError('call', 'parse_video')
        raise er from e
    return pvinfo, raw_text	# OK

def _check_add_enable_more(raw):
    log.w('parse._check_add_enable_more() not finished ')
    # TODO
    return raw

def _fix_size(pvinfo):
    log.w('parse._fix_size() not finished ')
    # TODO
    return pvinfo

def _create_task():
    
    # TODO create task_info, NOTE task_info is modified from pvinfo
    
    # TODO
    pass

def _check_log_file():
    pass

# TODO
# end parse.py


