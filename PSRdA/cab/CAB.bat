@echo off &echo. &set "ext=%~x1" &title CAB [%1] &rem input file or folder / 'files' folder / unpacks .cab .??_
if "_%1"=="_" if not exist "%~dp0files" echo CAB: No input and no 'files' directory to pack &goto :Exit "do nothing"
if "_%1"=="_" if exist "%~dp0files" call :CabDir "%~dp0files" &goto :Exit "input = none, use 'files' directory -pack" 
for /f "tokens=1 delims=r-" %%I in ("%~a1") do if "_%%I"=="_d" call :CabDir "%~f1" &goto :Exit "input = dir -pack"
if not "_%~x1"=="_.cab" if not "_%ext:~-1%"=="__" call :CabFile "%~f1" &goto :Exit "input = file -pack"
call :CabExtract "%~f1" &goto :Exit "input = .cab or .??_ -unpack" 
:Exit AveYo: script will add a CAB entry to right-click -- SendTo menu
if exist "%APPDATA%\Microsoft\Windows\SendTo\CAB.bat" xcopy "%~f0" "%APPDATA%\Microsoft\Windows\SendTo\CAB.*" /D /E /F /H /R /Y /C /Z>nul 2>nul
if not exist "%APPDATA%\Microsoft\Windows\SendTo\CAB.bat" copy /y "%~f0" "%APPDATA%\Microsoft\Windows\SendTo\CAB.bat" >nul 2>nul
ping -n 6 localhost >nul &title cmd.exe &exit /b
:CabExtract %1:[.cab or .xx_]
echo %1 &pushd "%~dp1" &mkdir "%~n1" >nul 2>nul &expand -R "%~1" -F:* "%~n1" &popd &goto :eof
:CabFile %1:[filename]
echo %1 &pushd "%~dp1" &makecab /D CompressionType=LZX /D CompressionLevel=7 /D CompressionMemory=21 "%~nx1" "%~n1.cab" &goto :eof   
:CabDir %1:[directory]
dir /a:-D/b/s "%~1"
set "ddf="%temp%\ddf""
echo/.New Cabinet>%ddf%
echo/.set Cabinet=ON>>%ddf%
echo/.set CabinetFileCountThreshold=0>>%ddf%
echo/.set Compress=ON>>%ddf%
echo/.set CompressionType=LZX;MSZIP>>%ddf%
echo/;.set CompressionLevel=7>>%ddf%
echo/;.set CompressionMemory=21>>%ddf%
echo/.set FolderFileCountThreshold=0;>>%ddf%
echo/.set FolderSizeThreshold=0;>>%ddf%
echo/.set GenerateInf=OFF>>%ddf%
echo/.set InfFileName=nul>>%ddf%
echo/.set MaxCabinetSize=0;>>%ddf%
echo/.set MaxDiskFileCount=0;>>%ddf%
echo/.set MaxDiskSize=0;>>%ddf%
echo/.set MaxErrors=1;>>%ddf%
echo/.set RptFileName=nul>>%ddf%
echo/.set UniqueFiles=ON>>%ddf%
setlocal enabledelayedexpansion
pushd "%~dp1"
for /f "tokens=* delims=" %%D in ('dir /a:-D/b/s "%~1"') do (
 set "DestinationDir=%%~dpD" &set "DestinationDir=!DestinationDir:%~1=!" &set "DestinationDir=!DestinationDir:~0,-1!"
 echo/.Set DestinationDir=!DestinationDir!;>>%ddf%
 echo/"%%~fD"  /inf=no;>>%ddf%
)
makecab /F %ddf% /D DiskDirectory1="" /D CabinetNameTemplate=%~nx1.cab &endlocal &popd &del /q /f %ddf% &goto :eof