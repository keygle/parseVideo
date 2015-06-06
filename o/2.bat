@echo off
echo parse_video ºÚµ•≤‚ ‘ 2.bat 0.py

:start
set /p url=«Î ‰»Î URL: 

%1 parsev --output-easy --write-output-file %url%

pause

goto start


