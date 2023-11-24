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

Just in case, you cannt realy start, maybe some first commands help out.

SH: (Windows GitBash prefered (!))
```
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
```

PS: (as Administrator)
```
[Net.ServicePointManager]::SecurityProtocol = ([Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls11 -bor [Net.SecurityProtocolType]::Tls12 -bor [Net.SecurityProtocolType]::Tls13);
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Confirm
Invoke-Expression "& { $(Invoke-RestMethod 'https://github.com/kaestnja/RdA/raw/master/PSRdA/setup_prerequisites.ps1') }"
Unblock-File -Path './setup_prerequisites.ps1'
```
Stay Up-to-date on your second developer station.

SH: (Windows GitBash prefered (!))
```
cd $USERPROFILE'\source\repos\' && find . -type d -name .git -execdir sh -c "pwd && git stash && git fetch && git pull" \;
```

set nano as editor, because sometime the local editor is opened during git "calls" and the closing of the editor prevents the further "calls". Nano can be closed via "strg + x", by the way vim can be closed with "esc" than ":q!". 
```
git config --global core.editor "nano"
```

https://www.w3docs.com/snippets/git/how-to-force-git-pull-to-override-local-files.html
```
git fetch --all
git reset --hard origin/master

#only if needed:
git stash
git stash list
git stash drop
git pull
```
