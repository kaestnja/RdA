# The script exports all third-party drivers detected in use, trying to avoid Microsoft drivers that come prepackaged inside the OS
# 
# Tested on Windows 7 SP1, Windows 8.1, Windows 2012 R2 and Windows 2016
#
# Example usage: .\Export-Used-Drivers.ps1 -TargetDirectory "C:\temp\drivers"
#
#############################################
# Author: Narcis Mircea
# E-mail: narcis.mircea at gmail.com
# Script Version: 2.2
# Date: 09.04.2017
#############################################
Param (
    [Parameter(Mandatory=$false)]
    [ValidateScript({Test-Path (Split-Path $_ -Parent) -PathType Container})]
    [String]
    $TargetDirectory = '.\' # working path to store the exported data
)

$hostname = $ENV:COMPUTERNAME

# Initialize the list of detected driver packages as an array
$DriverFolders = @()

### Get all devices present in the OS currently
$Devices = Get-WmiObject Win32_PNPEntity 

# Check the drivers for each device 
foreach ($i in $Devices) {
$PNPSignedDriver = $null
$Caption = $i.Caption
Write-Host -ForegroundColor Green "Current device is: $Caption"

############################################################################################## Win32_PNPSignedDriver
# For each device found on the system, we first try the WMI class Win32_PNPSignedDriver
$PNPSignedDriver = Get-WmiObject Win32_PNPSignedDriver | Where {$_.DeviceID -eq $i.DeviceID}
if ($PNPSignedDriver -ne $null -and $PNPSignedDriver.DriverProviderName -ne "Microsoft") {
$DeviceName = $PNPSignedDriver.DeviceName
Write-Host -ForegroundColor Green "Detected a driver defined for: $DeviceName - Moving on to detecting driver INF files for this device..."
$DriverFiles = $null
$ModifiedDeviceID = $null
$Antecedent = $null
# For each driver instance from WMI class Win32_PNPSignedDriver, we compose the related WMI object name from the other WMI driver class, Win32_PNPSignedDriverCIMDataFile
$ModifiedDeviceID = $i.DeviceID -replace "\\", "\\"
$Antecedent = "\\" + $hostname + "\ROOT\cimv2:Win32_PNPSignedDriver.DeviceID=""$ModifiedDeviceID"""
# Get all related driver files for each driver listed in WMI class Win32_PNPSignedDriver
$DriverFiles += Get-WmiObject Win32_PNPSignedDriverCIMDataFile | where {$_.Antecedent -eq $Antecedent}
if ($DriverFiles -ne $null) {
Write-Host "Some driver files have been detected... Moving on to driver folder detection from DriverStore."
foreach ($x in $DriverFiles) {
# We elliminate double backslashes from the file paths
$path = $x.Dependent.Split("=")[1] -replace '\\\\', '\'
# We elliminate the trailing and ending quotes from the file paths
$path2 = $path.Substring(1,$path.Length-2)
# On the first pass, we only process the INF files as there is a very low chance of existing more than one driver package on the same machine, with the same INF file legth
if ($path2.Split("\\")[$path2.Split("\\").Length-1].split(".")[1] -eq "inf") {
# We get the file attributes for each INF file
$InfItem = Get-Item -Path $path2
$DeviceName = $i.Name
Write-Output "The current driverfile is ""$path2"" for the device ""$DeviceName"""
# We search in the DriverRepository for all packages containing this INF file, with the same length
$PackagedInfDrivers = Get-ChildItem C:\Windows\System32\DriverStore\FileRepository -Include "*.inf" -Recurse | where {$_.Length -eq $InfItem.Length}
# We initialize the array of found driver packages for this INF file
$CurrentlyDetectedPackages = @()
foreach ($f in $PackagedInfDrivers) {
$PackagePath = Split-Path -Path $f -Parent
Write-Host "PackagePath detected $PackagePath" -ForegroundColor Magenta
# We add each result at once, as there should be only one INF file per each subfolder of "C:\Windows\System32\DriverStore\FileRepository", so we should not have duplicates here
$CurrentlyDetectedPackages += $PackagePath
} # End of foreach ($f in $PackagedInfDrivers)
# In case we found several driver packages with the same INF file length inside, we proceed to a second pass detection
if ($CurrentlyDetectedPackages.Count -gt 1 ) {
Write-Host "More than one Driver Packages have been detected for the current INF file!!" -ForegroundColor Gray
Write-Host "The packages detected are $CurrentlyDetectedPackages - Trying to determine if only one is a good match." -ForegroundColor Gray
# We initialize a second array of found driver packages for this WMI driver object
$CurrentlyDetectedPackages2 = @()
# In the second pass, we are now interested in the total number of driver files, because we must match all of them in a Driver Package folder, for it to be considered detected on the second pass
foreach ($q in $DriverFiles) {
# We elliminate double backslashes from the file paths
$path = $q.Dependent.Split("=")[1] -replace '\\\\', '\'
# We elliminate the trailing and ending quotes from the file paths
$path2 = $path.Substring(1,$path.Length-2)
# Now we only process other files besides INF
if ($path2.Split("\\")[$path2.Split("\\").Length-1].split(".")[1] -ne "inf") {
# We get the file attributes
$DriverItem = Get-Item -Path $path2
# We parse now again the driver packages detected in the first pass, to try and filter them down
foreach ($h in $CurrentlyDetectedPackages) {
# This time, we search for all driver files, excluding the INF file, and we keep track of where we found those, amond the driver packages detected in the first pass
$PackagedDriverItems = Get-ChildItem $h -Exclude "*.inf" -Recurse | where {$_.Length -eq $DriverItem.Length}
# For every search result, we add one more item in the $CurrentlyDetectedPackages2 array with the location of the Driver Package
# This will lead to multiple entries with the same value and depending on how many of those we have, we know that the proper
# driver files are in the correct Driver Package
if ($PackagedDriverItems -ne $null) {
$CurrentlyDetectedPackages2 += $h
} # End of if ($PackagedDriverItems -ne $null)
} # End of foreach ($h in $CurrentlyDetectedPackages)
} # End of if ($path2.Split("\\")[$path2.Split("\\").Length-1].split(".")[1] -ne "inf")
} # End of foreach ($q in $DriverFiles)
# We initialize a control variable, to see later if we validated any driver package or not
$DriverValidated = 0
# We parse each item from the second pass results, including the reoccurences, and for each item we add the valid packages to the final results
foreach ($m in $CurrentlyDetectedPackages2){
# We get the total number of driver files, excluding the inf file, to compare with the number of reoccurences for each item in $CurrentlyDetectedPackages2
# If an item reappears in $CurrentlyDetectedPackages2 for the same number of times as the number of detected driver files, this driver package is considered validated
# The target Count number is the total number of driver related files for the current device, minus one, representing the INF file, which was not processed in the second pass
$Count = $DriverFiles.Count - 1
# The condition is counting how many occurences of each Driver Package are in $CurrentlyDetectedPackages2. If there is a value that appears as many times as the number of Driver Related files,
# it means that for that package, all related driver files from the system are also present there, so the Package is VALIDATED.
if (((0..($CurrentlyDetectedPackages2.Count-1)) | where {$CurrentlyDetectedPackages2[$_] -eq $m}).Count -eq $Count) {
if (!($DriverFolders -contains $m)){
Write-Host "The Driver Package $m has been VALIDATED in the second pass." -ForegroundColor Cyan
$DriverValidated = 1
$DriverFolders += $m
}
}
} # end of - foreach ($m in $CurrentlyDetectedPackages2)
# If no driver package is validated, we add all packages detected in the second pass. This may be already only one, the correct one :)
if ($DriverValidated -eq 0) {
Write-Host "No Driver Package has been validated on the second pass!" -ForegroundColor Cyan
Write-Host "We will add all driver packages detected in the second pass, to be sure we do not miss the correct one!" -ForegroundColor Cyan
foreach ($k in $CurrentlyDetectedPackages2){
if (!($DriverFolders -contains $k)){
$DriverFolders += $k
}
}
} # End of if ($DriverValidated -eq 0)
# End of multiple drivers detected routine.
} # End of if ($CurrentlyDetectedPackages.Count -gt 1 )
# In case we found one package driver or less, we add it to the final results array, if it is not already present there, detected from another device
else {
if (!($DriverFolders -contains $PackagePath)){
$DriverFolders += $PackagePath
} # End of if (!($DriverFolders -contains $PackagePath))
} # End of else
} # End of if ($path2.Split("\\")[$path2.Split("\\").Length-1].split(".")[1] -eq "inf")
} # End of foreach ($i in $DriverFiles)
} # end of - if ($DriverFiles -ne $null) 

############################################################################################## Win32_SystemDriver
else {
$SystemDriverPNPEntry = $null
Write-Host -ForegroundColor Cyan "For device: $ModifiedDeviceID - no driver files have been detected in the Win32_PNPSignedDriverCIMDataFile WMI class. Moving on to Win32_SystemDriver WMI class."
$Antecedent = "\\" + $hostname + "\ROOT\cimv2:Win32_PNPEntity.DeviceID=""$ModifiedDeviceID"""
$SystemDriverPNPEntry = Get-WmiObject Win32_SystemDriverPNPEntity | where {$_.Antecedent -eq $Antecedent} | Select-Object -First 1

if ($SystemDriverPNPEntry -ne $null) {
$SystemDriverFileObject = Get-WmiObject Win32_SystemDriver | where {$_.Name -eq $SystemDriverPNPEntry.Dependent.split("=")[1].Substring(1,$SystemDriverPNPEntry.Dependent.split("=")[1].Length-2)}
if ($SystemDriverFileObject -ne $null) {
$SystemDriverPath = $SystemDriverFileObject.PathName
Write-Host "Driver Path detected for the current device is $SystemDriverPath Checking now if this is a Microsoft file."
# Testing driver file path before getting file information
if (Test-Path -Path $SystemDriverPath) {
$SysItem = Get-Item -Path $SystemDriverPath
# Checking now to see if this sys file is not actually released by Microsoft...
if ($SysItem.VersionInfo.ProductName -like "*Microsoft*" -or $SysItem.VersionInfo.CompanyName -like "*Microsoft*") {
Write-Host "This driver file is a Microsoft product. Skipping..."
continue
}   
# We continue now to detect the associated folder from the DriverStore
# We search in the DriverRepository for all packages containing this SYS file, with the same length
$PackagedSysDrivers = Get-ChildItem C:\Windows\System32\DriverStore\FileRepository -Include "*.sys" -Recurse | where {$_.Length -eq $SysItem.Length -and $_.Name -eq $SysItem.Name}
# We initialize the array of found driver packages for this SYS file
$CurrentlyDetectedPackages = @()
$DriverStorePath = ("$env:windir\System32\DriverStore\FileRepository\").ToLower()
# The sys files found here may be present in subfolders of the driver packages from the FileRepository, so we must detect the entire driver packages in this case and not their subfolders
if ($PackagedSysDrivers -ne $null){
foreach ($f in $PackagedSysDrivers) {
$CurrentPath = $f.FullName.ToLower()
if (!$CurrentPath.StartsWith($DriverStorePath)) {
Write-Host "This driver path ($CurrentPath) is not valid for export as it is not present in the OS driver file repository. Skipping..."
continue
}
else {
$PackagePath = $DriverStorePath + $CurrentPath.Replace($DriverStorePath,"").Split("\")[0]
Write-Host "PackagePath detected $PackagePath" -ForegroundColor Magenta
}
# We add each result only after making sure we do not have a duplicate
if (!($CurrentlyDetectedPackages -contains $PackagePath)){
$CurrentlyDetectedPackages += $PackagePath
}
} # End of foreach ($f in $PackagedInfDrivers)
# Here we add all discovered packages to the master array, as here we do not have a method of second pass detection
foreach ($z in $CurrentlyDetectedPackages) {
if (!($DriverFolders -contains $z)){
$DriverFolders += $z
}
} # end of - foreach ($z in $CurrentlyDetectedPackages)

} # end of if ($PackagedSysDrivers -ne $null)
} # end of if (Test-Path -Path $SystemDriverPath)  
} # end of - if ($SystemDriverFileObject -ne $null)
} # end of - if ($SystemDriverPNPEntry -ne $null)
else {
Write-Host "No driver files have been detected for the current device in the Win32_SystemDriver either."
}
} # end of - if ($DriverFiles -ne $null) {} else
} # end of - if ($PNPSignedDriver -ne $null -and $PNPSignedDriver.DriverProviderName -ne "Microsoft")
elseif ($PNPSignedDriver -eq $null) {
Write-Host "No driver files detected in the Win32_PNPSignedDriver for the current device."
}
elseif ($PNPSignedDriver.DriverProviderName -eq "Microsoft") {
Write-Host "The currently found device driver is provided by Microsoft. Skipping..."
}
} # end of - foreach ($i in $Devices)

############################################################################################## Export Drivers section

# We create the target folder before we start the copy operation
if (!(Test-Path -Path $TargetDirectory -PathType container)) {New-Item -Path $TargetDirectory -ItemType "directory"}

# We copy each Driver Package detected to the target folder
foreach ($v in $DriverFolders) {
$v
Copy-Item -Path $v -Destination $TargetDirectory -Recurse -Force
} # End of foreach ($v in $DriverFolders)