# conf_default.py, part for parse_video : a fork from parseVideo. 
# conf_default: o/pvtkgui/conf_default: parse_video Tk GUI, default config, and ui text. 
# version 0.0.3.0 test201506181209
# author sceext <sceext@foxmail.com> 2009EisF2015, 2015.06. 
# copyright 2015 sceext
#
# This is FREE SOFTWARE, released under GNU GPLv3+ 
# please see README.md and LICENSE for more information. 
#
#    parse_video : a fork from parseVideo. 
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

# import

# global vars

# default config obj
default_conf = {
    'hd' : '2', 
    'xunlei_dl_path' : 'c:\\pvtkgui_dl\\', 
}

# support urls
SUPPORT_URL_RE = [
    '^http://[a-z]+\.iqiyi\.com/.+\.html', 
    '^http://www\.letv\.com/ptv/vplay/[0-9]+\.html', 
    
    # support for evparse
    '^http://tv\.sohu\.com/(19|20)[0-9]{6}/n[0-9]+\.shtml', 
    '^http://www\.hunantv\.com/v/2/[0-9]+/[a-z]/[0-9]+\.html', 
    '^http://v\.pptv\.com/show/[A-Za-z0-9]+\.html', 
]

watch_thread_sleep_time_s = 0.1	# sleep 100ms

# pvtkgui, UI text

main_win_init_text = [
    [None, '       请在 '], 
    ['gray', '( '], 
    ['big_blue', '↗'], 
    ['blue', ' 上方 '], 
    ['big_blue', '↗'], 
    ['gray', ' 右侧的)'], 
    [None, ' 文本框'], 
    ['gray', '中'], 
    [None, '输入 '], 
    ['red', '视频播放页面'], 
    ['gray', '的 '], 
    ['red_bold', 'URL'], 
    ['gray', '. \n'], 
    [None, '                点击 '], 
    ['white_blue', ' 开始解析 '], 
    [None, ' 按钮'], 
    ['gray', '或'], 
    [None, '按回车键 '], 
    ['gray', '开始解析. \n\n'], 
    ['h2', ' parse_video Tk GUI 2'], 
    ['red_bold', '          parse_video 图形界面\n'], 
    ['gray', '          version 0.2.0.0 test201506172051\n'], 
    [None, '\n'], 
    ['big_blue', '\n+'], 
    ['bold', ' hd 值 说明\n'], 
    [None, '  左侧上方的文本框, '], 
    ['white_blue', ' hd='], 
    ['blue', ' 数字'], 
    [None, ', 用于选择解析并输出哪种清晰度的视频文件 URL. \n'
        + '                              这样做可以加快解析速度. \n', 
    ], 
    ['blue', '  hd 值'], 
    [None, ' 请在解析结果中 查看. \n'], 
    ['big_blue', '\n+'], 
    ['bold', ' 操作说明\n'], 
    [None, '  鼠标中键点击 URL 输入文本框 '], 
    ['gray', '(上方右侧)'], 
    [None, ', 可以直接从剪切板粘贴 URL. \n'
        + '  按 F9 键或右键菜单, 可以直接复制解析结果中的全部 URL 到剪切板. '
        + '不复制其它文本. \n', 
    ], 
    ['red', '\n(抱歉, 尚未完成)'], 
    [None, '\n\n\n\n\n'], 
    [None, '更多帮助信息, 请见\n  '], 
    ['a', 'https://github.com/sceext2/parse_video/wiki/zh_cn-easy-guide'], 
    [None, '\n\n  如有更多问题, 需要讨论, 请\n\n'], 
    ['gray', '          加 qq 群 '], 
    ['bold', '飞驴友视频下载交流群'], 
    ['gray', ' 141712855'], 
    ['gray', '\n\ncopyright 2015 sceext <sceext@foxmail.com> 2015.06\n'], 
]

# TODO

# functions

# end conf_default.py


