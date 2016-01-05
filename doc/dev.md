<!-- dev.md, parse_video/doc/
   - language: Chinese (zh_cn) 
  -->

# parse_video 开发者指导
parse_video version 0.5.3.0


## 内容目录

+ **[1. parse_video 主要文件](#1-parse_video-主要文件)**
+ **[2. extractor 接口](#2-extractor-接口)**
+ **[3. 基础工具集介绍](#3-基础工具集介绍)**


## 1. parse_video 主要文件

```
parse_video/    # parse_video 根目录
    lib/        # 解析库
        entry.py        # 解析库入口文件
        conf.py         # 解析库配置文件
        
        var.py          # 解析库全局数据
        err.py          # 错误定义
        restruct.py     # 格式化输出 json 信息
        
        b.py            # 基础工具集
        _b/             # 基础工具集
        
        e/              # extractor
            common.py   # extractor 共用代码
            log_text.py # extractor 共用提示文本
            
            hunantv/    # extractor hunantv, 以此 extractor 举例说明
                entry.py        # extractor 入口文件
                var.py          # extractor 全局数据
        bridge/         # bridge 功能
        lan.py          # 语言文本
    bin/                # 命令行界面 (CLI)
        parse_video.py  # CLI 主要可执行文件
    
    doc/        # parse_video 文档
    etc/        # 一些配置文件
    o/          # 附属小工具
    LICENSE     # GNU GPL v3 许可证
    README.md   # 说明文件
    makefile    # 主要用于测试
    
    parsev      # CLI 入口
    run.py      # 猎影插件入口文件 (lieying plugin)
```

+ `lib/e`: **extractor 位置**
  
  parse_video 的 extractor 都位于此目录中. 每个 extractor 是一个子目录, 
  以其 `EXTRACTOR_ID` 命名. 
  
  *注意*: `EXTRACTOR_ID` 应是合适的 *python 标识符*, 以便 extractor 能够被顺利 `import`. 


## 2. extractor 接口
TODO


## 3. 基础工具集介绍
TODO


TODO
<!-- end dev.md -->


