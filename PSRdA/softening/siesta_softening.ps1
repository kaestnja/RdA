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
    Default {$PublishSettings=$false} 
} 

if($PublishSettings) {

    $revert_file = "revert_siesta_softening_"+([datetime]::UtcNow).tostring("yyyy-MM-dd_HH-mm-ss")+".ps1"

    if (Test-Path $revert_file) {
        Remove-Item -Path $revert_file -Force
    }

    # Disable UAC
    #"Disabling User Account Control ..."
    #$reg_uac = (Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).EnableLUA
    #if ($reg_uac -match "1") {
    #    "reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d $reg_uac /f" | Out-File $revert_file -Append
    #    reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 0 /f
    #}

    #Enable LocalAccountTokenFilterPolicy"
    "Enabling LocalAccountTokenFilterPolicy ..."
    if (Get-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\system' -Name LocalAccountTokenFilterPolicy -ErrorAction SilentlyContinue) {
        $reg_LocalAccountTokenFilterPolicy = (Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Policies\system).LocalAccountTokenFilterPolicy
        if ($reg_LocalAccountTokenFilterPolicy -match "0") {
            "reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d $reg_LocalAccountTokenFilterPolicy /f" | Out-File $revert_file -Append
            reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
        }
    } else {
        "reg.exe DELETE HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /f" | Out-File $revert_file -Append
        reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f
    }

    # PowerShell Script Execution
    "Enabling PowerShell Script Execution ..."
    if (Test-Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\") {
        $reg_enablescripts = (Get-ItemProperty HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell).EnableScripts
        if ($reg_enablescripts -match "0") {
            "reg.exe ADD HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell /v EnableScripts /t REG_DWORD /d $reg_enablescripts /f" | Out-File $revert_file -Append
            reg.exe ADD HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell /v EnableScripts /t REG_DWORD /d 1 /f
        }
    } else {
        "reg.exe DELETE HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell /f" | Out-File $revert_file -Append
        reg.exe ADD HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell
    }

    "Set PowerShell ExecutionPolicy ..."
    if (Get-ItemProperty -Path 'HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell' -Name ExecutionPolicy -ErrorAction SilentlyContinue) {
        $reg_executionpolicy = (Get-ItemProperty HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell).ExecutionPolicy
        if ($reg_executionpolicy -match "RemoteSigned") {
            "PowerShell ExecutionPolicy OK"
        } else {
            "reg.exe ADD HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell /v ExecutionPolicy /t REG_DWORD /d $reg_executionpolicy /f" | Out-File $revert_file -Append
            reg.exe ADD HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell /v ExecutionPolicy /t REG_SZ /d "RemoteSigned" /f
        }
    } else {
        $reg_executionpolicy = Get-ExecutionPolicy
        if ($reg_executionpolicy -match "RemoteSigned") {
            "PowerShell ExecutionPolicy OK"
        } else {
            "Set-ExecutionPolicy -ExecutionPolicy $reg_executionpolicy -Force" | Out-File $revert_file -Append
            Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Force
        }
    }


    # Enable admin share
    "Enabling Admin Share ..."
    if (Test-Path "filesystem::\\localhost\C$") {
        "Admin share already enabled"
    } else {        
        $reg_autoshareserver = (Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters).AutoShareServer
        if ($reg_autoshareserver -match "0") {
            "reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v AutoShareServer /t REG_DWORD /d $reg_autoshareserver /f" | Out-File $revert_file -Append
            reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v AutoShareServer /t REG_DWORD /d 1 /f
        }
        $reg_autosharewks = (Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters).AutoShareWks
        if ($reg_autosharewks -match "0") {
            "reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v AutoShareWks /t REG_DWORD /d $reg_autosharewks /f" | Out-File $revert_file -Append
            reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v AutoShareWks /t REG_DWORD /d 1 /f
        }
        "cmd.exe /c 'net share C$ /delete'" | Out-File $revert_file -Append
        cmd.exe /c $( "net share C$=C:\ /GRANT:""$(Get-GroupName -SID 'S-1-1-0')"",FULL" )
    }

    # Allow unencrypted SMB sessions
    "Allowing unencrypted SMB sessions ..."
    $reg_RejectUnencryptedAccess = (Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters).RejectUnencryptedAccess
    if ($reg_RejectUnencryptedAccess -match "1") {
        "reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v RejectUnencryptedAccess /t REG_DWORD /d $reg_RejectUnencryptedAccess /f" | Out-File $revert_file -Append
        reg.exe ADD HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters /v RejectUnencryptedAccess /t REG_DWORD /d 1 /f
    }

    # Activate remote registry
    "Activating Remote Registry service ..."
    if (Get-Service remoteregistry -ErrorAction SilentlyContinue) {
        $starttype_remoteregistry = (Get-WmiObject Win32_Service -Filter "Name='remoteregistry'").StartMode
        if ($starttype_remoteregistry -match "Disabled") {
            "Set-Service remoteregistry -startuptype $starttype_remoteregistry" | Out-File $revert_file -Append
            Set-Service remoteregistry -startuptype "manual"
        }
    } else {
        "Service remoteregistry does not exist ..."
    }

    # Activate lanmanserver (Server)
    "Activating and starting lanmanserver service ..."
    if (Get-Service lanmanserver -ErrorAction SilentlyContinue) {
        $starttype_lanmanserver = (Get-WmiObject Win32_Service -Filter "Name='lanmanserver'").StartMode
        if ($starttype_lanmanserver -match "Disabled") {
            "Set-Service lanmanserver -startuptype $starttype_lanmanserver" | Out-File $revert_file -Append
            Set-Service lanmanserver -startuptype "Automatic"
        }
        $status_lanmanserver = (Get-Service 'lanmanserver').Status
        if ($status_lanmanserver -match "Stopped") {
            "Stop-Service lanmanserver" | Out-File $revert_file -Append
            Start-Service -Name lanmanserver
        }
    } else {
        "Service lanmanserver does not exist ..."
    }

    # Activate wuauserv (Windows Update)
    "Activating and starting wuauserv service ..."
    if (Get-Service wuauserv -ErrorAction SilentlyContinue) {
        $starttype_wuauserv = (Get-WmiObject Win32_Service -Filter "Name='wuauserv'").StartMode
        if ($starttype_wuauserv -match "Disabled") {
            "Set-Service wuauserv -startuptype $starttype_wuauserv" | Out-File $revert_file -Append
            Set-Service wuauserv -startuptype "Automatic"
        }
        $status_wuauserv = (Get-Service 'wuauserv').Status
        if ($status_wuauserv -match "Stopped") {
            "Stop-Service wuauserv" | Out-File $revert_file -Append
            Start-Service -Name wuauserv
        }
    } else {
        "Service wuauserv does not exist ..."
    }
    
    # Deactivate AppIDSvc (required for AppLocker)
    "Deactivating and stopping AppIDSvc service (AppLocker) ..."
    # Set-Service AppIDSvc -startuptype "Disabled" # Not possible anymore with Windows 10 (protected process)
    if (Get-Service AppIDSvc -ErrorAction SilentlyContinue) {
        #$starttype_appidsvc = (Get-WmiObject Win32_Service -Filter "Name='AppIDSvc'").StartMode
        $status_appidsvc = (Get-Service 'AppIDSvc').Status
        if ($status_appidsvc -match "Running") {
            "Start-Service AppIDSvc" | Out-File $revert_file -Append
            Stop-Service -Name AppIDSvc
        }
    } else {
        "Service AppIDSvc does not exist ..."
    }

    # Open Port 445
    "Opening port 445..."
    $rules = netsh advfirewall firewall show rule status=enabled name=all | select-string -pattern "(LocalPort.*445)" -Context 9,4
    if ("$rules".Contains("Block")) {
        "Warning: Blocking rule enabled for Port 445"
    }
    "& netsh advfirewall firewall delete rule name='SiESTA SMB'" | Out-File $revert_file -Append
    & netsh advfirewall firewall add rule name="SiESTA SMB" dir=in action=allow enable=yes localport=445 protocol=tcp

    ""
    "Created file '$revert_file' to revert all settings made..."
    ""
}
else
{
    "Exiting..."
    exit
}