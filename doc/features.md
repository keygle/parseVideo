<!-- features.md, parse_video/doc/
   - language: Chinese (zh_cn) 
  -->

# parse_video 功能特性
parse_video version 0.5.4.0

| extractor | `method` | quality | format | `--more` |     |
| :-------- | :------- | :-----: | :----- | :------- | :-- |
| bks1      | pc_flash_gate | `4K`          | flv         | *first_json* | `checksum.md5`, (w) |
| letv      | pc_flash_gate | 1080p         | *ts* (m3u8) | vid_info     | |
|           | `flvsp`       |               | mp4 *(单段)* |              | |
|           | *m3u8*        |               | *ts* (m3u8) | 不支持        | 支持 m3u8 URL 或 本地 m3u8 文件 |
| hunantv   | pc_flash_gate | *720p*        | *m3u8*      | vid_info     | |
|           | `flvsp`       |               | mp4 *(单段)* |              | |
| tvsohu    | pc_flash_gate | `4K` (h265)   | mp4         | *first_json* | 下载方式 `pv_tvsohu_http` |
|           | `flvsp`       |               |             |              | |
| pptv      | pc_flash_gate | `1080p` *高码* | mp4         | vid_info     | `expire` |
|           | `android`     | 1080p         | mp4 *(单段)* |              | `expire` |
| vqq       | pc_flash_gate | 1080p         | mp4         | 不支持        | `checksum.md5` |

*注*

+ *extractor*, *quality*, *format*, `--more` 为空表示 *同上*
+ *format* 默认为 *分段*

## method 参数

+ **bks1**.*pc_flash_gate*
  
  + `set_um`
  + `set_vv`
  + `fix_4k`

+ **letv**.*pc_flash_gate*
  
  + `fast_parse`

+ **tvsohu**.*pc_flash_gate*
  
  + `gen_header`

+ **vqq**.*pc_flash_gate*
  
  + `fix_1080p`
  + `ignore_fix_1080p_error`
  + `enable_fmt_black_list`
  + `add_raw_quality`


<!-- end features.md -->


