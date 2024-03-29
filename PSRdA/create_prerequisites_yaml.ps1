$prerequisitesyamlbuilding = @"
CdA:
- 1.0.2
Python37:
  recommended:
  - 3.7.5
  minimum:
  - 3.7.4
Python27:
  recommended:
  - 2.7.17
Git:
  recommended:
  - 2.24.1.2
  minimum:
  - 2.24.0.2
MongoDB42:
  recommended:
  - 4.2.1
  minimum:
  - 4.2.0
NPP:
  recommended:
  - 7.8.1
  minimum:
  - 7.7.1
VSBuildTools:
  recommended:
  - 16
  minimum:
  - 15
VSEnterprise:
  recommended:
  - 16
  minimum:
  - 15
Python37-V3.7.5-Url: https://www.python.org/ftp/python/3.7.5/python-3.7.5-amd64.exe
Python38-V3.8.0-Url: https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe
Python27-V2.7.17-Url: https://www.python.org/ftp/python/2.7.17/python-2.7.17.amd64.msi
Git-V2.24.0.2-Url: https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi
MongoDB42-V4.2.1-Url: https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2012plus-4.2.1-signed.msi
MongoDBCompass-V6.2.3-Url: https://downloads.mongodb.com/compass/mongodb-compass-community-1.19.12-win32-x64.msi
MongoDBCompassReadonly-V6.2.3-Url: https://downloads.mongodb.com/compass/mongodb-compass-readonly-1.19.12-win32-x64.msi
Powershell-V6.2.3-Url: https://github.com/PowerShell/PowerShell/releases/download/v6.2.3/PowerShell-6.2.3-win-x64.msi
NPP-V7.8.1-Url: http://download.notepad-plus-plus.org/repository/7.x/7.8.1/npp.7.8.1.Installer.x64.exe
NPP-V7.7.1-Url: https://notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe
VSBuildTools-V16: https://aka.ms/vs/16/release/vs_buildtools.exe
VSEnterprise-V16: https://aka.ms/vs/16/release/vs_Enterprise.exe
"@
$prerequisitesyamlbuilding | Out-File -FilePath C:\Temp\prerequisites.yaml

#https://github.com/cloudbase/powershell-yaml	http://dbadailystuff.com/a-brief-introduction-to-yaml-in-powershell http://dbadailystuff.com/yaml-in-powershell

#[System.Version]"2.7.0.19530" -gt [System.Version]"3.0.0.4080"		False
#[System.Version]"2.7.0.19530" -lt  [System.Version]"3.0.0.4080"	True

#to precheck!
#get-content -Raw C:\Temp\prerequisites.yaml | ConvertFrom-Yaml -Ordered

# Convert YAML to PowerShell Object
$PsYaml = (ConvertFrom-Yaml -Yaml $RawYaml)

# Convert the Object to JSON
$PsJson = @($PsYaml | ConvertTo-Json)

# Convert JSON back to PowerShell Array
$PsArray = @($PsJson | ConvertFrom-Json)

# Convert the Array to YAML
ConvertTo-Yaml -Data $PsArray