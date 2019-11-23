#plz replace all �   with - " , except in this line. those came from copy snipets from internet.
$temppath = "C:\Temp"
$gitserver = 'github.com'
$gituser = 'kaestnja'

ssh -T "git@$gitserver"

#~/.ssh/config
#Connect-Ssh
#Add-SshConnection -Name gitserver -Uri "$gitserver" -User "$gituser""
#Add-SshConnection -Name Server1 -Uri server1.jeremyskinner.co.uk -User jeremy
#Start-SshAgent -Quiet

#check proxy maybe set proxy
#[Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://username:password@proxy:port/", [EnvironmentVariableTarget]::Machine)
#$myPipProxy='--proxy=http://194.145.60.1:9400'
#$myPipProxy='--proxy=http://server:port'
#$myPipProxy='--proxy=https://user@server:port'
#$myPipProxy='--proxy=https://user:pass@server:port'

#report some important info
wmic os get caption
wmic os get osarchitecture
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\').BuildLabEx
$PSVersionTable.PSVersion

#check and generate the Powershell profile, maybe the session have to be restarted?
if (!($profile | Test-Path)) {echo "no powershell profile found"} else {echo "current powershell profile: $profile"}
if (!($profile | Test-Path)) {New-Item -path $profile -type file -force}

#identify the correct userprofile path, need to prepare desktop links and others
#Get-Childitem env:
#Get-Childitem -path env:* | get-member
$folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop"
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop" }
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:OneDrive").Value + "\Desktop" }
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:Home").Value + "\Desktop" }
if (Test-Path $folder) { echo "found: $folder" }

#eventually prepare executability
Get-ExecutionPolicy
#Set-ExecutionPolicy RemoteSigned
#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Confirm

#enable the verry long names for files and paths, just for sure
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control" -Name "FileSystem@LongPathsEnabled" -Value 1
#prevent download fails, if internet explorer was not first initilized with recommended microsoft settings
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Internet Explorer\Main" -Name "DisableFirstRunCustomize" -Value 2

#check for a needed system reboot, which should be done first
if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired") {read-host "reboot needed! Press ENTER to continue..."}
if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending") {read-host "reboot needed! Press ENTER to continue..."}
if (Test-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations") {read-host "reboot needed! Press ENTER to continue..."}
if (Test-Path "HKLM:\SYSTEM\ControlSet001\Control\Session Manager\PendingFileRenameOperations") {read-host "reboot needed! Press ENTER to continue..."}
if (Test-Path "HKLM:\SYSTEM\ControlSet002\Control\Session Manager\PendingFileRenameOperations") {read-host "reboot needed! Press ENTER to continue..."}
if (Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\InProgress") {read-host "reboot needed! Press ENTER to continue..."}

if ([System.Net.ServicePointManager]::SecurityProtocol -eq [System.Net.SecurityProtocolType]::SystemDefault){echo "PowerShell Transport Layer Security Protocols is maybe to weak (default)";
	#to enable TLS1.2 for now: [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;
	[Net.ServicePointManager]::SecurityProtocol = ([Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12);
	#enter TLS1.2 into Powershell profile for next script too:
	$data = Get-Content -Raw -Path $profile; echo $data;
	if (!($data -like "*Net.ServicePointManager*")) {Add-Content $profile "# Configure PowerShell Transport Layer Security Protocols";
		Add-Content $profile "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12 ;";};
	$data = Get-Content -Path $profile; echo $data;}

####################################################################################################################################
#Install-Module PowerShellGet -Scope CurrentUser -Force -AllowClobber
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
####################################################################################################################################

if (!($temppath | Test-Path)) { md -p "$temppath" }
if (Test-Path "$temppath") {
	cd $temppath
	Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/README.md" -OutFile "$temppath\README_RdA_Github.md";

	#Install PScore6 
	#iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"
	$file = "PowerShell-6.2.3-win-x64.msi"
	if (!("$temppath\$file" | Test-Path)) { curl https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi -OutFile "$temppath\$file" }
	#msiexec.exe /l*v mdbinstall.log /qb /i PowerShell-6.2.3-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i PowerShell-6.2.3-win-x64.msi","/quiet","ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1","ENABLE_PSREMOTING=1","REGISTER_MANIFEST=1" }

	#Install Git 
	$file = "Git-2.24.0.2-64-bit.exe"
	if (!("$temppath\$file" | Test-Path)) { curl https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe -OutFile "$temppath\$file" }
	#.\Git-2.24.0.2-64-bit.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /COMPONENTS="icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate" /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled
	#with ArgumentList as list
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/SILENT /NORESTART /NOCANCEL /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled /COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }
	#with ArgumentList as string array
	#if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/SILENT","/NORESTART","/NOCANCEL","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/NoIcons=0","/SetupType=default","/EditorOption=Nano","/PathOption=Cmd","/SSHOption=OpenSSH","/TortoiseOption=false","/CURLOption=OpenSSL","/CRLFOption=CRLFCommitAsIs","/BashTerminalOption=MinTTY","/PerformanceTweaksFSCache=Enabled","/UseCredentialManager=Enabled","/EnableSymlinks=Disabled","/EnableBuiltinInteractiveAdd=Disabled","/COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }

	#should be in Windows Path now like: ";C:\Program Files (x86)\Git\cmd;C:\Program Files (x86)\Git\bin;"
	$windows_path = $env:Path -split ';'
	$folder = (Get-Item "Env:ProgramFiles").Value + "\Git\bin"
	if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
	$folder = (Get-Item "Env:ProgramFiles").Value + "\Git\cmd"
    if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
	$folder = (Get-Item "Env:ProgramFiles(x86)").Value + "\Git\bin"
	if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
	$folder = (Get-Item "Env:ProgramFiles(x86)").Value + "\Git\cmd"
	if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }

	#add wget into Git 
	$file = "wget.exe"
	$folder = (Get-Item "Env:ProgramFiles").Value + "\Git\mingw64\bin"
	if (Test-Path $folder) { if (!("$folder\$file" | Test-Path)) { curl https://eternallybored.org/misc/wget/1.20.3/64/wget.exe -OutFile "$folder\$file" } }

	#install python
	$file = "python-3.7.5-amd64.exe"
	if (!("$temppath\$file" | Test-Path)) { curl https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python37","PrependPath=1" }

	$windows_path = $env:Path -split ';'
	$folder = "C:\Python37\Scripts\"
    if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
	$folder = "C:\Python37\"
    if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }

    python --version
    $errorcode = python -m pip install --upgrade pip --timeout=3 --retries=1
    #WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x000001DDE3735088>, 'Connection to pypi.org timed out. (connect timeout=3.0)')': /simple/pip/
    python -m pip install --upgrade pip $myPipProxy
	python -m pip install --upgrade setuptools $myPipProxy
	python -m pip install --upgrade wheel $myPipProxy


	#install mongodb
	$file = "mongodb-compass-community-1.19.12-win32-x64.msi"
	if (!("$temppath\$file" | Test-Path)) { curl https://downloads.mongodb.com/compass/mongodb-compass-community-1.19.12-win32-x64.msi -OutFile "$temppath\$file" }
	#server gets a mongodb-compass as application, which is able to edit mongodb completely
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi" }
	
	if (!("C:\MongoDB\data" | Test-Path)) { md -p "C:\MongoDB\data" }
	if (!("C:\MongoDB\log" | Test-Path)) { md -p "C:\MongoDB\log" }
	$file = "mongodb-win32-x86_64-2012plus-4.2.1-signed.msi"
	if (!("$temppath\$file" | Test-Path)) { curl https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi -OutFile "$temppath\$file" }
	#server gets a mongodb as application (not as service), which have to be startet with a shortcut on the desktop
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`"" }
	#if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"all`"" }

	#server gets an allround editor
	$file = "npp.7.7.1.Installer.x64.exe"
	if (!("$temppath\$file" | Test-Path)) { curl https://notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/S" }

	#server gets minimum c++ 14.0 for levenshtein
	$file = "vs_buildtools_2019.exe"
	if (!("$temppath\$file" | Test-Path)) { curl "https://$gitserver/$gituser/RdA/raw/master/PSRdA/vs/$file" -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { 
		Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--update","--passive","--wait" -Wait -PassThru;
		}
}

#(new-object Net.WebClient).DownloadString("http://psget.net/GetPsGet.ps1") | iex install-module posh-git
#maybe as first time install posh-git and posh-shell
#PowerShellGet\Install-Module posh-git -Scope CurrentUser -AllowPrerelease -Force
#PowerShellGet\Install-Module posh-sshell -Scope CurrentUser
#else
Install-Module posh-git -force
#Install-Module posh-sshell -force
#PowerShellGet\Update-Module posh-git
#PowerShellGet\Update-Module posh-sshell

#now
Import-Module posh-git
#Import-Module posh-sshell
#user
Add-PoshGitToProfile
#Add-PoshGitToProfile -force
#Add-PoshSshellToProfile
#all
#Add-PoshGitToProfile -AllUsers -AllHosts
#speed up git status
#$GitPromptSettings.EnableFileStatus = $false
#$GitPromptSettings.RepositoriesInWhichToDisableFileStatus

#disable home Path
#$GitPromptSettings.DefaultPromptAbbreviateHomeDirectory = $false

git update-git-for-windows

#Get-Item "Env:"
#get-childitem -path env:* | get-member
#get git CdA
$project = "CdA"
$folder = (Get-Item "Env:USERPROFILE").Value + "\source\repos\$gitserver"
if (Test-Path (Get-Item "Env:USERPROFILE").Value) { if (!($folder | Test-Path)) { md -p $folder } }
if (Test-Path $folder) { if (!("$folder\$project" | Test-Path)) { 
	cd $folder
	git clone "https://$gitserver/$gituser/CdA.git" 
	#git clone "https://username:password@$gitserver/$gituser/CdA.git"
	}
}
if (Test-Path "$folder\$project") { 
	cd "$folder\$project"
	git pull "https://$gitserver/$gituser/CdA.git"
	#git pull "https://username:password@$gitserver/$gituser/CdA.git"
	git status
}
$file = "requirements.txt"
if (Test-Path "$folder\$project\$file") { 
	cd "$folder\$project"
	python -m pip install -r "$folder\$project\$file" $myPipProxy
}