# V6 12:42
# copy this script to C:\Temp\siesta_softening.ps1
# to enable execution of scripts, use this command in administrative powershell console:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
# after that, start the script via C:\Temp\siesta_softening.ps1
# https://bitvijays.github.io/LFF-IPS-P3-Exploitation.html

function Get-GroupName {
    param ($SID)

    $objSID = New-Object System.Security.Principal.SecurityIdentifier($sid)
    $objUser = $objSID.Translate([System.Security.Principal.NTAccount])
    $objUser.Value
}


Write-host "
Please Read!
------------

This script does something like a reverse hardening (softening) to make a Windows system fit for remote interaction with SiESTA.

+---------------------------------------------------------------------+
| After softening, the system is not measure plan compliant any more. |
| We strongly advise to use the script only in protected networks     |
| and harden the system as soon as possible after the tests.          |
+---------------------------------------------------------------------+
"
Write-Host "Are you sure, you want to apply the changes?" -ForegroundColor Yellow 

$Readhost = Read-Host "( yes / no ) "

Switch ($ReadHost) { 
    Yes {$PublishSettings=$true} 
    No {$PublishSettings=$false} 
    Default {$PublishSettings=$true} 
} 
 
if($PublishSettings) {
    # https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/?view=powershell-5.1
    
    # enable Admin Acount
    # Get-LocalUser -Name "Administrator" | Enable-LocalUser
    # Enable-LocalUser -Name "Administrator"
    net user administrator P@ssw0rd /active:yes
    #net user Administrator /active:yes

    # set Password to Administrator
    $ToEncrypted = "P@ssw0rd"
    $Password = ConvertTo-SecureString -AsPlainText $ToEncrypted -Force
    # or
    #$Password = Read-Host "Insert password" -AsSecureString
    ######################### then
    #$UserAccount = Get-LocalUser -Name "Administrator"
    #$UserAccount | Set-LocalUser -Password $Password
    ######################### or
    #Reset-LocalAccountPassword -AdminAccount -Confirm:$false
    #Reset-LocalAccountPassword S35 -AdminAccount -Confirm:$false -Credential (Get-Credential)
    ######################### or
    $cred = New-Object System.Management.Automation.PSCredential("foo", $Password)
    $Admin=[adsi]("WinNT://$env:COMPUTERNAME/Administrator, user")
    $Admin.SetPassword($cred.GetNetworkCredential().Password)

    #$User = "Domain01\User01"
    #$User = "$env:COMPUTERNAME/Administrator"
    #$c = Get-Credential
    #Get-WmiObject Win32_DiskDrive -ComputerName S35 -Credential $cred
    #Get-WmiObject Win32_BIOS -ComputerName S35 -Credential (Get-Credential -Credential S35\Administrator)
    #Get-WmiObject Win32_BIOS -ComputerName S35 -Credential (Get-Credential -Credential $Admin)
    
    # Disable UAC
    "Disabling User Account Control ..."
    reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f

    # Disable Simple FileSharing
    "Disabling Simple FileSharing ..."
    reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Control\Lsa /v forceguest /t REG_DWORD /d 0 /f

    # Allow Admin Shares
    "Allow Admin Shares ..."
    net stop srvnet /y
    reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v AutoShareServer /t REG_DWORD /d 1 /f
    reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v AutoShareWks /t REG_DWORD /d 1 /f
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB1 -Type DWORD -Value 1 –Force
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" SMB2 -Type DWORD -Value 1 –Force
    net start srvnet /y
    net start Server /y
    #Get-WindowsFeature FS-SMB1
    #Enable-WindowsOptionalFeature -Online -FeatureName smb1protocol
    #Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol
    #
    #Get-WindowsOptionalFeature –Online –FeatureName SMB1Protocol 
    #Enable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
    #Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol
    #
    #Get-SmbServerConfiguration | Select EnableSMB1Protocol
    #Set-SmbServerConfiguration -EnableSMB1Protocol $true

    # Allow services to be started as interactive, needed for winexe
    "Allow Interactive Service Start ..."
    reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Control\Windows /v NoInteractiveServices /t REG_DWORD /d 0 /f

    # Activate remote registry
    "Starting Remote Registry service ..."
    # 
    Set-Service -Name RemoteRegistry -StartupType Manual
    Start-Service -Name RemoteRegistry
    Set-Service -Name RemoteRegistry -StartupType Automatic
    Get-Service | Select-Object -Property Name,Status,StartType | where-object {$_.Name -eq "RemoteRegistry"} | Format-Table -auto
    # Get-Service -ComputerName "S35" | Select-Object -Property MachineName,Name,Status,StartType | where-object {$_.Name -eq "RemoteRegistry"} | Format-Table -auto
    if ((Get-Service 'RemoteRegistry').StartType -match "Disabled") {
            Set-Service -Name RemoteRegistry -StartupType Manual
    }
    if ((Get-Service 'RemoteRegistry').Status -match "Stopped") {
            Start-Service -Name RemoteRegistry
    }
    if ((Get-Service 'RemoteRegistry').StartType -match "Manual") {
            Set-Service -Name RemoteRegistry -StartupType Automatic
    }
    # Get Service status
    # $Service = "RemoteRegistry"
    # sc.exe qc $Service
    # sc.exe config $Service start= auto
    # sc.exe start $Service

    Set-WSManQuickConfig -Force
    #Set-Item WSMan:\localhost\Service\Auth\Basic -Value $True
    #Set-Item WSMan:\localhost\Service\AllowUnencrypted -Value $True
    Enable-PSRemoting -Force
    cmd.exe /c $('winrm quickconfig -q & winrm set winrm/config/winrs @{MaxMemoryPerShellMB="2048"} & winrm set winrm/config @{MaxTimeoutms="3000000"} & winrm set winrm/config/client/auth @{Basic="true"} & winrm set winrm/config/service/auth @{Basic="true"} & winrm set winrm/config/service @{AllowUnencrypted="true"} & netsh advfirewall firewall add rule name="WinRM 5985" protocol=TCP dir=in localport=5985 action=allow & net stop winrm & sc config "WinRM" start= auto & net start "WinRM" & winrm create winrm/config/listener?Address=*+Transport=HTTP & net start "Winrm" ')
    #winrm enumerate winrm/config/listener
    #Get-Item WSMan:\localhost\Client\TrustedHosts
    #Set-Item WSMan:\localhost\Client\TrustedHosts -Value *
    #Set-Item WSMan:\localhost\Client\TrustedHosts *.pcs.local
    #Set-Item WSMan:\localhost\Client\TrustedHosts -Concatenate -Value Server02
    #Set-Item WSMan:\localhost\Client\TrustedHosts -Value 10.10.10.1,[0:0:0:0:0:0:0:0]
    #cmd.exe /c $('winrm set winrm/config/client @{TrustedHosts="S35"}')
    #cmd.exe /c $(winrm set winrm/config/client '@{TrustedHosts="S35,S36,S37,S38"}')
    #Enter-PSSession -ComputerName S35
    #or
    #connect-wsman -computername S35
    #set-item wsman:\S35\Client\TrustedHosts -value 192.168.24.34, 192.168.24.35, 192.168.24.36, 192.168.24.37, 192.168.24.38


    # Enable admin share
    # "Enabling Admin Share ..."
    # cmd.exe /c $( "net share ADMIN$=C:\Windows /GRANT:""$(Get-GroupName -SID 'S-1-1-0')"",FULL" )

    # Enable c$ admin share
    "Enabling c$ Admin Share ..."
    cmd.exe /c $( "net share C$=C:\ /GRANT:""$(Get-GroupName -SID 'S-1-1-0')"",FULL" )

    # Open Port 445
    "Opening port 445..."
    $rules = netsh advfirewall firewall show rule status=enabled name=all | select-string -pattern "(LocalPort.*445)" -Context 9,4
    if ("$rules".Contains("Block")) {
        "Warning: Blocking rule enabled for Port 445"
    }
    & netsh advfirewall firewall add rule name="SiESTA SMB" dir=in action=allow enable=yes localport=445 protocol=tcp

    # Open File and Print Sharing
    "Opening File and Print Sharing..."
    #netsh firewall set service type = FILEANDPRINT mode = ENABLE
    #netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=Yes profile=public,private
    netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=Yes
    # netsh firewall set service type = FILEANDPRINT mode = DISABLE

    # net start lanmanserver
    # net share
    #New-SmbShare -Name "Temp" -Path "C:\Temp" -FullAccess ".\Administrator", "PCS\Administrators"
    New-SmbShare -Name "Temp" -Path "C:\Temp" -FullAccess "Administrator"


    # Turn On File & Print Sharing (Domain Network)
    # @FirewallAPI.dll,-28502 = File and Printer Sharing | @FirewallAPI.dll,-32752 = Network Discovery
    #foreach ($Group in ('@FirewallAPI.dll,-28502','@FirewallAPI.dll,-32752')) {
    #    Get-NetFirewallRule | Where-Object { ($_.Group -match $Group) -and ($_.Profile -eq 'any') -and ($_.Enabled -eq 'false') } | ForEach-Object -Process {
    #        Set-NetFirewallRule -InputObject $_ -Profile 'Domain' -Enabled 'true'
    #        Set-NetFirewallRule -InputObject (Copy-NetFirewallRule -InputObject $_ -NewName ('{' + (([GUID]::NewGuid()).Guid).ToUpper() + '}') -PassThru) -Profile 'Public,Private' -Enabled 'false'
    #    }    
    #}
    #Set-NetConnectionProfile -Name 'Network' -NetworkCategory 'Domain'
    #
    # get-module -listavailable
    # import-module activedirectory
    # Import-Module ServerManager
    # Add-WindowsFeature RSAT-AD-PowerShell
    # get-windowsfeature | where name -like RSAT-AD-PowerShell | Install-WindowsFeature
    #Set-SmbShare and Grant-SmbShareAccess
    

    "Please reboot the system to apply all changes"
}
else
{
    "Exiting..."
    exit
}

