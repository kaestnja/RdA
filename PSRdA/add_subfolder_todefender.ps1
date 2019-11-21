## Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

$folders = get-childitem D:\ -directory
echo $folders
pause
foreach ($folder in $folders)
 {
 $folderexception = $folder.fullname + "\" + ($folder.name)
 echo $folderexception
 # Add-MpPreference -ExclusionPath “C:\Temp”
 Add-MpPreference -ExclusionPath $folderexception
 pause
 }

