<!-- user.md, parse_video/doc/
   - language: Chinese (zh_cn) 
  -->

# 负锐 视频解析 (parse_video) 用户指导


## 内容目录
TODO


## parse_video 整体结构

`parse_video` 由 *解析库* (lib), *命令行界面* (CLI), *插件接口* (plugin), *附属小工具*, 
等 4部分 组成. 

其中 *解析库* 含有若干 *解析器* (`extractor`). 每个 extractor 支持 1个 *网站*. 

每个 extractor 可能含有 1个 或 *多个* *解析方法* (`method`). 
每个 extractor 有其 *默认* method (可配置), 也可以在解析时指定所使用的 method. 
(命令行界面 `--method`)

解析时如果没有指定 extractor (命令行界面 `--extractor`) 则 *解析库* 会匹配输入的 URL, 
自动选择 extractor. (可配置)

指定 extractor 和 method 时, 也可同时指定 *extractor 参数* 和 *method 参数*. 


TODO
<!-- end user.md -->


