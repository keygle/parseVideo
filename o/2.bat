@echo off
echo parse_video easy test 2.bat 0.py
set /p url=please input URL: 

%1 parsev --output-easy --make-ffmpeg-list %url%

pause


