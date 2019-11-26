# RdA
RdA contains helpful scripts, to easely setup and install prerequisites, for example the following "easy onliner" for Windows Powershell:

## Expert
```
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites_expert.ps1') }"
```
## Server
```
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites_server.ps1') }"
```
## Contributor
```
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites_contributor.ps1') }"
``` 

###hints (maybe needed to set for Windows 10 Pro):
``` 
[Net.ServicePointManager]::SecurityProtocol = ([Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12);
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Confirm
Unblock-File -Path './setup_prerequisites_contributor.ps1'
``` 