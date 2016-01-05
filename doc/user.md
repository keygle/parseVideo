<!-- user.md, parse_video/doc/
   - language: Chinese (zh_cn) 
   - test201601051943
  -->

# 负锐 视频解析 (parse_video) 用户指导
parse_video version 0.5.3.0

## 内容目录

+ **[1. parse_video 整体结构](#1-parse_video-整体结构)**

+ **[2. `method` 及其参数](#2-method-及其参数)**
  + **[2.1 `method` 字符串格式](#21-method-字符串格式)**

+ **[3. 加速解析](#3-加速解析)**
  + **[3.1 `hd` 和 `index` 的选择](#31-hd-和-index-的选择)**
  + **[3.2 `--more` 功能](#32---more-功能)**

+ **[4. 主要配置文件](#4-主要配置文件)**
  + **[4.1 `lib/conf.py`](#41-lib-conf-py)**

+ **[5. 调试模式](#5-调试模式)**


## 1. parse_video 整体结构

`parse_video` 由 *解析库* (lib), *命令行界面* (CLI), *插件接口* (plugin), *附属小工具*, 
等 4部分 组成. 

其中 *解析库* 含有若干 *解析器* (`extractor`). 每个 extractor 支持 1个 *网站*. 

每个 extractor 可能含有 1个 或 *多个* *解析方法* (`method`). 
每个 extractor 有其 *默认* method (可配置), 也可以在解析时指定所使用的 method. 
(命令行界面 `--method`)

解析时如果没有指定 extractor (命令行界面 `--extractor`) 则 *解析库* 会匹配输入的 URL, 
自动选择 extractor. (可配置)

指定 extractor 和 method 时, 也可同时指定 *extractor 参数* 和 *method 参数*. 


## 2. `method` 及其参数

每个 *extractor* 可以支持多个 *method*, 也就是说, 能够使用 *多种方法* 解析一个网站. 

不同的 method 可能各有优缺点. 请根据需要选择使用. 

method (extractor) 可能支持若干 *参数*, 用来控制或调节一些 *解析细节*. 

*参数* 由 method 解析和支持, 其含义由 method 自行定义. 不同 method 的参数很可能不同. 

### 2.1 `method` 字符串格式

*method 字符串* 格式如下:

```
method 名称;参数1,参数2, ...
```

*method 名称* 和 *参数* 之间用 `;` (分号) 分开. 如果没有参数, 则 `;` 可省略. 

*多个参数* 之间用 `,` (逗号) 分开. 如果只有一个参数, 则 `,` 可省略. 

比如 

> `android` <br />
> `pc_flash_gate;gen_header` <br />
> `pc_flash_gate;enable_more,fast_parse` <br />
> `pc_flash_gate;set_um,fix_4k,enable_vv_error` 

等, 都是格式正确的 *method 字符串*. 

使用 CLI 的 `--method` 参数指定解析时使用的 *method 字符串*. 如果没有指定, 
将使用 `lib/conf.py` 中配置的默认值. 

*注意*: 有的 extractor 可能自定义 `;` 后面的参数分隔格式. 此处所使用 `,` 分隔, 只是通常情况. 


## 3. 加速解析

要 *加快解析速度*, 就是要 *减少* 解析过程中的 *网络请求* 数量. 

对于某个 extractor 的某个 method 来说, 如果获取全部信息 (特别是 *全部文件的下载地址*) 
可能需要许多网络请求. 这时解析就会比较慢. 

此时, 可以根据需要, 有选择的减少 extractor 获取的信息. 这样 extractor 就可以根据具体情况, 
减少网络请求的数量, 从而 *显著* 加快解析. 

除了下述的 *hd 和 index 的选择* 和 *--more 功能* 之外, 有的 extractor 的某些 method 
还有专门的参数, 用来进一步的减少网络请求从而加快解析. <br />
比如 extractor `letv` method `pc_flash_gate` 的 `fast_parse` 参数. 

### 3.1 `hd` 和 `index` 的选择

+ `quality`: 表示视频 *画质* (或者说 *清晰度*). 一般情况下, 如果编码方式相同, 
  (比如都是 `h264` 编码) 则 *分辨率* 越高, *码率* 越高, quality 越好. 

对于同一个视频 (输入的 URL) 可能 (使用相同的 extractor 以及相同的 method) 
会得到多个不同 `quality` 的结果. 

+ `hd`: parse_video 使用 *hd 值* 表示 quality. hd 是一个 *数字*, 可以是 *整数*, 
  也可以是 *小数*. 可以 *大于*, *等于*, *小于* 0. 
  
  hd 越大, 则 quality 越好. 在同一个 parse_video 的输出结果中, hd 值 *不允许重复*. 


**hd 的选择**

使用 CLI 的 `--min`, `--max` 参数指定 *最小*, *最大* 的 hd 值. 可以指定为 *任意数字*. 

并且, *最大*值 可以 *大于*, *等于*, 甚至 **小于** *最小值*. 如果不指定, 则表示 *不限制*. 

比如 

> `--min -1` <br />
> `--max 5.1` <br />
> `--min 4 --max 4` <br />
> `--min 1 --max 0` 

等, 都是允许的. 

*注意*: hd 选择功能需要 extractor 的支持. 有的 extractor 也可能直接忽略此参数. 


**index 的选择**

`index` 是 *分段视频文件* 的序号, 从 `0` 开始 (即 0 表示 *第1个分段* 文件). 

使用 `--i-min`, `--i-max` 参数指定 *最小*, *最大* 的所需获取信息的分段文件的序号. 
`--i-min`, `--i-max` 的使用和 `--min`, `--max` 很像. 

比如 

> `--i-min 5` <br />
> `--i-max 12` <br />
> `--i-min 2 --i-max 2` <br />
> `--i-min 1 --i-max 0`

等, 都是允许的. 

*注意*: index 选择功能需要 extractor 的支持. 也有可能被忽略. 


### 3.2 `--more` 功能

在 *多次解析同一个* URL 时, 有些信息可以重复利用, 不必每次都从网络下载. <br />
比如, 通常都要下载 URL 指定的网页的 html 文本, 从中获取 `vid` 等信息. 

如果能够保存这些信息, 下次解析时直接提供给 extractor, 就有可能减少网络请求, 
从而进一步加快解析速度. 

`--more` 功能就是用来给 extractor **提供 更多信息** 的. 

比如, 重复解析 URL 指定的视频

> ```
> ./parsev URL --method "pc_flash_gate;enable_more" --output 2.json
> ./parsev URL --more 2.json
> ```

第1条命令, 使用 `enable_more` 参数让 extractor 将更多信息保存到输出信息中, 
并且将输出保存到 *2.json* 文件. 

第2条命令, 解析同一个 URL, 并且使用 `--more` 将 *2.json* 中的信息提供给 extractor. 

*注意*: `--more` 功能需要 extractor 的支持. 


## 4. 主要配置文件

### 4.1 `lib/conf.py`

+ **extractor 的** *默认* **method**
  
  ```
  DEFAULT_METHOD = {
      'bks1' : 'pc_flash_gate;fix_4k', 
      'letv' : 'flvsp', 
      'hunantv' : 'flvsp', 
      'tvsohu' : 'flvsp', 
      'pptv' : 'pc_flash_gate', 
  }
  ```
  
  左侧为 `EXTRACTOR_ID`, 右侧为 *默认* method 字符串. 

+ **根据输入的 URL 匹配选择 extractor**
  
  ```
  URL_TO_EXTRACTOR = {
      '^http://[a-z]+\.iqiyi\.com/.+\.html' : 'bks1', 
      '^http://www\.letv\.com/.+\.html' : 'letv', 
      '^http://www\.hunantv\.com/.+\.html' : 'hunantv', 
      '^http://tv\.sohu\.com/.+\.shtml' : 'tvsohu', 
      '^http://v\.pptv\.com/.+\.html' : 'pptv', 
  }
  ```
  
  左侧为 *正则表达式* (RE), 用来匹配输入的 URL. 右侧为 `EXTRACTOR_ID`. 


## 5. 调试模式

使用 `--debug` 参数开启 *调试模式*, 将会输出更多的 *解析细节*. 
这将有助于 *调试* 和 *除错*. 

默认模式将仅输出少量信息, 即解析的大致过程. 

使用 `--quiet` 参数开启 *安静模式*. (将输出更少的信息) 
仅输出 *错误* 和 *警告* 信息. 


<!-- end user.md -->


