# PS C:\Windows\system32> Get-ExecutionPolicy 
# Restricted
# PS C:\Windows\system32> Get-ExecutionPolicy -Scope CurrentUser
# Undefined
# PS C:\Windows\system32> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
# PS C:\Windows\system32> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# PS C:\Windows\system32> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
# PS C:\Windows\system32> Set-ExecutionPolicy Undefined -Scope CurrentUser
# PowerShell.exe -ExecutionPolicy AllSigned

# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

# Export-WindowsDriver -Online -Destination C:\Temp\DriverBackup
Export-WindowsDriver -Destination "C:\Temp\Drivers\$((Get-WmiObject -Class win32_computersystem).Model)" -Online

Export-StartLayout -Path C:\Temp\customstartlayout.xml

# https://docs.microsoft.com/de-de/powershell/scripting/setup/installing-powershell-core-on-windows?view=powershell-6
# $env:ProgramFiles\PowerShell\<version>\pwsh.exe




New-PSSession -ComputerName <deviceIp> -Credential Administrator
# change the destination to however you had partitioned it with sufficient
# space for the zip and the unzipped contents
# the path should be local to the device
Copy-Item .\PowerShell-6.1.0-win-arm32.zip -Destination u:\users\administrator\Downloads -ToSession $s

Enter-PSSession $s
Set-Location u:\users\administrator\downloads
Expand-Archive .\PowerShell-6.1.0-win-arm32.zip

Set-Location .\PowerShell-6.1.0-win-arm32
# Be sure to use the -PowerShellHome parameter otherwise it'll try to create a new
# endpoint with Windows PowerShell 5.1
.\Install-PowerShellRemoting.ps1 -PowerShellHome .
# You'll get an error message and will be disconnected from the device because it has to restart WinRM

# Be sure to use the -Configuration parameter.  If you omit it, you will connect to Windows PowerShell 5.1
Enter-PSSession -ComputerName <deviceIp> -Credential Administrator -Configuration powershell.6.1.0