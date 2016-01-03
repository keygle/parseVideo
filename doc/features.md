<!-- features.md, parse_video/doc/
   - language: Chinese (zh_cn) 
  -->

# parse_video 功能特性

| extractor | `method` | quality | format | `--more` | *args* |     |
| :-------- | :------- | :-----: | :----- | :------- |:------ | :-- |
| bks1      | pc_flash_gate | `4K`          | flv         | *first_json* | `set_um`, `set_vv`, `fix_4k`, <br /> `set_flag_v`, `enable_vv_error` | (w) | 
| letv      | pc_flash_gate | 1080p         | *ts* (m3u8) | vid_info     | `fast_parse` | |
|           | `flvsp`       |               | mp4 *(单段)* |              | | |
| hunantv   | pc_flash_gate | *720p*        | *m3u8*      | vid_info     | | |
|           | `flvsp`       |               | mp4 *(单段)* |              | | |
| tvsohu    | pc_flash_gate | `4K` (h265)   | mp4         | *first_json* | `gen_header` | 下载方式 `pv_tvsohu_http` |
|           | `flvsp`       |               |             |              | | |
| pptv      | pc_flash_gate | `1080p` *高码* | mp4         | vid_info     | | |
|           | `android`     | 1080p         | mp4 *(单段)* |              | | |

*注*

+ *extractor*, *quality*, *format*, `--more` 为空表示 *同上*
+ *format* 默认为 *分段*


<!-- end features.md -->


