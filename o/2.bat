@echo off
echo parse_video �򵥲��� 2.bat 0.py

:start
set /p url=������ URL: 

%1 parsev --output-easy --write-output-file %url%

pause

goto start


