#Requires -RunAsAdministrator
param([switch]$Elevated)
#start it via: Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites_contributor.ps1') }"
#$ErrorActionPreference = 'SilentlyContinue'
#$ErrorActionPreference = 'Continue'

function Test-Admin {
  $currentPrincipal = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
  $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}
function Test-RegistryValue {param ( [parameter(Mandatory=$true)] [ValidateNotNullOrEmpty()]$Path,[parameter(Mandatory=$true)] [ValidateNotNullOrEmpty()]$Value)
    $Error.clear()
    try {
        Get-ItemProperty -Path $Path | Select-Object -ExpandProperty $Value -ErrorAction Stop | Out-Null
        return $true
        }
    catch {
        return $false
    }
}


#plz replace all wrong characters like –   with - " , except in this line. those came from copying snipets from internet.
$temppath = "C:\Temp"
$gitserver = 'github.com'
$gituser = 'kaestnja'
$version = '0.0.4'
$myname = 'setup_prerequisites_contributor.ps1'
$keyRunOnce = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce'
$Error.clear()
#echo "version: " + $version
Write-Host -ForegroundColor Green "version:" + $version

$keyValue = $myname
If (Test-RegistryValue -Path $keyRunOnce -Value $keyValue){
    Write-Host -ForegroundColor Yellow "this script seems like to run from a CurrentUser RunOnce registry entry, which will be removed now(!)"
    #Remove-ItemProperty -Path $keyRunOnce -Name $keyValue -ErrorVariable 'MyError' -ErrorAction "SilentlyContinue"
    #Remove-ItemProperty -Path $keyRunOnce -Name $keyValue -ErrorAction "SilentlyContinue"
    Remove-ItemProperty -Path $keyRunOnce -Name $keyValue *>&1 | out-null
    #Remove-ItemProperty -Path $keyRunOnce -Name $keyValue
}


if ((Test-Admin) -eq $false){
	read-host "This code have to be run elevate, which is not the case now.";
    if ($elevated) {
        read-host "tried to elevate, did not work";
    }else{
		read-host "try to download the same script for running it local now..."
		if (!($temppath | Test-Path)) { md -p "$temppath" }
		if (Test-Path "$temppath") { Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/PSRdA/setup_prerequisites_contributor.ps1" -OutFile "$temppath\setup_prerequisites_contributor.ps1";}
		if (Test-Path "$temppath\setup_prerequisites_contributor.ps1") { 
            read-host "have the same script, now try to elevate and run the second instance local now...";
			#Unblock-File -Path '$temppath\setup_prerequisites_contributor.ps1';
			Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f "$temppath\setup_prerequisites_contributor.ps1");
            #Start-Process -FilePath "powershell" -ArgumentList "$('-File ""')$(Get-Location)$('\')$($MyInvocation.MyCommand.Name)$('""')" -Verb runAs;
		}
		#Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites_contributor.ps1') }"
		#Start-Process powershell -verb runas -ArgumentList "-file fullpathofthescript"
        #Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
		#Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites_contributor.ps1') }"))
	}
    read-host "aborting this script now (!)";
	exit;
}

read-host "aborting anything now";
exit;
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
if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\Desktop")) { echo "found: cd $($(Get-Item "Env:USERPROFILE").Value + "\Desktop")" }

#eventually prepare executability
Get-ExecutionPolicy
#Set-ExecutionPolicy RemoteSigned
#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Confirm

#enable the verry long names for files and paths, just for sure
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control" -Name "FileSystem@LongPathsEnabled" -Value 1
#prevent download fails, if internet explorer was not first initilized with recommended microsoft settings
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Internet Explorer\Main" -Name "DisableFirstRunCustomize" -Value 2

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
	Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/PSRdA/setup_prerequisites_contributor.ps1" -OutFile "$temppath\setup_prerequisites_contributor.ps1";

	#check for a needed system reboot, which should be done first
	if ((Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired") -bor
	(Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending")  -bor
	(Test-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations") -bor
	(Test-Path "HKLM:\SYSTEM\ControlSet001\Control\Session Manager\PendingFileRenameOperations") -bor
	(Test-Path "HKLM:\SYSTEM\ControlSet002\Control\Session Manager\PendingFileRenameOperations") -bor
	(Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\InProgress") ) {
		read-host "reboot needed! Press ENTER to going to reboot now.";
		if (Test-Path "$temppath\setup_prerequisites_contributor.ps1") {
			Write-Host "Changing RunOnce script." -foregroundcolor "magenta"
			read-host "To continue after reboot, this script is called once after login the same user...";
	        $Command = "%systemroot%\System32\WindowsPowerShell\v1.0\powershell.exe -executionpolicy bypass -file $temppath\setup_prerequisites_contributor.ps1";
			#$Command = "%systemroot%\System32\WindowsPowerShell\v1.0\PowerShell.exe -NoProfile -ExecutionPolicy Unrestricted -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Unrestricted -File ""C:\Users\UserName\Desktop\-online.ps1""' -Verb RunAs}";
            $keyValue = $myname
            if (Test-RegistryValue -Path $keyRunOnce -Value $keyValue){
                Set-ItemProperty -Path $keyRunOnce -Name $keyValue -Value $Command
                }else{
                New-ItemProperty -Path $keyRunOnce -Name $keyValue -Value $Command -PropertyType ExpandString
            }
		}
	}

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
	$file = "python-2.7.17.amd64.msi"
	if (!("$temppath\$file" | Test-Path)) { curl https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i python-2.7.17.amd64.msi","/passive","/norestart" }

	$file = "python-3.8.0-amd64.exe"
	if (!("$temppath\$file" | Test-Path)) { curl https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python38" }

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
	#developer gets a mongodb-compass as application, which is able to edit mongodb completely
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi" }
	
	if (!("C:\MongoDB\data" | Test-Path)) { md -p "C:\MongoDB\data" }
	if (!("C:\MongoDB\log" | Test-Path)) { md -p "C:\MongoDB\log" }
	$file = "mongodb-win32-x86_64-2012plus-4.2.1-signed.msi"
	if (!("$temppath\$file" | Test-Path)) { curl https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi -OutFile "$temppath\$file" }
	#developer gets a mongodb as application (not as service), which have to be startet with a shortcut on the desktop
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerNoService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`"" }
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
	if (!("$temppath\$file" | Test-Path)) { curl https://notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/S" }
	$file = "npp.7.8.1.Installer.x64.exe"
	if (!("$temppath\$file" | Test-Path)) { curl http://download.notepad-plus-plus.org/repository/7.x/7.8.1/npp.7.8.1.Installer.x64.exe -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/S" }

	#developer gets minimum c++ 14.0 for levenshtein and complete ide for python and django webdeployment
    Get-PSRepository
    Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted
	$vsconfig_vs_buildtools_2019 = 	"`"--add Microsoft.VisualStudio.Workload.MSBuildTools`",`"--add Microsoft.VisualStudio.Workload.VCTools`",`"--add Microsoft.Component.MSBuild`",`"--add Microsoft.VisualStudio.Component.Roslyn.Compiler`",`"--add Microsoft.VisualStudio.Component.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.Windows10SDK`",`"--add Microsoft.VisualStudio.Component.VC.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64`",`"--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest`",`"--add Microsoft.VisualStudio.Component.Windows10SDK.18362`",`"--add Microsoft.VisualStudio.Component.VC.CMake.Project`",`"--add Microsoft.VisualStudio.Component.TestTools.BuildTools`",`"--add Microsoft.VisualStudio.Component.WebDeploy`""
	$vsconfig_vs_enterprise_2019 = 	"`"--add Microsoft.VisualStudio.Workload.CoreEditor`",`"--add Microsoft.VisualStudio.Workload.VCTools`",`"--add Microsoft.VisualStudio.Workload.Python`",`"--add Microsoft.VisualStudio.Workload.NativeDesktop`",`"--add Microsoft.Component.MSBuild`",`"--add Microsoft.Component.PythonTools`",`"--add Microsoft.Component.PythonTools.Web`",`"--add Microsoft.VisualStudio.Component.Roslyn.Compiler`",`"--add Microsoft.VisualStudio.Component.CoreEditor`",`"--add Microsoft.VisualStudio.Component.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.Windows10SDK`",`"--add Microsoft.VisualStudio.Component.VC.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64`",`"--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest`",`"--add Microsoft.VisualStudio.Component.Windows10SDK.18362`",`"--add Microsoft.VisualStudio.Component.VC.CMake.Project`",`"--add Microsoft.VisualStudio.Component.VC.CoreIde`",`"--add Microsoft.VisualStudio.Component.WebDeploy`""
	$file = "vs_buildtools.exe"
    #https://aka.ms/vs/16/release/vs_buildtools.exe
    if (!("$temppath\$file" | Test-Path)) { curl "https://aka.ms/vs/16/release/$file" -OutFile "$temppath\$file" }
	#if (!("$temppath\$file" | Test-Path)) { curl "https://$gitserver/$gituser/RdA/raw/master/PSRdA/vs/$file" -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { 

		echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--update`",`"--passive`",`"--wait`" -Wait -PassThru;"
		Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--update","--passive","--wait" -Wait -PassThru;
		read-host "To continue after update";
		echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--passive`",`"--wait`",$vsconfig_vs_buildtools_2019 -Wait -PassThru;"
		Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--passive","--wait",$vsconfig_vs_buildtools_2019 -Wait -PassThru;
		read-host "To continue after vs_buildtools_2019";
		}
	$file = "vs_enterprise_2019.exe"
	if (!("$temppath\$file" | Test-Path)) { curl "https://$gitserver/$gituser/RdA/raw/master/PSRdA/vs/$file" -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { 
		echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--update`",`"--passive`",`"--wait`" -Wait -PassThru;"
		Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--update","--passive","--wait" -Wait -PassThru;
		read-host "To continue after update";
		echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--passive`",`"--wait`",$vsconfig_vs_enterprise_2019 -Wait -PassThru;"
		Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--passive","--wait",$vsconfig_vs_enterprise_2019 -Wait -PassThru;
		read-host "To continue after vs_enterprise_20199";
		}
	#vs_enterprise.exe [command] <options>
	#vs_enterprise.exe --add Microsoft.VisualStudio.Workload.CoreEditor --passive --norestart
	#vs_enterprise.exe --add Microsoft.VisualStudio.Workload.CoreEditor --passive --norestart
	#vs_enterprise.exe --update --quiet --wait
	#vs_enterprise.exe update --wait --passive --norestart --installPath "C:\installPathVS"
	#vs_enterprise.exe --installPath C:\desktopVS --addProductLang fr-FR --add Microsoft.VisualStudio.Workload.ManagedDesktop --includeRecommended --quiet --wait
	##Start-Process -FilePath "C:\Temp\vs_buildtools_2019.exe" -WorkingDirectory "C:\Temp" -ArgumentList "--update","--passive","--wait","--quiet","--add Microsoft.VisualStudio.Workload.MSBuildTools" -Wait -PassThru;
	##Start-Process -FilePath "C:\Temp\vs_buildtools_2019.exe" -WorkingDirectory "C:\Temp" -ArgumentList "--update","--passive","--wait","--quiet","--add Microsoft.VisualStudio.Workload.MSBuildTools" -Wait -PassThru;


	#rem in case missing ...error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools", repeat:
	#python -m pip install --upgrade python-bsonjs
	#python -m pip install --upgrade pyxdameraulevenshtein
	#https://asawicki.info/news_1597_installing_visual_c_redistributable_package_from_command_line.html
	#https://docs.microsoft.com/de-de/visualstudio/releases/2019/system-requirements
	#https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container?view=vs-2017
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
if (Test-Path $($(Get-Item "Env:USERPROFILE").Value)) { echo "found: $($(Get-Item "Env:USERPROFILE").Value)" }
if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\source")) { echo "found: $($(Get-Item "Env:USERPROFILE").Value + "\source")" }
#get git CdA
$project = "CdA"
$folder = (Get-Item "Env:USERPROFILE").Value + "\source\repos\$gitserver\$gituser"
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


#"$folder\MongoDB.lnk"
$file = "mongod.exe"
if (Test-Path "${env:ProgramFiles}\MongoDB\Server\4.2\bin\$file") { 
	#cd "$folder\$project"
	#python "$folder\$project\$file"
	#Invoke-Expression "& { $(python "$folder\$project\$file") }"
	#python $home\source\repos\github.com\kaestnja\CdA\PyCdA.py
	#Invoke-Expression "& { $(python "$home\source\repos\github.com\kaestnja\CdA\PyCdA.py") }"
	Start-Process -FilePath "${env:ProgramFiles}\MongoDB\Server\4.2\bin\mongod.exe" -WorkingDirectory "${env:ProgramFiles}\MongoDB\Server\4.2\bin" -ArgumentList "--dbpath `"C:\MongoDB\data`"","--bind_ip 127.0.0.1","--port 27017" -PassThru;
}

$file = "PyCdA.py"
if (Test-Path "$folder\$project\$file") { 
	cd "$folder\$project"
	#python "$folder\$project\$file"
	Invoke-Expression "& { $(python "$folder\$project\$file") }"
	#python $home\source\repos\github.com\kaestnja\CdA\PyCdA.py
	#Invoke-Expression "& { $(python "$home\source\repos\github.com\kaestnja\CdA\PyCdA.py") }"
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