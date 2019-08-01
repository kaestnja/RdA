#windows client
Get-WindowsOptionalFeature -Online

#gcm -module DISM #List available commands
#Get-WindowsOptionalFeature -online | ft #List all features and status
#Get-WindowsOptionalFeature -online | Sort-Object -Property FeatureName | Format-Table -GroupBy State -Wrap
#Enable-WindowsOptionalFeature -online -FeatureName NetFx3 -Source e:\Sources\sxs

Add-WindowsFeature IIS-WebServerRole

function InstallFeature($name) {
    # server
    # cmd /c "ocsetup $name /passive"
    # client
    Enable-WindowsOptionalFeature -online -FeatureName $name
}
InstallFeature IIS-WebServerRole
    #InstallFeature IIS-WebServer
        #InstallFeature IIS-CommonHttpFeatures
            #InstallFeature IIS-DefaultDocument
            #InstallFeature IIS-DirectoryBrowsing
            #InstallFeature IIS-HttpErrors
            #InstallFeature IIS-StaticContent
            #InstallFeature IIS-HttpRedirect
            #InstallFeature IIS-WebDAV
        #InstallFeature IIS-HealthAndDiagnostics
            #InstallFeature IIS-HttpLogging
            #InstallFeature IIS-CustomLogging
            #InstallFeature IIS-HttpTracing
            #InstallFeature IIS-LoggingLibraries
        #InstallFeature IIS-Performance
            #IIS-HttpCompressionStatic
        #InstallFeature IIS-Security
            #InstallFeature IIS-RequestFiltering
            #InstallFeature IIS-WindowsAuthentication
        #InstallFeature IIS-ApplicationDevelopment
            InstallFeature IIS-NetFxExtensibility
            InstallFeature IIS-ISAPIExtensions
            InstallFeature IIS-ISAPIFilter
            InstallFeature IIS-ASPNET
            #InstallFeature IIS-WebSockets
            InstallFeature IIS-CGI
    #InstallFeature IIS-WebServerManagementTools 
        #InstallFeature IIS-ManagementConsole 
        InstallFeature IIS-ManagementScriptingTools
        InstallFeature IIS-ManagementService

import-module WebAdministration

Stop-WebAppPool DefaultAppPool

#windows server
#Install-WindowsFeature -name Web-Server -IncludeManagementTools