# -*- coding: utf-8 -*-
# io_one_line_only.py, pass many text in only one line text, sceext <sceext@foxmail.com> 
# LICENSE GNU GPLv3+ 
# version 0.1.1.0 test201509281252

# io encode function
def encode(raw_text_list=[]):
    raw = raw_text_list.copy()
    # check null list
    if len(raw) < 1:
        return ''
    # pre-process each raw text
    for i in range(len(raw)):
        t = raw[i]
        # process this text
        
        # keep all '\' chars to be safe
        t = t.replace('\\', '\\\\')
        # NOTE fix '\r', or '\r\n'
        t = t.replace('\r\n', '\n')
        t = t.replace('\r', '\n')
        # process multi-lines text
        t = t.replace('\n', '\\n')
        
        # process one text done
        raw[i] = t
    # join all text to finish encode
    out = ('\\0').join(raw)
    out += '\\0'	# add one more \0 after last line
    # done
    return out

# io decode function
def decode(raw_text=''):
    # check null decode
    if raw_text == '':
        return []
    # normal decode, should scan each char
    out = []
    flag_ = False
    t = ''
    for c in raw_text:
        # check flag
        if flag_:
            flag_ = False	# turn off flag first
            # check chars
            if c == '\\':
                t += '\\'	# should be \ char
            elif c == 'n':	# should be '\n' char
                t += '\n'
            elif c == '0':	# \0, should start a new text
                out.append(t)
                t = ''	# reset text
            else:	# as a normal char
                t += c
        else:	# check set flag
            if c == '\\':
                flag_ = True	# should turn on flag
            else:
                t += c	# append as a normal char
    # NOTE do not add last line
    return out	# done

# end io_one_line_only.py


