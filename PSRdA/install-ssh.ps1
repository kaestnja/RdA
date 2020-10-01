#https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_install_firstuse
#https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_server_configuration
#https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_keymanagement

Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'

# Install the OpenSSH Client
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Install the OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

Start-Service sshd
# OPTIONAL but recommended:
Set-Service -Name sshd -StartupType 'Automatic'
# Confirm the Firewall rule is configured. It should be created automatically by setup.
Get-NetFirewallRule -Name *ssh*
# There should be a firewall rule named "OpenSSH-Server-In-TCP", which should be enabled
# If the firewall does not exist, create one
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22

# Standardshell auf PowerShell.exe
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force


# test
#Ssh username@servername

# Uninstall the OpenSSH Client
#Remove-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0

# Uninstall the OpenSSH Server
#Remove-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0