for /d %%d in ("%~dp0*.") do set name=%%d
"C:\Program Files\WinRAR\rar.exe" a -r -m3 -sfx -ep1 -inul %name% %name%\*
"C:\Program Files\WinRAR\rar.exe" c -zc.txt -inul %name%.exe

@echo off
rem c.txt in the same dir:
rem Setup=uPP_Viewer.exe
rem TempMode
rem Silent=1
rem Overwrite=1
@echo on

pause