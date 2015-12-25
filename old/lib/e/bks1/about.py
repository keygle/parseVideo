# about.py, parse_video/lib/e/bks1
# LICENSE GNU GPLv3+ sceext 
# version 0.0.2.0 test201509271522

from . import var

def get_info():
    out = {}
    out['id'] = var.EXTRACTOR_ID
    out['version'] = THIS_EXTRACTOR_VERSION
    out['name'] = var.EXTRACTOR_NAME
    out['method'] = [
        'pc_flash_gate', 
        # TODO NOTE now only support one method
    ]
    out['help'] = HELP_TEXT
    return out

# more data

THIS_EXTRACTOR_VERSION = 'parse_video extractor bks1 version 0.4.0.0 test201509271516'

HELP_TEXT = '''
(help info for extractor bks1 not finished)
'''

# end about.py


