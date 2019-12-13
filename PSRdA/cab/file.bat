@echo off

:: file.bat CabFilesPath

REM For all files in each .cab file in 'CabFilesPath', extract them to the current directory, 
REM then re-compress each of the now uncompressed files to a new Cabinet file. Naming conflicts 
REM will be overwritten. Directories uncompressed will be ignored. 

REM If 'CabFilesPath' parameter is not specified, the current directory will be used instead. 
if "%~1"=="" ( set CabFilesPath=.) else ( set CabFilesPath=%1)

set temp_dir="%TEMP%\tmp_%~n0\"

set temp_dir=%TEMP_DIR:"=%
if "%TEMP_DIR:~-1%"=="\" set temp_dir=%TEMP_DIR:~0,-1%
set temp_dir="%TEMP_DIR%"

if exist "%TEMP_DIR:"=%"\* rd "%TEMP_DIR:"=%" /s /q
md "%TEMP_DIR:"=%"

pushd %CABFILESPATH%
for /f "delims=" %%I in (' dir /b *.cab ') do (
	cabarc x "%%~I" "%TEMP_DIR:"=%"\
	pushd "%TEMP_DIR:"=%"
	for /f "delims=" %%J in (' dir /a:-d /b "*" ') do (
		cabarc n "%%~nJ.cab" "%%~fJ"
	)
	popd
	xcopy "%TEMP_DIR:"=%\*.cab" "." /y
	del "%TEMP_DIR:"=%" /q
	for /f "delims=" %%K in ('dir /a:d /b "%TEMP_DIR:"=%"') do rd "%%~K"
)
popd

rd "%TEMP_DIR:"=%"