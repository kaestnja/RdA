Get-Host | Select-Object Version
Get-PSRepository
#repair default:
#Register-PSRepository -Default -InstallationPolicy Trusted
Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted
Update-Module
#Register-PSRepository -Name "myNuGetSource" -SourceLocation "https://www.myget.org/F/powershellgetdemo/api/v2" -PublishLocation "https://www.myget.org/F/powershellgetdemo/api/v2/Packages" -InstallationPolicy Trusted
#https://github.com/nightroman/Mdbc
#https://dev.to/tunaxor/powershell--mongo-34om
#Install-Module Mdbc

#https://winaero.com/blog/run-as-administrator-context-menu-for-power-shell-ps1-files/
