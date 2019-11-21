#plz replace all – with - , except in this line. those came from copy snipets from internet.

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
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:Home").Value + "\Desktop" }
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop" }
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:OneDrive").Value + "\Desktop" }
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

#check a bunch of TLS problems of PS defaults, ServicePointManager changes are applied per AppDomain ! for globally see https://johnlouros.com/blog/enabling-strong-cryptography-for-all-dot-net-applications and https://referencesource.microsoft.com/#System/net/System/Net/SecureProtocols/SslStream.cs,121
if (Test-Path "HKLM:\SOFTWARE\Wow6432Node\Microsoft\.NetFramework\v4.0.30319\SchUseStrongCrypto") {read-host "strong crypto not globaly enabled! Press ENTER to continue..."}
if (Test-Path "HKLM:\SOFTWARE\Microsoft\.NetFramework\v4.0.30319\SchUseStrongCrypto") {read-host "strong crypto not globaly enabled! Press ENTER to continue..."}
# set strong cryptography on 64 bit .Net Framework (version 4 and above)
#Set-ItemProperty -Path 'HKLM:\SOFTWARE\Wow6432Node\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -Type DWord
# set strong cryptography on 32 bit .Net Framework (version 4 and above)
#Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\.NetFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -Type DWord 

# default 
#[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::SystemDefault
# needed
#[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;

#to be stored in Microsoft.PowerShell_profile.ps1 and/or Microsoft.PowerShellISE_profile.ps1 ? 
#\OneDrive\Dokumente\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 \OneDrive\Dokumente\PowerShell\Microsoft.PowerShell_profile.ps1
#Else, it is a per session setting. The cmdlets like Invoke-RestMethod will always by default use, TLS 1.0
if ([System.Net.ServicePointManager]::SecurityProtocol -eq [System.Net.SecurityProtocolType]::SystemDefault){echo "PowerShell Transport Layer Security Protocols is maybe to weak (default)";
	#enable TLS1.2 for now:
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;
	#enter TLS1.2 into Powershell profile for next script too:
	$data = Get-Content -Raw -Path $profile; echo $data;
	if (!($data -like "*Net.ServicePointManager*")) {Add-Content $profile "# Configure PowerShell Transport Layer Security Protocols";
		Add-Content $profile "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12 ;";};
	$data = Get-Content -Path $profile; echo $data;}

####################################################################################################################################
#Invoke-RestMethod -Uri https://api.github.com/ -Method Get ;
#$exitCode = Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/README.md'; echo "exitcode was: $exitCode";
#$exitCode = Invoke-RestMethod 'https://github.com/kaestnja/CdA/raw/master/README.md'; echo "exitcode was: $exitCode";
##$exitCode = Invoke-WebRequest -Uri 'https://github.com/kaestnja/RdA/raw/master/README.md' -OutFile 'C:\Temp\README.md'; echo "exitcode was: $exitCode";
#$exitCode = Invoke-RestMethod 'https://code.siemens.com/jan.kaestner/RdA/raw/master/README.md'; echo "exitcode was: $exitCode";
#$exitCode = Invoke-RestMethod 'https://code.siemens.com/jan.kaestner/CdA/raw/master/README.md'; echo "exitcode was: $exitCode";
##$exitCode = Invoke-WebRequest -Uri 'https://code.siemens.com/jan.kaestner/RdA/raw/master/README.md' -OutFile 'C:\Temp\README.md'; echo "exitcode was: $exitCode";

#$myUri ="https://github.com/"
#$myUri ="https://github.com/kaestnja/RdA/raw/master/README.md"
#$myUri ="https://github.com/kaestnja/CdA/raw/master/README.md"
#$myUri ="https://code.siemens.com/jan.kaestner/RdA/raw/master/README.md"
#$myUri ="https://code.siemens.com/jan.kaestner/CdA/raw/master/README.md"
#[System.Net.ServicePointManager]::FindServicePoint($myUri)
#ServicePoint mySP = ServicePointManager.FindServicePoint(myUri);

#check proxy 
#[Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://username:password@proxy:port/", [EnvironmentVariableTarget]::Machine)
####################################################################################################################################
#Install-Module PowerShellGet -Scope CurrentUser -Force -AllowClobber
Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force
####################################################################################################################################
$temppath = "C:\Temp"
if (!($temppath | Test-Path)) { md -p "$temppath" }
if (Test-Path "$temppath") {
	cd $temppath

	#Install PScore6 
	#iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"
	$file = "PowerShell-6.2.3-win-x64.msi"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi -OutFile $path }
	#msiexec.exe /l*v mdbinstall.log /qb /i PowerShell-6.2.3-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1
	if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i PowerShell-6.2.3-win-x64.msi","/quiet","ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1","ENABLE_PSREMOTING=1","REGISTER_MANIFEST=1" }

	#Install Git 
	$file = "Git-2.24.0.2-64-bit.exe"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://github.com/git-for-windows/git/releases/download/v2.24.0.windows.2/Git-2.24.0.2-64-bit.exe -OutFile $path }
	#.\Git-2.24.0.2-64-bit.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /COMPONENTS="icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate" /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled
	#with ArgumentList as list
	if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/SILENT /NORESTART /NOCANCEL /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled /COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }
	#with ArgumentList as string array
	#if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/SILENT","/NORESTART","/NOCANCEL","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/NoIcons=0","/SetupType=default","/EditorOption=Nano","/PathOption=Cmd","/SSHOption=OpenSSH","/TortoiseOption=false","/CURLOption=OpenSSL","/CRLFOption=CRLFCommitAsIs","/BashTerminalOption=MinTTY","/PerformanceTweaksFSCache=Enabled","/UseCredentialManager=Enabled","/EnableSymlinks=Disabled","/EnableBuiltinInteractiveAdd=Disabled","/COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }

	#should be in Windows Path now: ";C:\Program Files (x86)\Git\cmd;C:\Program Files (x86)\Git\bin;"
	#$windows_path = $env:Path -split ';'
	#$path = (Get-Item "Env:ProgramFiles(x86)").Value + "\Git\bin"
	#if ($windows_path -notcontains $path) { if (Test-Path $path) { $env:path += ";" + $path } }
	#$windows_path = $env:Path -split ';'
	#$path = (Get-Item "Env:ProgramFiles(x86)").Value + "\Git\cmd"
	#if ($windows_path -notcontains $path) { if (Test-Path $path) { $env:path += ";" + $path } }

	$windows_path = $env:Path -split ';'
	$path = (Get-Item "Env:ProgramFiles").Value + "\Git\bin"
	if ($windows_path -notcontains $path) { if (Test-Path $path) { $env:path += ";" + $path } }
	$windows_path = $env:Path -split ';'
	$path = (Get-Item "Env:ProgramFiles").Value + "\Git\cmd"
	if ($windows_path -notcontains $path) { if (Test-Path $path) { $env:path += ";" + $path } }

	#add wget into Git 
	$file = "wget.exe"
	$folder = (Get-Item "Env:ProgramFiles").Value + "\Git\mingw64\bin"
	$path = "$folder\$file"
	if (Test-Path $folder) { if (!($path | Test-Path)) { curl https://eternallybored.org/misc/wget/1.20.3/64/wget.exe -OutFile $path } }

	#install python
	$file = "python-2.7.17.amd64.msi"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi -OutFile $path }
	if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i python-2.7.17.amd64.msi","/passive","/norestart" }

	$file = "python-3.8.0-amd64.exe"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe -OutFile $path }
	if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python38" }

	$file = "python-3.7.5-amd64.exe"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe -OutFile $path }
	if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python37","PrependPath=1" }

	$windows_path = $env:Path -split ';'
	$path = "C:\Python37\Scripts\"
	if ($windows_path -notcontains $path) { if (Test-Path $path) { $env:path += ";" + $path } }
	$windows_path = $env:Path -split ';'
	$path = "C:\Python37\"
	if ($windows_path -notcontains $path) { if (Test-Path $path) { $env:path += ";" + $path } }

	python --version
	python -m pip install --upgrade pip
	python -m pip install --upgrade setuptools
	python -m pip install --upgrade wheel

	#install mongodb
	$file = "mongodb-compass-community-1.19.12-win32-x64.msi"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://downloads.mongodb.com/compass/mongodb-compass-community-1.19.12-win32-x64.msi -OutFile $path }
	#developer gets a mongodb-compass as application, which is able to edit mongodb completely
	if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi" }
	if (!("C:\MongoDB\data" | Test-Path)) { md -p "C:\MongoDB\data" }
	if (!("C:\MongoDB\log" | Test-Path)) { md -p "C:\MongoDB\log" }
	$file = "mongodb-win32-x86_64-2012plus-4.2.1-signed.msi"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi -OutFile $path }
	#developer gets a mongodb as application (not as service), which have to be startet with a shortcut on the desktop
	if (Test-Path $path) { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerNoService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`"" }
	#C:\MongoDB\Server\4.2\bin\mongod.exe --dbpath "C:\MongoDB\data"  "C:\MongoDB\log" --bind_ip 127.0.0.1 --port 27017
	#C:\MongoDB\Server\4.2\bin\mongod.exe --bind_ip 127.0.0.1 --port 27017
	#find all home paths:  dir env:\home*
	$WshShell = New-Object -comObject WScript.Shell
	$folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop"
	if (!($folder | Test-Path)) { $folder = (Get-Item "Env:Home").Value + "\Desktop" }
	if (!($folder | Test-Path)) { $folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop" }
	if (!($folder | Test-Path)) { $folder = (Get-Item "Env:OneDrive").Value + "\Desktop" }
	if (Test-Path $folder) { 
		$Shortcut = $WshShell.CreateShortcut("$folder\MongoDB.lnk") 
		$Shortcut.TargetPath = "${env:ProgramFiles}\MongoDB\Server\4.2\bin\mongod.exe"
		$Shortcut.Arguments = "--dbpath `"C:\MongoDB\data`" --bind_ip 127.0.0.1 --port 27017"
		$Shortcut.Description = "start local MongoDB"
		#$Shortcut.IconLocation = "${env:ProgramFiles}\MongoDB\Server\4.2\bin\mongod.exe, 1"
		$Shortcut.WindowStyle = "1"
		$Shortcut.WorkingDirectory = "${env:ProgramFiles}\MongoDB\Server\4.2\bin"
		$Shortcut.Save()}
	
	#developer gets an allround editor
	$file = "npp.7.7.1.Installer.x64.exe"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe -OutFile $path }
	#if (Test-Path $path) { Start-Process -Wait -FilePath "npp.7.7.1.Installer.x64.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/S" }
	if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/S" }
	$file = "npp.7.8.1.Installer.x64.exe"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl http://download.notepad-plus-plus.org/repository/7.x/7.8.1/npp.7.8.1.Installer.x64.exe -OutFile $path }
	#if (Test-Path $path) { Start-Process -Wait -FilePath "npp.7.8.1.Installer.x64.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/S" }
	if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/S" }

	#https://asawicki.info/news_1597_installing_visual_c_redistributable_package_from_command_line.html
	#https://docs.microsoft.com/de-de/visualstudio/releases/2019/system-requirements
	#https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container?view=vs-2017
	$file = "vs_buildtools_2019.exe"
	$path = "$temppath\$file"
	if (!($path | Test-Path)) { curl https://github.com/kaestnja/RdA/raw/master/PSRdA/vs/vs_buildtools_2019.exe -OutFile $path }
	#if (Test-Path $path) { Start-Process -Wait -FilePath "vs_buildtools_2019.exe" -WorkingDirectory "C:\Temp" -ArgumentList "/S" }
	#if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "--update","--quiet","--wait" }
	if (Test-Path $path) { 
		#$exitCode = Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "--update","--quiet","--wait" 
		$exitCode = Start-Process -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "--update","--passive","--wait" -Wait -PassThru;
		echo "exitcode was: + $exitCode";
		read-host "Press ENTER to continue...";
		}
	#vs_enterprise.exe [command] <options>
	#vs_enterprise.exe --add Microsoft.VisualStudio.Workload.CoreEditor --passive --norestart
	#vs_enterprise.exe --update --quiet --wait
	#vs_enterprise.exe update --wait --passive --norestart --installPath "C:\installPathVS"
	#vs_enterprise.exe --installPath C:\desktopVS --addProductLang fr-FR --add Microsoft.VisualStudio.Workload.ManagedDesktop --includeRecommended --quiet --wait

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

$githubProjectServer = 'github.com'
$SiemensProjectServer = 'code.siemens.com'

ssh -T git@$githubProjectServer
ssh -T git@$SiemensProjectServer

#~/.ssh/config
#Connect-Ssh
#Add-SshConnection -Name githubProjectServer -Uri $githubProjectServer -User kaestnja
#Add-SshConnection -Name Server1 -Uri server1.jeremyskinner.co.uk -User jeremy
#Start-SshAgent -Quiet

#Get-Item "Env:"
#get-childitem -path env:* | get-member
#get git CdA
$project = "CdA"
$folder = (Get-Item "Env:USERPROFILE").Value + "\source\repos\github.com"
$path = "$folder\$project"
if (Test-Path (Get-Item "Env:USERPROFILE").Value) { if (!($folder | Test-Path)) { md -p $folder } }
if (Test-Path $folder) { if (!($path | Test-Path)) { 
	cd $folder
	git clone "https://github.com/kaestnja/CdA.git" 
	#git clone "https://username:password@code.siemens.com/jan.kaestner/CdA.git"
	}
}
if (Test-Path $path) { 
	cd $path
	git pull "https://github.com/kaestnja/CdA.git"
	#git pull "https://username:password@code.siemens.com/jan.kaestner/CdA.git"
	git status
}

$project = "CdA"
$folder = (Get-Item "Env:USERPROFILE").Value + "\source\repos\github.com"
$path = "$folder\$project"
if (Test-Path $path) { 
	cd $path
	git pull "https://github.com/kaestnja/CdA.git"
	#git pull "https://username:password@code.siemens.com/jan.kaestner/CdA.git"
	python -m pip install -r requirements.txt
	git status
}


Function Pause ($Message = "Press any key to continue...") {
   # Check if running in PowerShell ISE
   If ($psISE) {
      # "ReadKey" not supported in PowerShell ISE.
      # Show MessageBox UI
      $Shell = New-Object -ComObject "WScript.Shell"
      $Button = $Shell.Popup("Click OK to continue.", 0, "Hello", 0)
      Return
   }
 
   $Ignore =
      16,  # Shift (left or right)
      17,  # Ctrl (left or right)
      18,  # Alt (left or right)
      20,  # Caps lock
      91,  # Windows key (left)
      92,  # Windows key (right)
      93,  # Menu key
      144, # Num lock
      145, # Scroll lock
      166, # Back
      167, # Forward
      168, # Refresh
      169, # Stop
      170, # Search
      171, # Favorites
      172, # Start/Home
      173, # Mute
      174, # Volume Down
      175, # Volume Up
      176, # Next Track
      177, # Previous Track
      178, # Stop Media
      179, # Play
      180, # Mail
      181, # Select Media
      182, # Application 1
      183  # Application 2
 
   Write-Host -NoNewline $Message
   While ($KeyInfo.VirtualKeyCode -Eq $Null -Or $Ignore -Contains $KeyInfo.VirtualKeyCode) {
      $KeyInfo = $Host.UI.RawUI.ReadKey("NoEcho, IncludeKeyDown")
   }
}