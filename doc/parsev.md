<!-- parsev.md, parse_video/doc/, <https://github.com/sceext2/parse_video>
   - language: Chinese (zh_cn) 
   - version 0.0.8.0 test201512312024
  -->

parse_video version 0.5.2.2

# parse_video : 小而精 的 纯解析 程序


## 已支持网站 (4)

1. 271 (`4K`, w, `bks1`, *flv*)
2. letv (`1080p`, `letv`, *ts*) (m3u8)
3. hunantv (`720p`, `hunantv`, *m3u8*)
4. tvsohu (`4K`, *h265*, `tvsohu`, *mp4*)


## 支持网站 限制

+ 主要支持 *中国* 的大型视频网站. 
  
  其它国家的 一般 不考虑. 

+ 支持 *少数* 网站, 但力求达到 *优质* 支持. 

+ **高清** 支持: 
  
  + *至少* `720p` 画质 (*分辨率* 约为 `1280 x 720`)
  
  + *大多数* 支持 `1080p` 画质 (约 `1920 x 1080`)
  
  + *少数* 支持 `4K` (约 `3840 x 2160`) 和 `h265` 
  
  + 清晰度 (画质) *太低* 的 *不考虑* 支持


## -> version 0.5.x 特性

+ 原生提供 `lyyc` 插件接口. (默认输出 `LYYC_parsev 结构` 格式)

+ 整合 原 `parse_video` 和 `evparse` 的 网站 支持. (`evparse` 已被 废弃)

+ 原生内置 `bridge` 功能支持. 

+ 继承 `parse_video version 0.4.x` 的 `method` 参数传递功能, 
  以及命令行接口. (命令行参数格式)
  
  (`--min`, `--max`, `--i-min`, `--i-max`, `--extractor`, `--method`, `--debug`)


## 计划支持的网站 (4)
(`extractor`)

+ pptv (*高码* `1080p`)

+ vqq (ckey5.4, `1080p`)
+ kankan (`1080p`, `h265`)

+ youku (TODO)

*实现顺序*

1. pptv
2. kankan
3. vqq


## `bridge` 支持

+ `vqq`: 有关 `ckey5.4` 的 bridge
+ `271`: 有关 `salt` 的 *bridge* (*无颜* 系列)


## 专用 下载器

某些网站的视频文件下载方式, 不是普通的 http 下载方式. 
使用 *通用下载工具* 难以取得良好的效果. 
此时配合使用 *专用下载器* 可达到更好的效果. 

+ `tvsohu`: 专用文件下载器 (`pv_tvsohu_http`)
+ `kankan_flv`: 专用 flv 视频文件下载器


TODO
<!-- end parsev.md -->


