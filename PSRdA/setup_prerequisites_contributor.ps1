wmic os get caption
wmic os get osarchitecture

#enable the verry long names for files and paths, just for sure
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control" -Name "FileSystem@LongPathsEnabled" -Value 1
#prevent download fails, if internet explorer was not first initilized with recommended microsoft settings
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Internet Explorer\Main" -Name "DisableFirstRunCustomize" -Value 2

#on the Siemens network, do not forget to check and set the proxy
# SET HTTP_PROXY=194.145.60.1:9400
# SET HTTPS_PROXY=194.145.60.1:9400
# SET HTTPS_PROXY=https://user:pass@194.145.60.1:9400

md -p "C:\Temp"
cd c:\Temp

#Install PScore6 
#iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"
curl https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi -OutFile C:\Temp\PowerShell-6.2.3-win-x64.msi
#msiexec.exe /l*v mdbinstall.log /qb /i PowerShell-6.2.3-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1
Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i PowerShell-6.2.3-win-x64.msi","/quiet","ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1","ENABLE_PSREMOTING=1","REGISTER_MANIFEST=1"

#Install Git 
curl https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe -OutFile C:\Temp\Git-2.24.0.2-64-bit.exe
#.\Git-2.24.0.2-64-bit.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /COMPONENTS="icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate" /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled
#with ArgumentList as list
Start-Process -Wait -FilePath "Git-2.24.0.2-64-bit.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/SILENT /NORESTART /NOCANCEL /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled /COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate`""
#with ArgumentList as string array
#Start-Process -Wait -FilePath "Git-2.24.0.2-64-bit.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/SILENT","/NORESTART","/NOCANCEL","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/NoIcons=0","/SetupType=default","/EditorOption=Nano","/PathOption=Cmd","/SSHOption=OpenSSH","/TortoiseOption=false","/CURLOption=OpenSSL","/CRLFOption=CRLFCommitAsIs","/BashTerminalOption=MinTTY","/PerformanceTweaksFSCache=Enabled","/UseCredentialManager=Enabled","/EnableSymlinks=Disabled","/EnableBuiltinInteractiveAdd=Disabled","/COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate`""
#add wget into Git 
curl https://eternallybored.org/misc/wget/1.20.3/64/wget.exe -OutFile "C:\Program Files\Git\mingw64\bin\wget.exe"

curl https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe -OutFile C:\Temp\python-3.8.0-amd64.exe
#.\python-3.8.0-amd64.exe /passive InstallAllUsers=1 TargetDir=C:\Python38 PrependPath=1
Start-Process -Wait -FilePath "python-3.8.0-amd64.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python38"

curl https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe -OutFile C:\Temp\python-3.7.5-amd64.exe
#.\python-3.7.5-amd64.exe /passive InstallAllUsers=1 TargetDir=C:\Python37 PrependPath=1
Start-Process -Wait -FilePath "python-3.7.5-amd64.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python37","PrependPath=1"

curl https://downloads.mongodb.com/compass/mongodb-compass-community-1.19.12-win32-x64.msi -OutFile C:\Temp\mongodb-compass-community-1.19.12-win32-x64.msi
Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi"
md -p "C:\MongoDB\data"
md -p "C:\MongoDB\log"
curl https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi -OutFile C:\Temp\mongodb-win32-x86_64-2012plus-4.2.1-signed.msi
#developer
Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerNoService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`""
#C:\MongoDB\Server\4.2\bin\mongod.exe --dbpath "C:\MongoDB\data"  "C:\MongoDB\log" --bind_ip 127.0.0.1 --port 27017
#C:\MongoDB\Server\4.2\bin\mongod.exe --bind_ip 127.0.0.1 --port 27017
#shortcut
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\MongoDB.lnk")
$Shortcut.TargetPath = "${env:ProgramFiles}\MongoDB\Server\4.2\bin\mongod.exe"
$Shortcut.Arguments = "--dbpath `"C:\MongoDB\data`" `"C:\MongoDB\log`" --bind_ip 127.0.0.1 --port 27017"
$Shortcut.Description = "start local MongoDB"
#$Shortcut.IconLocation = "${env:ProgramFiles}\MongoDB\Server\4.2\bin\mongod.exe, 1"
$Shortcut.WindowStyle = "1"
$Shortcut.WorkingDirectory = "${env:ProgramFiles}\MongoDB\Server\4.2\bin"
$Shortcut.Save()

#curl https://notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe -OutFile C:\Temp\npp.7.7.1.Installer.x64.exe
curl http://download.notepad-plus-plus.org/repository/7.x/7.8.1/npp.7.8.1.Installer.x64.exe -OutFile C:\Temp\npp.7.8.1.Installer.x64.exe
Start-Process -Wait -FilePath "npp.7.8.1.Installer.x64.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/S"