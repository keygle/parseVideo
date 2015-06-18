# gui.py, part for parse_video : a fork from parseVideo. 

# import

from .. import set_key

# class

# main window

class MainWin(object):
    
    # start create and show main window
    def start(self):
        # bind more event to Text
        root.bind(set_key.KEY_COPY_URLS, self._on_c_key)	# copy urls
        root.bind(set_key.KEY_PASTE_URL, self._on_url_entry_paste)
        root.bind(set_key.KEY_START_PARSE, self._on_return_key)
        t.bind('<Button-3>', self._on_main_text_menu)	# show main Text menu
        
    # end MainWin class

# end gui.py


