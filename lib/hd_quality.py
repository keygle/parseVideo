# hd_quality.py, parse_video/lib
# LICENSE GNU GPLv3+ sceext 
# version 0.0.1.0 test201509271940

'''
parse_video/lib/hd_quality.py
    definition of video hd and quality 

description

 hd	quality		english			note

 -8			(reserved)
 -7	无语渣		very very bad		清晰度 (分辨率) 太低
 -6	极其渣		very very bad		清晰度 (分辨率) 太低
 -5	渣的受不了	very very bad		清晰度 (分辨率) 太低
 
 -4	超渣		very very bad		清晰度 (分辨率) 太低
 -3	渣清		very very bad		清晰度 (分辨率) 太低
 -2	超低清		very low		清晰度 (分辨率) 太低
 -1	低清		low			较低清晰度
 
 0	普清		normal			普通清晰度
 1	高清		high			较高清晰度
 
 2	720p		1280 x 720		分辨率约 1280 x 720
 3			(reserved)
 4	1080p		1920 x 1080		分辨率约 1920 x 1080
 5	高码1080p	high bitrate 1080p	高码率 1080p
 
 6			(reserved)
 7	4K		4096 x 2160		分辨率约 4096 x 2160
 8	高码4K		high bitrate 4K		高码率 4K
 
 9			(reserved)
 10			(reserved)
 11	8K		8192 x 4320		分辨率约 8192 x 4320
 12			(reserved)

'''

HD_MIN = -4	# min hd number
HD_MAX = 8	# max hd number

# real define, from hd to video quality text
defi = {
    -8 : '', 	# reserved
    -7 : '无语渣', 
    -6 : '极其渣', 
    -5 : '渣的受不了', 
    
    -4 : '超渣', 
    -3 : '渣清', 
    -2 : '超低清', 
    -1 : '低清', 
    
    0 : '普清', 
    1 : '高清', 
    
    2 : '720p', 
    3 : '', 	# reserved
    4 : '1080p', 
    5 : '高码1080p', 
    
    6 : '', 	# reserved
    7 : '4K', 
    8 : '高码4K', 
    
    9 : '', 	# reserved
    10 : '', 	# reserved
    11 : '8K', 
    12 : '', 	# reserved
}

def get(hd):
    '''
    convert hd to video quality
    '''
    return defi[int(hd)]

# end hd_quality.py


