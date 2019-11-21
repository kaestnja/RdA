wmic os get caption
wmic os get osarchitecture

#enable the verry long names for files and paths, just for sure
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control" -Name "FileSystem@LongPathsEnabled" -Value 1
#prevent download fails, if internet explorer was not first initilized with recommended microsoft settings
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Internet Explorer\Main" -Name "DisableFirstRunCustomize" -Value 2

md -p "C:\Temp"
cd c:\Temp

#Install PScore6 
#iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"
$path = "C:\Temp\PowerShell-6.2.3-win-x64.msi"
if (!($path | Test-Path)) { curl https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi -OutFile $path }
#msiexec.exe /l*v mdbinstall.log /qb /i PowerShell-6.2.3-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1
if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i PowerShell-6.2.3-win-x64.msi","/quiet","ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1","ENABLE_PSREMOTING=1","REGISTER_MANIFEST=1" }

#Install Git 
$path = "C:\Temp\Git-2.24.0.2-64-bit.exe"
if (!($path | Test-Path)) { curl https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe -OutFile $path }
#.\Git-2.24.0.2-64-bit.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /COMPONENTS="icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate" /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled
#with ArgumentList as list
if (Test-Path $path) { Start-Process -Wait -FilePath "Git-2.24.0.2-64-bit.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/SILENT /NORESTART /NOCANCEL /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled /COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }
#with ArgumentList as string array
#if (Test-Path $path) { Start-Process -Wait -FilePath "Git-2.24.0.2-64-bit.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/SILENT","/NORESTART","/NOCANCEL","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/NoIcons=0","/SetupType=default","/EditorOption=Nano","/PathOption=Cmd","/SSHOption=OpenSSH","/TortoiseOption=false","/CURLOption=OpenSSL","/CRLFOption=CRLFCommitAsIs","/BashTerminalOption=MinTTY","/PerformanceTweaksFSCache=Enabled","/UseCredentialManager=Enabled","/EnableSymlinks=Disabled","/EnableBuiltinInteractiveAdd=Disabled","/COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }
#add wget into Git 
$path = "C:\Program Files\Git\mingw64\bin\wget.exe"
if (!($path | Test-Path)) { curl https://eternallybored.org/misc/wget/1.20.3/64/wget.exe -OutFile $path }

$path = "C:\Temp\python-3.7.5-amd64.exe"
if (!($path | Test-Path)) { curl https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe -OutFile $path }
#.\python-3.7.5-amd64.exe /passive InstallAllUsers=1 TargetDir=C:\Python37 PrependPath=1
if (Test-Path $path) { Start-Process -Wait -FilePath "python-3.7.5-amd64.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python37","PrependPath=1" }

$path = "C:\Temp\mongodb-compass-community-1.19.12-win32-x64.msi"
if (!($path | Test-Path)) { curl https://downloads.mongodb.com/compass/mongodb-compass-community-1.19.12-win32-x64.msi -OutFile $path }
if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi" }
md -p "C:\MongoDB\data"
md -p "C:\MongoDB\log"
$path = "C:\Temp\mongodb-win32-x86_64-2012plus-4.2.1-signed.msi"
if (!($path | Test-Path)) { curl https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi -OutFile $path }
#if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`"" }
if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","SHOULD_INSTALL_COMPASS=`"0`"","ADDLOCAL=`"all`"" }
