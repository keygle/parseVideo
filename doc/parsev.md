<!-- parsev.md, parse_video/doc/, <https://github.com/sceext2/parse_video>
   - language: Chinese (zh_cn) 
  -->

# 负锐 视频解析 (parse_video) : 小型 纯解析 程序
parse_video version 0.5.9.0


## 已支持网站 (6)

|   # | site | quality | extractor |     |
| --: | :--- | :-----: | :-------- | :-- |
|  1 | 271     | `4K`          | `bks1`    | |
|  2 | letv    | 1080p         | `letv`    | |
|  3 | hunantv | *720p*        | `hunantv` | |
|  4 | tvsohu  | `4K` *h265*   | `tvsohu`  | |
|  5 | pptv    | `1080p` *高码* | `pptv`    | |
|  6 | vqq     | 1080p         | `vqq`     | *ckey5.4* |


## parse_video 特色

+ **本地解析** <br />
  parse_video 的 解析过程, 完全在本地完成, 不依赖中心服务器. 
  
  所以, 只要视频网站的服务器能够访问, 就能够解析. 

+ **多种解析方法** <br />
  对于每个网站, parse_video 可以提供多种 *解析方法* (`method`). 
  
  可根据需要选择使用, 或者在配置文件中指定 *默认解析方法*. 

+ **更多详细信息** <br />
  在不牺牲解析速度的情况下, parse_video 会努力解析出更多信息, 
  比如 *视频分辨率*, *小标题*, *分段文件的 md5 校验值*, 等. 

+ **加速解析** <br />
  parse_video 可以通过多种方式来减少网络请求数量, 从而加快解析速度. 

+ **更接近标准的解析** (TODO) <br />
  *parse_video* 的 `pc_flash_gate` 方法, 使用 PC 网页版 flash 的方法, 
  大多数情况下, 只要视频能够正常播放, 就能够正常解析. 

+ **纯解析** <br />
  parse_video 是 *纯粹的* 解析程序, 不和 下载程序 集成在一起. 
  
  这样更方便使用其它下载程序进行下载. 
  
  不过, parse_video 附带了一个小工具: `pvdl` 是一个简单的下载程序. 

+ **json 文本输出** <br />
  parse_video 使用命令行文本界面, 输出格式统一的 JSON 文本. 
  
  这使得 parse_video 很容易被其它程序调用和使用. 

+ **跨平台** <br />
  parse_video 使用 `python 3` 编写, 具有良好的跨平台特性. 
  
  目前 parse_video 能够在下列平台上正常工作: 
  
  + GNU/Linux (如 `ArchLinux`)
  + Windows (如 *Windows 10*)
  + Android (如 *Android 5.1*)


## 支持网站 限制

+ 主要支持 *中国* 的大型视频网站. 
  
  其它国家的 一般 不考虑. 

+ 支持 *少数* 网站, 但力求达到 *优质* 支持. 

+ **高清** 支持: 
  
  + *至少* `720p` 画质 (*分辨率* 约为 `1280 x 720`)
  
  + *大多数* 支持 `1080p` 画质 (约 `1920 x 1080`)
  
  + *少数* 支持 `4K` (约 `3840 x 2160`) 和 `h265` 
  
  + 清晰度 (画质) *太低* 的 *不考虑* 支持


## 计划支持的网站 (2)
(`extractor`)

+ youku (TODO)

+ kankan (`1080p`, `h265`)

*实现顺序*

1. youku


## version 0.5.x 特性

+ 原生提供 `lyyc` 插件接口. (默认输出 `LYYC_parsev 结构` 格式)

+ 原生内置 `bridge` 功能支持. 


## TODO `bridge` 支持

+ `vqq`: 有关 `ckey5.4` 的 bridge
+ `271`: 有关 `salt` 的 *bridge* (*无颜* 系列)

## TODO 专用 下载器

某些网站的视频文件下载方式, 不是普通的 http 下载方式. 
使用 *通用下载工具* 难以取得良好的效果. 
此时配合使用 *专用下载器* 可达到更好的效果. 

+ `tvsohu`: 专用文件下载器 (`pv_tvsohu_http`)
+ `kankan_flv`: 专用 flv 视频文件下载器


<!-- end parsev.md -->


