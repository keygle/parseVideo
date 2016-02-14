# __init__.py, parse_video/lib/e/letv/o/m3u8_encrypt/
# TODO support m3u8_encrypt.c

try:    # m3u8_encrypt2 is faster than m3u8_encrypt
    from . import m3u8_encrypt2 as m3u8_encrypt
except Exception:
    from . import m3u8_encrypt

# end __init__.py


