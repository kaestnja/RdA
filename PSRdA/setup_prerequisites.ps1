#Requires -RunAsAdministrator
param([switch]$Elevated,[parameter(HelpMessage="can be one of:expert,server,contributor or just nothing")][String]$setuptype,[parameter(HelpMessage="reinstalls anything, if set to true")][Boolean]$force)
#start it via: Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') }"
#start it via: Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') } -setuptype 'contributor' "

#plz replace all wrong characters like – with - " , except in this line. those came from copying snipets from internet.
if ( (!($setuptype -like '*expert*')) -and (!($setuptype -like '*server*')) -and (!($setuptype -like '*contributor*')) ) {
	Write-Host -ForegroundColor Red "setuptype wrong:" + $setuptype
	read-host "proceed as contributor now";
	$setuptype = "contributor"
	}
$force = 0 #"force"
$temppath = "C:\Temp"
$gitserver = 'github.com'
$gituser = 'kaestnja'
$version = '0.0.22'
$myname = 'setup_prerequisites.ps1'
$prerequisitesyaml = '' 
$prerequisitesyamlurl = "https://$gitserver/$gituser/RdA/raw/master/prerequisites.yaml"
$keyRunOnce = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce'
$Error.clear()
#echo "version: " + $version
Write-Host -ForegroundColor Green "version:" + $version
#$ErrorActionPreference = 'SilentlyContinue'
#$ErrorActionPreference = 'Continue'

$gitfile = "Git-2.27.0-64-bit.exe"
$giturl = "https://github.com/git-for-windows/git/releases/download/v2.27.0.windows.1/Git-2.27.0-64-bit.exe"
$pythonurl37 = "https://www.python.org/ftp/python/3.7.8/python-3.7.8-amd64.exe"
$pythonurl38 = "https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe"
$powershellurl62 = "https://github.com/PowerShell/PowerShell/releases/download/v6.2.7/PowerShell-6.2.7-win-x64.msi"
$powershellurl70 = "https://github.com/PowerShell/PowerShell/releases/download/v7.0.3/PowerShell-7.0.3-win-x64.msi"

function Test-Admin {
	$currentPrincipal = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
	$currentPrincipal.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}
function Test-RegistryValue {param ( [parameter(Mandatory=$true)] [ValidateNotNullOrEmpty()]$Path,[parameter(Mandatory=$true)] [ValidateNotNullOrEmpty()]$Value)
    $Error.clear()
    try {
        #Get-ItemProperty -Path $Path | Select-Object -ExpandProperty $Value -ErrorAction Stop | Out-Null
        Get-ItemProperty -Path $Path -Name $Value -ErrorAction Stop | Out-Null
        return $true
        }
    catch {
        return $false
    	}
}
#Function Test-RegistryValue { param([string]$RegKeyPath,[string]$Value)
#    $ValueExist = (Get-ItemProperty $RegKeyPath).$Value -ne $null
#    Return $ValueExist
#}
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
function get-FileFromUri {
    param(
        [Parameter(Mandatory = $true,Position = 0,ValueFromPipeline = $true,ValueFromPipelineByPropertyName = $true)]
        [string]
        $Url,
        [Parameter(Mandatory = $false,Position = 1)]
        [string]
        [Alias('Folder')]
        $FolderPath
      )
      process {
		  # doit
			try {
				# resolve short URLs
				$req = [System.Net.HttpWebRequest]::Create($Url)
				$req.Method = "HEAD"
				$response = $req.GetResponse()
				$fUri = $response.ResponseUri
				$filename = [System.IO.Path]::GetFileName($fUri.LocalPath);
				$response.Close()
				# download file
				$destination = (Get-Item -Path ".\" -Verbose).FullName
				if ($FolderPath) { $destination = $FolderPath }
				if ($destination.EndsWith('\')) {
				$destination += $filename
				} else {
				$destination += '\' + $filename
				}
				$webclient = New-Object System.Net.webclient
				$webclient.downloadfile($fUri.AbsoluteUri,$destination)
				Write-Host -ForegroundColor DarkGreen "downloaded '$($fUri.AbsoluteUri)' to '$($destination)'"
			} catch {
				Write-Host -ForegroundColor DarkRed $_.Exception.Message
			}
		return $filename
		}
}



$giturl_file = get-FileFromUri $giturl $temppath
Write-Host $gitfile
Write-Host $giturl_file
exit



$keyValue = $myname
If (Test-RegistryValue -Path $keyRunOnce -Value $keyValue){
    Write-Host -ForegroundColor Yellow "this script seems like to run from a CurrentUser RunOnce registry entry, which will be removed now(!)"
    #Remove-ItemProperty -Path $keyRunOnce -Name $keyValue -ErrorVariable 'MyError' -ErrorAction "SilentlyContinue"
    #Remove-ItemProperty -Path $keyRunOnce -Name $keyValue -ErrorAction "SilentlyContinue"
    #Remove-ItemProperty -Path $keyRunOnce -Name $keyValue *>&1 | out-null
    Remove-ItemProperty -Path $keyRunOnce -Name $keyValue
}

Write-Host "check Admin Mode---------------------" -foregroundcolor "white"
if ((Test-Admin) -eq $false){
	read-host "This code have to be run elevate, which is not the case now.";
    if ($elevated) {
        Write-Host -ForegroundColor Red "tried to elevate, did not work";
    } else {
		Write-Host -ForegroundColor Yellow "try to download the same script for running it local now..."
		if (!($temppath | Test-Path)) { md -p "$temppath" }
		if (Test-Path "$temppath") { Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/PSRdA/setup_prerequisites.ps1" -OutFile "$temppath\setup_prerequisites.ps1";}
		if (Test-Path "$temppath\setup_prerequisites.ps1") { 
            Write-Host  -ForegroundColor Green "have the same script locally."
            if ($setuptype -eq "contributor"){
                read-host  -ForegroundColor Red "will now try to elevate into a second and administrative, but local instance now...";
			    #Unblock-File -Path '$temppath\setup_prerequisites.ps1';
			    Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f "$temppath\setup_prerequisites.ps1 -setuptype 'contributor'");
                #Start-Process -FilePath "powershell" -ArgumentList "$('-File ""')$(Get-Location)$('\')$($MyInvocation.MyCommand.Name)$('""')" -Verb runAs;
            }
		}
		#Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') }"
		#Start-Process powershell -verb runas -ArgumentList "-file fullpathofthescript"
        #Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
		#Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') }"))
	}
	exit;
}
Write-Host "check SSH with Git Server---------------------" -foregroundcolor "white"
ssh -T "git@$gitserver"

#~/.ssh/config
#Connect-Ssh
#Add-SshConnection -Name gitserver -Uri "$gitserver" -User "$gituser""
#Add-SshConnection -Name Server1 -Uri server1.jeremyskinner.co.uk -User jeremy
#Start-SshAgent -Quiet

#Get-ChildItem -Path Env:\
#Set-Location -Path Env:\
#Get-ChildItem -Path COMPUTERNAME,Path
#$env:Path                                                      #session wise user context environment variables
#[System.Environment]::GetEnvironmentVariable('PATH')           #permament wise user context environment variables
#[System.Environment]::GetEnvironmentVariable('PATH','machine') #permament wise system context environment variables, like "Machine, Process or User"
#[System.Environment]::SetEnvironmentVariable('FOO', 'bar',[System.EnvironmentVariableTarget]::Machine)

#check proxy maybe set proxy
#[Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://username:password@proxy:port/", [EnvironmentVariableTarget]::Machine)
#$myPipProxy='--proxy=http://194.145.60.1:9400'
#$myPipProxy='--proxy=http://server:port'
#$myPipProxy='--proxy=https://user@server:port'
#$myPipProxy='--proxy=https://user:pass@server:port'

#report some important info
#get-wmiobject win32_operatingsystem | select @{Name="Installed"; Expression={$_.ConvertToDateTime($_.InstallDate)}}, Caption
#$osinfo = (Get-CimInstance -ClassName win32_operatingsystem).name.split("|")[0]
#$osinfo = (Get-WMIObject win32_operatingsystem).name.split("|")[0] + " " + (Get-WmiObject Win32_OperatingSystem).OSArchitecture + " " + (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\').BuildLabEx
$osinfo = (Get-CimInstance -ClassName win32_operatingsystem).name.split("|")[0] + " " + (Get-CimInstance -ClassName win32_operatingsystem).OSArchitecture + " " + (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\').BuildLabEx
#wmic os get caption
#wmic os get osarchitecture
#(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\').BuildLabEx
Write-Host -foregroundcolor "green" $osinfo
#Get-Content C:\test1\testfile2.txt | Out-String
$psinfo = ForEach-Object {"$($PSVersionTable.PSVersion)"}
$psinfo = "Powershell Version: " + $psinfo
Write-Host -foregroundcolor "green" $psinfo

#check and generate the Powershell profile, maybe the session have to be restarted?
if (!($profile | Test-Path)) {
	Write-Host -foregroundcolor "yellow" "no powershell profile found, create it now";
	New-Item -path $profile -type file -force
} else {Write-Host -foregroundcolor "green" "current powershell profile: $profile"}


#identify the correct userprofile path, need to prepare desktop links and others
#Get-Childitem env:
#Get-Childitem -path env:* | get-member
$folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop"
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:USERPROFILE").Value + "\Desktop" }
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:OneDrive").Value + "\Desktop" }
if (!($folder | Test-Path)) { $folder = (Get-Item "Env:Home").Value + "\Desktop" }
if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\Desktop")) { echo "found: $($(Get-Item "Env:USERPROFILE").Value + "\Desktop")" }

#eventually prepare executability
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned
#Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Confirm

#enable the verry long names for files and paths, just for sure
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control" -Name "FileSystem@LongPathsEnabled" -Value 1
#prevent download fails, if internet explorer was not first initilized with recommended microsoft settings
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Internet Explorer\Main" -Name "DisableFirstRunCustomize" -Value 2

Write-Host "check Security Protocols---------------------" -foregroundcolor "white"
if ([System.Net.ServicePointManager]::SecurityProtocol -eq [System.Net.SecurityProtocolType]::SystemDefault){echo "PowerShell Transport Layer Security Protocols is maybe to weak (default)";
	#to enable TLS1.2 for now: [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;
	[Net.ServicePointManager]::SecurityProtocol = ([Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12);
	#enter TLS1.2 into Powershell profile for next script too:
	$data = Get-Content -Raw -Path $profile; echo $data;
	if (!($data -like "*Net.ServicePointManager*")) {Add-Content $profile "# Configure PowerShell Transport Layer Security Protocols";
		Add-Content $profile "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12 ;";};
	$data = Get-Content -Path $profile; echo $data;
}

####################################################################################################################################
Write-Host "check PowerShell---------------------" -foregroundcolor "white"
if (Get-InstalledModule -Name "PowerShellGet" -MinimumVersion 2.2.4){
    Write-Host "PowerShellGet is up to date" -foregroundcolor "green"
} else {
    Write-Host "PowerShellGet will be updated now" -foregroundcolor "yellow"
    #Remove-Module -Name "PowerShellGet" -force
    #Uninstall-Module -Name "PowerShellGet"  -AllVersions -force
    #Remove-Module -Name "PackageManagement" -force
    #Uninstall-Module -Name "PackageManagement"  -AllVersions -force

    #Install-PackageProvider Nuget -force -verbose
    Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.208 -Force -ErrorAction Stop | Out-Null
    #Get-Module -ListAvailable
    #Find-Module -Name PowerShellGet*
    #Find-Module -Name PackageManagement*
    #Install-Module PowerShellGet -Scope AllUsers -Force -AllowClobber -ErrorAction Stop | Out-Null
    #Install-Module -Name PowerShellGet -Force -Verbose
    Install-Module -Name PowerShellGet -RequiredVersion 2.2.1 -Force -Scope AllUsers -AllowClobber -ErrorAction Continue -SkipPublisherCheck | Out-Null
    }
Update-Module -Name PowerShellGet
#Get-PSRepository
Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted

Install-Module powershell-yaml
#Install-Module -Name powershell-yaml -Force -Repository PSGallery -Scope AllUsers #CurrentUser
Update-Module -Name powershell-yaml
Import-Module powershell-yaml
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
$prerequisitesyaml = ''
if (!($temppath | Test-Path)) { md -p "$temppath" }
if (Test-Path "$temppath") {
	Write-Host "check additional files---------------------" -foregroundcolor "white"
	cd $temppath
	Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/README.md" -OutFile "$temppath\README_RdA_Github.md";
	#Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/prerequisites.yaml" -OutFile "$temppath\prerequisites.yaml";
	#Invoke-WebRequest -Uri "https://$gitserver/$gituser/CdA/blob/master/prerequisites.yaml" -OutFile "$temppath\prerequisites.yaml";
	#Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kaestnja/CdA/master/prerequisites.yaml" -OutFile "$temppath\prerequisites.yaml";
	#Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/requirements.txt" -OutFile "$temppath\requirements.txt";
	#Invoke-WebRequest -Uri "https://$gitserver/$gituser/CdA/blob/master/requirements.txt" -OutFile "$temppath\requirements.txt";
	#Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kaestnja/CdA/master/requirements.txt" -OutFile "$temppath\requirements.txt";
	Invoke-WebRequest -Uri "https://$gitserver/$gituser/RdA/raw/master/PSRdA/setup_prerequisites.ps1" -OutFile "$temppath\setup_prerequisites.ps1";

	[string[]]$fileContent = Get-Content "$temppath\prerequisites.yaml"
	$content = ''
	foreach ($line in $fileContent) { $content = $content + "`n" + $line }
	$prerequisitesyaml = ConvertFrom-YAML $content

	#check for a needed system reboot, which should be done first
	Write-Host "check RebootRequiered---------------------" -foregroundcolor "white"
	if ((Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired") -bor
	(Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending")  -bor
	(Test-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations") -bor
	(Test-Path "HKLM:\SYSTEM\ControlSet001\Control\Session Manager\PendingFileRenameOperations") -bor
	(Test-Path "HKLM:\SYSTEM\ControlSet002\Control\Session Manager\PendingFileRenameOperations") -bor
	(Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\InProgress") ) {
		read-host "reboot needed! Press ENTER to going to reboot now.";
		if (Test-Path "$temppath\setup_prerequisites.ps1") {
			Write-Host "Changing RunOnce script." -foregroundcolor "magenta"
			read-host "To continue after reboot, this script is called once after login the same user...";
	        $Command = "%systemroot%\System32\WindowsPowerShell\v1.0\powershell.exe -executionpolicy bypass -file $temppath\setup_prerequisites.ps1 -setuptype 'contributor'";
			#$Command = "%systemroot%\System32\WindowsPowerShell\v1.0\PowerShell.exe -NoProfile -ExecutionPolicy Unrestricted -Command "& {Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Unrestricted -File ""C:\Users\UserName\Desktop\-online.ps1""' -Verb RunAs}";
            $keyValue = $myname
            if (Test-RegistryValue -Path $keyRunOnce -Value $keyValue){
                Set-ItemProperty -Path $keyRunOnce -Name $keyValue -Value $Command
            } else {
                New-ItemProperty -Path $keyRunOnce -Name $keyValue -Value $Command -PropertyType ExpandString
            }
		}
	}
	Write-Host "check PowerShell Core (V6)---------------------" -foregroundcolor "white"
	#Install PScore6 
    #$key = "HKLM:\Software\Microsoft\PowerShell\1\Install"
    #$key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\PowerShellEngine\PowerShellVersion"
    #$key = "HKLM:\SOFTWARE\Microsoft\PowerShell\3"
    $key = "HKLM:\SOFTWARE\Microsoft\PowerShellCore\InstalledVersions\31ab5147-9a97-4452-8443-d9709f0516e1"
    $keyValue = "SemanticVersion"
    if (!(Test-Path $key )){
        Write-Host "Powershell 6 missing" -foregroundcolor "yellow"
        if (!(Test-RegistryValue -Path $key -Value $keyValue)){
            Write-Host "Powershell 6 not identified" -foregroundcolor "yellow"
            #iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"
	        $file = "PowerShell-6.2.7-win-x64.msi"
	        if (!("$temppath\$file" | Test-Path)) { curl https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi -OutFile "$temppath\$file" }
	        #msiexec.exe /l*v mdbinstall.log /qb /i PowerShell-6.2.3-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1
	        if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i PowerShell-6.2.3-win-x64.msi","/quiet","ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1","ENABLE_PSREMOTING=1","REGISTER_MANIFEST=1" }
        }
    }








    #Install Git 
	Write-Host "check Git---------------------" -foregroundcolor "white"
	$testupdategit = ''
    try
    {
        git | Out-Null
		$testupdategit = git --version
		Write-Host "Git is installed, $testupdategit" -foregroundcolor "green" #git version 2.24.0.windows.2
		if ( (!($testupdategit -like '*2.27*')) ){
			git update-git-for-windows
		}
        #git update-git-for-windows
		#$testupdategit = ''
		#$testupdategit = git update-git-for-windows | Out-Null
    }
    catch [System.Management.Automation.CommandNotFoundException]
    {
        Write-Host "Git is not installed" -foregroundcolor "red"
    }
	#$file = "Git-2.24.1.2-64-bit.exe"
	#$gitfile = "Git-2.25.0-64-bit.exe"
	#$giturl = "https://github.com/git-for-windows/git/releases/download/v2.25.0.windows.1/Git-2.25.0-64-bit.exe" 
    $isGitInstalled = $null -ne ( (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*) + (Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*) | Where-Object { $null -ne $_.DisplayName -and $_.Displayname.Contains('Git') })
    if ( (!($isGitInstalled )) -or (!($testupdategit -like '*2.27*')) ){
		#if (!("$temppath\$file" | Test-Path)) { curl https://github.com/git-for-windows/git/releases/download/v2.24.1.windows.2/Git-2.24.1.2-64-bit.exe -OutFile "$temppath\$file" }
		if (!("$temppath\$gitfile" | Test-Path)) { curl "$giturl" -OutFile "$temppath\$gitfile" }
	    #.\Git-2.24.0.2-64-bit.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /COMPONENTS="icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh,autoupdate" /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled
	    #with ArgumentList as list
	    if (Test-Path "$temppath\$gitfile") { Start-Process -Wait -FilePath "$temppath\$gitfile" -WorkingDirectory "$temppath" -ArgumentList "/SILENT /NORESTART /NOCANCEL /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /NoIcons=0 /SetupType=default /EditorOption=Nano /PathOption=Cmd /SSHOption=OpenSSH /TortoiseOption=false /CURLOption=OpenSSL /CRLFOption=CRLFCommitAsIs /BashTerminalOption=MinTTY /PerformanceTweaksFSCache=Enabled /UseCredentialManager=Enabled /EnableSymlinks=Disabled /EnableBuiltinInteractiveAdd=Disabled /COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }
	    #with ArgumentList as string array
	    #if (Test-Path $path) { Start-Process -Wait -FilePath "$path" -WorkingDirectory "$temppath" -ArgumentList "/SILENT","/NORESTART","/NOCANCEL","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/NoIcons=0","/SetupType=default","/EditorOption=Nano","/PathOption=Cmd","/SSHOption=OpenSSH","/TortoiseOption=false","/CURLOption=OpenSSL","/CRLFOption=CRLFCommitAsIs","/BashTerminalOption=MinTTY","/PerformanceTweaksFSCache=Enabled","/UseCredentialManager=Enabled","/EnableSymlinks=Disabled","/EnableBuiltinInteractiveAdd=Disabled","/COMPONENTS=`"icons,ext,ext\shellhere,ext\guihere,gitlfs,assoc,assoc_sh`"" }

	    #oldSystemPath = [System.Environment]::GetEnvironmentVariable('PATH','machine')
        #newSystemPath = oldSystemPath
        #[System.Environment]::SetEnvironmentVariable('PATH', 'bar',[System.EnvironmentVariableTarget]::Machine)
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
	    git update-git-for-windows

	    #add wget into Git 
	    $file = "wget.exe"
	    $folder = (Get-Item "Env:ProgramFiles").Value + "\Git\mingw64\bin"
	    if (Test-Path $folder) { if (!("$folder\$file" | Test-Path)) { curl https://eternallybored.org/misc/wget/1.20.3/64/wget.exe -OutFile "$folder\$file" } }
    }
	








	#install python
	Write-Host "check Python---------------------" -foregroundcolor "white"
	#$windows_path = $env:Path -split ';'
    #if ($windows_path -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on $env:Path' -foregroundcolor "red";Read-Host "will add it to path now" -foregroundcolor "red"}
	#if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
    #$folder = "C:\Python37\"
	#if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
    
    # redirect stderr into stdout
	$p = &{python -V} 2>&1
	$pythonexception = 0
	$pythonversion = "3.7.5"
    # check if an ErrorRecord was returned
    $version = if($p -is [System.Management.Automation.ErrorRecord]){
        Trace-Command -Name CommandDiscovery -Expression {get-command python} -PSHost
        # grab the version string from the error message
		#$p.Exception.Message
		$pythonexception = 1
		Write-Host "python version exception: $p.Exception.Message" -foregroundcolor "red"
    } else {
        # otherwise return as is
		#$p
		Write-Host "python version: $p" -foregroundcolor "yellow"
		$pythonversion = Out-String -InputObject $p
		Write-Host "python version: $pythonversion" -foregroundcolor "yellow"
		$pythonversion = $pythonversion.Replace("Python","")
		Write-Host "python version: $pythonversion" -foregroundcolor "yellow"
		$pythonversion = $pythonversion.Trim()
		Write-Host "python version: $pythonversion" -foregroundcolor "yellow"
	}
	
	
	#[System.Version]"2.7.0.19530" -gt [System.Version]"3.0.0.4080"		False
	#[System.Version]"2.7.0.19530" -lt  [System.Version]"3.0.0.4080"	True
    if (($version -like '*is not recognized*') -or ($pythonexception -eq 1) -or ([System.Version]$pythonversion -lt [System.Version]"3.7.6")){
		Write-Host "$version" -foregroundcolor "yellow"
		$pythonurl37_file = get-FileFromUri $pythonurl37 $temppath
		Write-Host "install $pythonurl37_file now" -foregroundcolor "yellow"
	    #$pythonfile = "python-3.7.5-amd64.exe"

		#if (!("$temppath\$pythonurl37_file" | Test-Path)) { curl https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe -OutFile "$temppath\$pythonurl37_file" }
		if (!("$temppath\$pythonurl37_file" | Test-Path)) { curl "$pythonurl37" -OutFile "$temppath\$pythonurl37_file" }

	    if (Test-Path "$temppath\$pythonurl37_file") { 
			Start-Process -Wait -FilePath "$temppath\$pythonurl37_file" -WorkingDirectory "$temppath" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python37","PrependPath=1" 
			read-host "python installed?"
			if (!("C:\Python37\python.exe" | Test-Path)){
				Write-Host "missing C:\Python37\python.exe" -foregroundcolor "red"
				read-host "?"
			}else{
                $folder = "C:\Python37\Scripts\"
                #--------------------------maschine
                $focused_path = [System.Environment]::GetEnvironmentVariable('PATH','machine')
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on [System.Environment]::GetEnvironmentVariable("PATH","machine") ,will add it to path now' -foregroundcolor "red";
                $focused_path = $folder + ";" + $focused_path
                [System.Environment]::SetEnvironmentVariable('PATH',$focused_path,[System.EnvironmentVariableTarget]::Machine)}
                #--------------------------user
                $focused_path = [System.Environment]::GetEnvironmentVariable('PATH','user')
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on [System.Environment]::GetEnvironmentVariable("PATH","user") ,will add it to path now' -foregroundcolor "red";
                $focused_path = $folder + ";" + $focused_path
                [System.Environment]::SetEnvironmentVariable('PATH',$focused_path,[System.EnvironmentVariableTarget]::User)}
                #--------------------------process
                $focused_path = [System.Environment]::GetEnvironmentVariable('PATH','process')
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on [System.Environment]::GetEnvironmentVariable("PATH","process") ,will add it to path now' -foregroundcolor "red";
                $focused_path = $folder + ";" + $focused_path
                [System.Environment]::SetEnvironmentVariable('PATH',$focused_path,[System.EnvironmentVariableTarget]::Process)}
                #--------------------------session
                $focused_path = $env:Path -split ';'
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on $env:Path' -foregroundcolor "red";Read-Host "will add it to path now" -foregroundcolor "red";
                $env:path = $folder + ";" + $focused_path}

                $folder = "C:\Python37\"
                #--------------------------maschine
                $focused_path = [System.Environment]::GetEnvironmentVariable('PATH','machine')
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on [System.Environment]::GetEnvironmentVariable("PATH","machine")' -foregroundcolor "red";
                $focused_path = $folder + ";" + $focused_path
                [System.Environment]::SetEnvironmentVariable('PATH',$focused_path,[System.EnvironmentVariableTarget]::Machine)}
                #--------------------------user
                $focused_path = [System.Environment]::GetEnvironmentVariable('PATH','user')
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on [System.Environment]::GetEnvironmentVariable("PATH","user")' -foregroundcolor "red";
                $focused_path = $folder + ";" + $focused_path
                [System.Environment]::SetEnvironmentVariable('PATH',$focused_path,[System.EnvironmentVariableTarget]::User)}
                #--------------------------process
                $focused_path = [System.Environment]::GetEnvironmentVariable('PATH','process')
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on [System.Environment]::GetEnvironmentVariable("PATH","process")' -foregroundcolor "red";
                $focused_path = $folder + ";" + $focused_path
                [System.Environment]::SetEnvironmentVariable('PATH',$focused_path,[System.EnvironmentVariableTarget]::Process)}
                #--------------------------session
                $focused_path = $env:Path -split ';'
                $focused_path_splited = $focused_path -split ';'
                if ($focused_path_splited -notcontains $folder) { Write-Host 'missing C:\Python37\Scripts\ on $env:Path' -foregroundcolor "red";
                $env:path = $folder + ";" + $focused_path}
            }
		}else{
			Write-Host "$temppath\$file not found" -foregroundcolor "red"
		}
	} else {
		Write-Host "Python is installed as: $version" -foregroundcolor "green"
	}

	$p = &{python -V} 2>&1
    $version = if($p -is [System.Management.Automation.ErrorRecord]){
        Trace-Command -Name CommandDiscovery -Expression {get-command python} -PSHost
        $p.Exception.Message
    } else {
        $p
    }
	if ($version -like '*Python 3.7*'){
		$windows_path = $env:Path -split ';'
		$folder = "C:\Python37\Scripts\"
		if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
		$folder = "C:\Python37\"
		if ($windows_path -notcontains $folder) { if (Test-Path $folder) { $env:path += ";" + $folder } }
	}
	Write-Host "check Python Modules---------------------" -foregroundcolor "white"
	$errorcode = $null
	$errorcode = python -m pip install --upgrade pip --timeout=3 --retries=1
	if ($errorcode -like '*Requirement already up-to-date:*'){
		Write-Host "Python pip already up-to-date" -foregroundcolor "green"
	} elseif ($errorcode -like '*Successfully installed*'){
		Write-Host "Python pip successfully installed" -foregroundcolor "green"
	} else {
		Write-Host $errorcode -foregroundcolor "red"
	}
	#WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectTimeoutError(<pip._vendor.urllib3.connection.VerifiedHTTPSConnection object at 0x000001DDE3735088>, 'Connection to pypi.org timed out. (connect timeout=3.0)')': /simple/pip/
	python -m pip install --upgrade pip $myPipProxy
	python -m pip install --upgrade setuptools $myPipProxy
	python -m pip install --upgrade wheel $myPipProxy

    #if maybe other python is needed as well, uncomment this:
    #$file = "python-2.7.17.amd64.msi"
	#if (!("$temppath\$file" | Test-Path)) { curl https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi -OutFile "$temppath\$file" }
	#if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i python-2.7.17.amd64.msi","/passive","/norestart" }

	#$file = "python-3.8.0-amd64.exe"
	#if (!("$temppath\$file" | Test-Path)) { curl https://www.python.org/ftp/python/3.8.2/python-3.8.2-amd64.exe -OutFile "$temppath\$file" }
	#if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/passive","InstallAllUsers=1","TargetDir=C:\Python38" }















	#install mongodb-compass
	Write-Host "check MongoDB Compass---------------------" -foregroundcolor "white"
    if (($setuptype -eq "contributor") -or ($setuptype -eq "server")){
        if (!("C:\Program Files\MongoDB Compass Community\MongoDBCompassCommunity.exe" | Test-Path)) {
	        $file = "mongodb-compass-community-1.19.12-win32-x64.msi"
	        if (!("$temppath\$file" | Test-Path)) { curl https://downloads.mongodb.com/compass/mongodb-compass-community-1.19.12-win32-x64.msi -OutFile "$temppath\$file" }
	        #developer gets a mongodb-compass as application, which is able to edit mongodb completely
	        if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi" }
	    }
    }
    if ($setuptype -eq "expert"){
        if (!("C:\Program Files\MongoDB Compass Readonly\MongoDBCompassReadonly.exe" | Test-Path)) {
            $file = "mongodb-compass-readonly-1.19.12-win32-x64.msi"
	        if (!("$temppath\$file" | Test-Path)) { curl https://downloads.mongodb.com/compass/mongodb-compass-readonly-1.19.12-win32-x64.msi -OutFile "$temppath\$file" }
	        #developer gets a mongodb-compass as application, which is able to edit mongodb completely
	        if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-compass-community-1.19.12-win32-x64.msi" }
        }
    }

    #install mongodb
	Write-Host "check MongoDB---------------------" -foregroundcolor "white"
    if (!("C:\Program Files\MongoDB\Server\4.2\bin\mongod.exe" | Test-Path)) {
	    if (!("C:\MongoDB\data" | Test-Path)) { md -p "C:\MongoDB\data" }
	    if (!("C:\MongoDB\log" | Test-Path)) { md -p "C:\MongoDB\log" }
	    $file = "mongodb-win32-x86_64-2012plus-4.2.1-signed.msi"
	    if (!("$temppath\$file" | Test-Path)) { curl https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi -OutFile "$temppath\$file" }
	    #developer gets a mongodb as application (not as service), which have to be startet with a shortcut on the desktop
	    if ($setuptype -eq "contributor"){
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
				$Shortcut.Save()
			}
		}
		#server gets a mongodb as service, which runs from startup
		if ($setuptype -eq "server"){
			if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`"" }
			#if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"all`"" }
		}
		#expert gets a mongodb as service, not to care about configuring
		if ($setuptype -eq "expert"){
			if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"ServerService,Router,Client,MonitoringTools,ImportExportTools,MiscellaneousTools`"" }
			#if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "msiexec.exe" -WorkingDirectory "$temppath" -ArgumentList "/l*v mdbinstall.log","/qb","/i mongodb-win32-x86_64-2012plus-4.2.1-signed.msi","ADDLOCAL=`"all`"" }
		}
	}

	#developer, expert and server gets an allround editor, if possible the new 7.8.1, or at minimum the 7.7.1
	Write-Host "check Notepad++ ---------------------" -foregroundcolor "white"
    if (($setuptype -eq "contributor") -or ($setuptype -eq "server") -or ($setuptype -eq "expert")){
        if (!('C:\Program Files\Notepad++\notepad++.exe' | Test-Path)) {
	        $file = "npp.7.7.1.Installer.x64.exe"
	        if (!("$temppath\$file" | Test-Path)) { curl https://notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe -OutFile "$temppath\$file" }
	        if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/S" }
	        $file = "npp.7.8.1.Installer.x64.exe"
	        if (!("$temppath\$file" | Test-Path)) { curl http://download.notepad-plus-plus.org/repository/7.x/7.8.1/npp.7.8.1.Installer.x64.exe -OutFile "$temppath\$file" }
	        if (Test-Path "$temppath\$file") { Start-Process -Wait -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "/S" }
        }
    }

	#developer gets minimum c++ 14.0 for levenshtein and complete ide for python and django webdeployment
	Write-Host "check c++ 14.0 (via Visual Studion BuildTools)---------------------" -foregroundcolor "white"
    Install-Module VSSetup -Scope AllUsers
    Update-Module VSSetup
    Import-Module VSSetup

	#$vsconfig_vs_buildtools_2019 = 	"`"--add Microsoft.VisualStudio.Workload.MSBuildTools`",`"--add Microsoft.VisualStudio.Workload.VCTools`",`"--add Microsoft.Component.MSBuild`",`"--add Microsoft.VisualStudio.Component.Roslyn.Compiler`",`"--add Microsoft.VisualStudio.Component.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.Windows10SDK`",`"--add Microsoft.VisualStudio.Component.VC.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64`",`"--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest`",`"--add Microsoft.VisualStudio.Component.Windows10SDK.18362`",`"--add Microsoft.VisualStudio.Component.VC.CMake.Project`",`"--add Microsoft.VisualStudio.Component.TestTools.BuildTools`",`"--add Microsoft.VisualStudio.Component.WebDeploy`""
	#$vsconfig_vs_buildtools_2019 = 	"`"--add Microsoft.VisualStudio.Workload.MSBuildTools`""
	#$vsconfig_vs_buildtools_2019_splited = $vsconfig_vs_buildtools_2019 -split ','
	#echo $vsconfig_vs_buildtools_2019_splited
	#$vsconfig_vs_buildtools_2019 = "--quiet --wait --update"
	$vsconfig_vs_buildtools_2019 = "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.MSBuildTools --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.Component.MSBuild --add Microsoft.VisualStudio.Component.Roslyn.Compiler --add Microsoft.VisualStudio.Component.CoreBuildTools --add Microsoft.VisualStudio.Component.Windows10SDK --add Microsoft.VisualStudio.Component.VC.CoreBuildTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.VC.Redist.14.Latest --add Microsoft.VisualStudio.Component.Windows10SDK.18362 --add Microsoft.VisualStudio.Component.VC.CMake.Project --add Microsoft.VisualStudio.Component.TestTools.BuildTools --add Microsoft.VisualStudio.Component.WebDeploy"
	#$vsconfig_vs_enterprise_2019 = "`"--add Microsoft.VisualStudio.Workload.CoreEditor`",`"--add Microsoft.VisualStudio.Workload.VCTools`",`"--add Microsoft.VisualStudio.Workload.Python`",`"--add Microsoft.VisualStudio.Workload.NativeDesktop`",`"--add Microsoft.Component.MSBuild`",`"--add Microsoft.Component.PythonTools`",`"--add Microsoft.Component.PythonTools.Web`",`"--add Microsoft.VisualStudio.Component.Roslyn.Compiler`",`"--add Microsoft.VisualStudio.Component.CoreEditor`",`"--add Microsoft.VisualStudio.Component.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.Windows10SDK`",`"--add Microsoft.VisualStudio.Component.VC.CoreBuildTools`",`"--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64`",`"--add Microsoft.VisualStudio.Component.VC.Redist.14.Latest`",`"--add Microsoft.VisualStudio.Component.Windows10SDK.18362`",`"--add Microsoft.VisualStudio.Component.VC.CMake.Project`",`"--add Microsoft.VisualStudio.Component.VC.CoreIde`",`"--add Microsoft.VisualStudio.Component.WebDeploy`""
	$vsconfig_vs_enterprise_2019 = "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.CoreEditor --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Workload.Python --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.Component.MSBuild --add Microsoft.Component.PythonTools --add Microsoft.Component.PythonTools.Web --add Microsoft.VisualStudio.Component.Roslyn.Compiler --add Microsoft.VisualStudio.Component.CoreEditor --add Microsoft.VisualStudio.Component.CoreBuildTools --add Microsoft.VisualStudio.Component.Windows10SDK --add Microsoft.VisualStudio.Component.VC.CoreBuildTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.VC.Redist.14.Latest --add Microsoft.VisualStudio.Component.Windows10SDK.18362 --add Microsoft.VisualStudio.Component.VC.CMake.Project --add Microsoft.VisualStudio.Component.VC.CoreIde --add Microsoft.VisualStudio.Component.WebDeploy"
	
	$file = "vs_buildtools.exe"
    #https://aka.ms/vs/16/release/vs_buildtools.exe
    if (!("$temppath\$file" | Test-Path)) { curl "https://aka.ms/vs/16/release/$file" -OutFile "$temppath\$file" }
	#if (!("$temppath\$file" | Test-Path)) { curl "https://$gitserver/$gituser/RdA/raw/master/PSRdA/vs/$file" -OutFile "$temppath\$file" }
	if (Test-Path "$temppath\$file") { 
		#echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--update`",`"--passive`",`"--wait`" -Wait -PassThru;"

        #Install-Module MSI -Scope AllUsers
		#Get-MSIRelatedProductInfo '{1571205C-BAD1-4237-BFE6-B77E622C51DB}'
        #Get-MSIRelatedProductInfo '{1571205C-BAD1-4237-BFE6-B77E622C51DB}' | Repair-MSIProduct
        #read-host "Repair 1 would be done"

		Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList $vsconfig_vs_buildtools_2019 -Wait -PassThru
		$errorcode = $null
		$errorcode = python -m pip install --upgrade python-bsonjs --timeout=3 --retries=1
		if (($errorcode -like "*Successfully installed*") -or ($errorcode -like "*Requirement already up-to-date*")) { Write-Host "Visual Studio install minimum c++ 14.0 for levenshtein and bsonjs seems ready" -foregroundcolor "green" }
		elseif (($errorcode -like "*Command errored out with exit status 1*") -or ($errorcode -like "*failed with exit status 2*")) { echo $errorcode; read-host "Visual Studio install minimum c++ 14.0 for levenshtein and bsonjs seems failed."; }
		else { echo $errorcode; read-host "something else happend?"; }

        Get-VSSetupInstance -All -Prerelease

		$errorcode = $null
		$errorcode = python -m pip install --upgrade pyxdameraulevenshtein --timeout=3 --retries=1
		if (($errorcode -like '*Requirement already up-to-date:*') -or ($errorcode -like '*Requirement already up-to-date*')){
			Write-Host "Python pyxdameraulevenshtein already up-to-date" -foregroundcolor "green"
		} elseif ($errorcode -like '*error: Microsoft Visual C++ 14.0 is required.*'){
			Write-Host $errorcode -foregroundcolor "red"
		} else {
			Write-Host $errorcode -foregroundcolor "black"
			read-host "python -m pip install --upgrade pyxdameraulevenshtein --timeout=3 --retries=1"
		}
		$errorcode = $null
		$errorcode = python -m pip install --upgrade python-bsonjs --timeout=3 --retries=1
		if (($errorcode -like '*Requirement already up-to-date:*') -or ($errorcode -like '*Requirement already up-to-date*')){
			Write-Host "Python python-bsonjs already up-to-date" -foregroundcolor "green"
		} elseif ($errorcode -like '*error: Microsoft Visual C++ 14.0 is required.*'){
			Write-Host $errorcode -foregroundcolor "red"
		} else {
			Write-Host $errorcode -foregroundcolor "black"
			read-host "python -m pip install --upgrade python-bsonjs --timeout=3 --retries=1"
		}

		if (!(Get-VSSetupInstance -All -Prerelease | Select-VSSetupInstance -Product * -Require 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64')){
		    read-host "Installation of Visual Studio failed. You can try it manually with the command between the last two yellow lines...";
            return;
            }
	}

	
    if ($setuptype -eq "contributor"){
		Write-Host "check Visual Studio IDE (via Visual Studion Enterprise)---------------------" -foregroundcolor "white"
	    $file = "vs_enterprise.exe"
	    #https://aka.ms/vs/16/release/vs_Enterprise.exe
	    if (!("$temppath\$file" | Test-Path)) { curl "https://aka.ms/vs/16/release/$file" -OutFile "$temppath\$file" }
	    #if (!("$temppath\$file" | Test-Path)) { curl "https://$gitserver/$gituser/RdA/raw/master/PSRdA/vs/$file" -OutFile "$temppath\$file" }
	    if (Test-Path "$temppath\$file") { 
		    #echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--update`",`"--passive`",`"--wait`" -Wait -PassThru;"
		    #Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--update","--passive","--wait" -Wait -PassThru;
		    #read-host "To continue after update";
		    #Write-Host -ForegroundColor Blue "--------------------------------------------------------------"
		    #echo "Start-Process -FilePath `"$temppath\$file`" -WorkingDirectory `"$temppath`" -ArgumentList `"--passive`",`"--wait`",$vsconfig_vs_enterprise_2019 -Wait -PassThru;"
		    #Write-Host -ForegroundColor Blue "--------------------------------------------------------------"
		    #Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList "--passive","--wait",$vsconfig_vs_enterprise_2019 -Wait -PassThru;
			Start-Process -FilePath "$temppath\$file" -WorkingDirectory "$temppath" -ArgumentList $vsconfig_vs_enterprise_2019 -Wait -PassThru
		    if (!(Get-VSSetupInstance -All -Prerelease | Select-VSSetupInstance -Product * -Require 'Microsoft.VisualStudio.Component.VC.Tools.x86.x64')){
		        read-host "Installation of Visual Studio failed. You can try it manually with the command between the last two blue lines...";
                return;
            }
		}
    }

	#rem in case missing ...error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools", repeat:
	#python -m pip install --upgrade python-bsonjs
	#python -m pip install --upgrade pyxdameraulevenshtein
	#https://asawicki.info/news_1597_installing_visual_c_redistributable_package_from_command_line.html
	#https://docs.microsoft.com/de-de/visualstudio/releases/2019/system-requirements
	#https://docs.microsoft.com/en-us/visualstudio/install/build-tools-container?view=vs-2017
}

Write-Host "check PowerShell Git---------------------" -foregroundcolor "white"
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

#Get-Item "Env:"
#get-childitem -path env:* | get-member
if (Test-Path $($(Get-Item "Env:USERPROFILE").Value)) { echo "found: $($(Get-Item "Env:USERPROFILE").Value)" }
if (Test-Path $($(Get-Item "Env:USERPROFILE").Value + "\source")) { echo "found: $($(Get-Item "Env:USERPROFILE").Value + "\source")" }
#get git CdA
Write-Host "check CdA sources---------------------" -foregroundcolor "white"
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

Write-Host "check usebility (via desktop shortcuts)---------------------" -foregroundcolor "white"
if ($setuptype -eq "contributor"){
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
}

Write-Host "check Run---------------------" -foregroundcolor "white"
if (($setuptype -eq "contributor") -or ($setuptype -eq "expert")){
	$file = "PyCdA.py"
	if (Test-Path "$folder\$project\$file") { 
		cd "$folder\$project"
		#python "$folder\$project\$file"
		Invoke-Expression "& { $(python "$folder\$project\$file") }"
		#python $home\source\repos\github.com\kaestnja\CdA\PyCdA.py
		#Invoke-Expression "& { $(python "$home\source\repos\github.com\kaestnja\CdA\PyCdA.py") }"
	}
}
if (($setuptype -eq "contributor") -or ($setuptype -eq "expert") -or ($setuptype -eq "server")){
	$file = "PyCdA.py"
	#find all home paths:  dir env:\home*
	$WshShell = New-Object -comObject WScript.Shell
	$desktopfolder = (Get-Item "Env:USERPROFILE").Value + "\Desktop"
	if (!($desktopfolder | Test-Path)) { $desktopfolder = (Get-Item "Env:Home").Value + "\Desktop" }
	if (!($desktopfolder | Test-Path)) { $desktopfolder = (Get-Item "Env:USERPROFILE").Value + "\Desktop" }
	if (!($desktopfolder | Test-Path)) { $desktopfolder = (Get-Item "Env:OneDrive").Value + "\Desktop" }
	if (Test-Path $desktopfolder) { 
		$Shortcut = $WshShell.CreateShortcut("$desktopfolder\PyCdA.lnk") 
		$Shortcut.TargetPath = "C:\Python37\python.exe"
		$Shortcut.Arguments = "$folder\$project\$file"
		$Shortcut.Description = "start PyCdA"
		#$Shortcut.IconLocation = "$folder\$project\cda.ico, 1"
		$Shortcut.WindowStyle = "1"
		$Shortcut.WorkingDirectory = "$folder\$project"
		$Shortcut.Save()
	}
}
cd "${env:Userprofile}"