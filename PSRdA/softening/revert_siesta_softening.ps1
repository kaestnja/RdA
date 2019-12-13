# Enable UAC
"Enabling User Account Control ..."
reg.exe ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 1 /f

# Deactivate remote registry
"Stopping Remote Registry service ..."
Stop-Service -Name remoteregistry

# Disable admin share
"Disabling Admin Share ..."
cmd.exe /c "net share C$ /delete"

# Close Port 445
"Deleting SiESTA firewall rule ..."
& netsh advfirewall firewall delete rule name="SiESTA SMB"

"Please reboot the system to apply all changes"
