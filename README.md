<!-- README.md, parse_video/, <https://github.com/sceext2/parse_video>
   - author sceext <sceext@foxmail.com>
   - test201601312253
  -->

# parse_video version 0.5.9.0

`parse_video` is used to get video information (video file download URL) 
from some web sites. 


## Description

**Supported** (6)

+ *271* (`4K`)
+ *letv* (1080p)
+ *hunantv* (*720p*)
+ *tvsohu* (`4K` h265)
+ *pptv* (`1080p` *high bitrate*)
+ *vqq* (1080p)


## Install

`parse_video` runs under `python 3.5`. 
<https://www.python.org/>


## Usage

```
$ ./pv --help
Usage: parsev [OPTION]... URL
parse_video: get video info from some web sites. 

  -i, --min HD       set min hd number for video formats
  -M, --max HD       set max hd
      --i-min INDEX  set min index number for part video files
      --i-max INDEX  set max index
  
  -e, --extractor EXTRACTOR  set extractor (and extractor arguments)
  -m, --method METHOD        set method (and method arguments)
  
  -o, --output FILE  write result (video info) to file (default to stdout)
      --more FILE    input more info from file to enable more mode
      
      --network-timeout-s  set timeout (second) to network operations
      
  -d, --debug  set log level to debug
  -q, --quiet  set log level to quiet
      
      --help     display this help and exit
      --version  output version information and exit
      --license  show license information and exit

More information online: <https://github.com/sceext2/parse_video> 
$ 
```


## Tests

Please run `make test` 


## LICENSE

```
$ ./pv --license
    parse_video : get video info from some web sites. 
    Copyright (C) 2015-2016 sceext <sceext@foxmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
$ 
```


<!-- end README.md -->


