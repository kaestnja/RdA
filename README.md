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
Currently, I am working a lot on this sproject, please carefully use the scripts.
Of course, I should generate a release version of it and let the "easy onliners" point to it next time - in a cuple of days!