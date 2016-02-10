# io_one_line_json.py, parse_video/lib/bridge/sandwich_bridge/sandwich_host/sandwich_io/

import json

def _encode(raw):
    tmp = raw[:]
    out = json.dumps(tmp) + '\n'
    return out

def _decode(raw):
    try:
        tmp = json.loads(raw)
        out = tmp[:]
    except Exception as e:
        out = ['err', 'io_one_line_json.decode', str(e)]
    return out

# io_one_line_json exports
encode = _encode	# encode(raw :[]) -> str
decode = _decode	# decode(raw :str) -> []
# end io_one_line_json.py


