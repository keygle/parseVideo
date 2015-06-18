# make_rename_list.py, part for parse_video : a fork from parseVideo. 

# make number length
def make_num_len(n, l=4):
    t = str(n)
    while len(t) < l:
        t = '0' + t
    return t

def clean_file_name(text, remove_chars='/|\\ ?	*<>:\'\"', replace_char='_'):
    to = remove_chars
    out = ''
    for i in text:
        if i in to:
            out += replace_char
        else:
            out += i
    # done
    return out

def make_part_name(hinfo):
    t = hinfo['title'] + '_' + hinfo['title_sub']
    t = clean_file_name(t)
    return t

# end make_rename_list.py


