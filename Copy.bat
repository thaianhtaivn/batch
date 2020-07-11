@echo off

set SRC="%CD%"\file_2
set DES="%CD%"\file_1
set FILENAME=MyTest1.txt
set Wait1="%CD%"\file_1\Wait1.bat
set Wait2="%CD%"\file_1\Wait2.bat
set Wait3="%CD%"\file_1\Wait3.bat

echo Start_time: %time%
REM echo Copy %FILENAME% from %SRC% to %DES%
xcopy /s/y %SRC% %DES%

timeout 5

 call %Wait1%
 call %Wait2%
 call %Wait3%

echo End_time: %time%
