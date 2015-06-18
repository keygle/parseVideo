# make_rename_list.py, part for parse_video : a fork from parseVideo. 

def make_part_name(hinfo):
    t = hinfo['title'] + '_' + hinfo['title_sub']
    t = clean_file_name(t)
    return t

# end make_rename_list.py


