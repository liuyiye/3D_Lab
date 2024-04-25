REM 获取当前日期并将其格式化为 YYYY-MM-DD-TIME
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /format:list') do set datetime=%%a
set datestamp=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%-%datetime:~8,6%

rename C:\GE_Not_Good\GE_Not_Good.log %datestamp%.log
"%ProgramFiles%\WinRAR\RAR.exe" a -ep1 -o- C:\GE_Not_Good\log.zip C:\GE_Not_Good\%datestamp%.log
del C:\GE_Not_Good\%datestamp%.log

robocopy  C:\GE_Not_Good\storage  C:\GE_Not_Good\not_finished /E /MOVE /IS
mkdir C:\GE_Not_Good\storage

python C:\GE_Not_Good\GE_Not_Good.py

