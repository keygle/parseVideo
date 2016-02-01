<!-- README.md, parse_video/pvdl/
   -
  -->

A small tool of `parse_video`: 
# pvdl : parse_video Downloader
A *reference implemention* of a downloader which uses `parse_video`. 

`pvdl version 0.0.12.1`


## Install

`pvdl` runs under `python 3.5`. <https://www.python.org/>

**Dependencies**

+ `wget` (version 1.16 or later recommended) <https://www.gnu.org/software/wget/>
+ `ffmpeg` (version 2.8 or later recommended) <https://www.ffmpeg.org/>
+ *[optional]* `mediainfo` (version 0.7 or later recommended) <https://mediaarea.net/en/MediaInfo>

If you use `ArchLinux`, you can install them by: 

```
 # pacman -S --needed wget ffmpeg mediainfo
```

*python modules*

+ `colored` (version 1.2 or later) <https://pypi.python.org/pypi/colored/>

please use `# pip install colored --upgrade` to install it. 


## Usage

```
$ ./pvdl --help
Usage: pvdl [OPTION]... URL
pvdl: A reference implemention of a downloader which uses parse_video. 

      --hd HD                  set hd to select
  -o, --output DIR             save downloaded file to DIR
      --title-suffix SUFFIX    add suffix to resolve name conflicts
      --title-no NO            set title_no
      --retry TIMES            set retry times
      --retry-wait SECONDS     wait seconds before retry
      --parse-timeout SECONDS  set parse timeout
      
      --enable FEATURE   enable pvdl features
      --disable FEATURE  disable pvdl features
      
      --list FILE         download each item in list file
      --list-retry TIMES  set list retry times
      
      --  directly pass options to parse_video
  
  -d, --debug  set log level to debug
      
      --help     display this help and exit
      --version  output version information and exit
      --license  show license information and exit

More information online: <https://github.com/sceext2/parse_video> 
$ 
```


<!-- end README.md -->


