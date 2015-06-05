@echo off
set ffmpegbin=ffmpeg
echo "merge1.bat for parse_video"
set /p list=Input list file name: 
set /p output=Input output file name: 
echo "INFO: starting merge ... "

%ffmpegbin% -f concat -i %list% -c copy %output%

pause


