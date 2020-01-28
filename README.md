# RdA
RdA contains helpful scripts, to easely setup and install prerequisites, for example the following "easy onliner" for Windows Powershell:

## Expert
```
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') } -setuptype 'expert' "
```
## Server
```
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') } -setuptype 'server' "
```
## Contributor
```
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') } -setuptype 'contributor' "
``` 

### hints (maybe needed to set for Windows 10 Pro):

PS: (as Administrator)
```
[Net.ServicePointManager]::SecurityProtocol = ([Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12);
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Confirm
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') }"
Unblock-File -Path './setup_prerequisites.ps1'
```
SH: (Windows GitBash prefered (!))
```
cd $USERPROFILE'\source\repos\' && find . -type d -name .git -execdir sh -c "pwd && git stash && git fetch && git pull" \;
```