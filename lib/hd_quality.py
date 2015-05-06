# -*- coding: utf-8 -*-
# hd_quality.py, part for parse_video : a fork from parseVideo. 
# evparse:lib/hd_quality: definition of video hd and quality. 
# version 0.1.0.0 test201505062235
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.05. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    evparse : EisF Video Parse, evdh Video Parse. 
#    Copyright (C) 2015 sceext <sceext@foxmail.com> 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# description								sites
# hd	quality		english			note			iqiyi				
#
# -8			(reserved)									
# -7	无语渣		very very bad		清晰度 (分辨率) 太低
# -6	极其渣		very very bad		清晰度 (分辨率) 太低
# -5	渣的受不了	very very bad		清晰度 (分辨率) 太低
# -4	超渣		very very bad		清晰度 (分辨率) 太低
# -3	渣清		very very bad		清晰度 (分辨率) 太低	极速	LIMIT, topspeed
# -2	超低清		very low		清晰度 (分辨率) 太低	流畅	NONE, none
# -1	低清		low			较低清晰度		标清	STANDARD, standard	
#
# 0	普清		normal			普通清晰度		高清	HIGH, high		
# 1	高清		high			较高清晰度		超清	SUPER, super
# 2	720p		1280 x 720		分辨率约 1280 x 720	720p	SUPER_HIGH, super-high	
# 3			(reserved)
# 4	1080p		1920 x 1080		分辨率约 1920 x 1080	1080p	FULL_HD, fullhd		
# 5	高码1080p	high bitrate 1080p	高码率 1080p
# 6			(reserved)
# 7	4K		4096 x 2160		分辨率约 4096 x 2160	4K	FOUR_K, 4k		
# 8	高码4K		high bitrate 4K		高码率 4K						
# 9			(reserved)
# 10			(reserved)
# 11	8K		8192 x 4320		分辨率约 8192 x 4320
# 12			(reserved)

# definition

defi = {}

HD_MIN = -7	# min hd number

defi['-8'] = ''	# reserved
defi['-7'] = '无语渣'
defi['-6'] = '极其渣'
defi['-5'] = '渣的受不了'
defi['-4'] = '超渣'
defi['-3'] = '渣清'
defi['-2'] = '超低清'
defi['-1'] = '低清'

defi['0'] = '普清'
defi['1'] = '高清'
defi['2'] = '720p'
defi['3'] = ''	# reserved
defi['4'] = '1080p'
defi['5'] = '高码1080p'
defi['6'] = ''	# reserved
defi['7'] = '4K'
defi['8'] = '高码4K'
defi['9'] = ''	# reserved
defi['10'] = ''	# reserved
defi['11'] = '8K'
defi['12'] = ''	# reserved

HD_MAX = 8	# max hd number

# functions
def get(hd):
    return defi[str(hd)]

# end hd_quality.py


