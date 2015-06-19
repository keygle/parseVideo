# -*- coding: utf-8 -*-
# make_name.py, for parse_video Tk GUI, sceext <sceext@foxmail.com> 2009EisF2015, 2015.06 

# 说明: 此文件可用来更改 parse_video 图形界面 调用 迅雷 下载时, 生成的 文件名

# 下面这个 函数 "make()", 用于生成 文件名
#	函数参数列表及其含义说明
#
#	title		视频标题, 比如 少年四大名捕未删减版第44集
#	title_sub	小标题, 比如 决胜归来大团圆
#	title_no	集数, 电视剧的第几集, 比如 44
#	title_short	视频短标题, 比如 少年四大名捕未删减版
#
#	site		网站名称, 比如 爱奇艺
#		说明: 以上信息来源网页 http://www.iqiyi.com/v_19rroj1k0g.html
#
#	part_i		分段文件序号
#	ext		文件扩展名
#
def make(title, title_sub, title_no, title_short, site, part_i, num_len, ext):
    
    # 以下生成数字, 集数 和 分段文件序号, 可以更改最小数字长度
    
    # 下面生成 集数 数字, 最小数字长度 默认 是 4, 请修改下面一行
    title_no = num_len(title_no, 4)
    
    # 下面生成 分段文件序号 数字, 最小数字长度 默认 是 4, 请修改下面一行
    part_i = num_len(part_i, 4)
    
    # 下面一行, name 就是最终 生成的 文件名
    name = '_' + title_no + '_' + title + '_' + title_sub + '_' + site + '_' + part_i
    
    # 下面一行, 为文件名添加扩展名
    name += ext
    
    # 上面的默认情况如下, 生成的文件名格式类似
    # _0044_少年四大名捕未删减版第44集_决胜归来大团圆_0001.flv
    # _0002_花千骨第2集_灵虫糖宝初降世_0001.flv
    
    return name

# end make_name.py, 2015-06-19 13:40 GMT+0800 CST


