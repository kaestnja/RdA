Get-Host | Select-Object Version
Get-PSRepository
Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted
Update-Module
