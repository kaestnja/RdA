# https://gallery.technet.microsoft.com/scriptcenter/Ausstehenden-Neustart-d6cf137b

# set "HKLM:\SOFTWARE\Microsoft\Windows\Updates\UpdateExeVolatile" to 0

Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired"
Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending"
Test-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations"
Test-Path "HKLM:\SYSTEM\ControlSet001\Control\Session Manager\PendingFileRenameOperations"
Test-Path "HKLM:\SYSTEM\ControlSet002\Control\Session Manager\PendingFileRenameOperations"
Test-Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\InProgress"

reg query "HKLM\SOFTWARE\Microsoft\Windows\Updates" /v UpdateExeVolatile
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Installer" /v InProgress
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update" /v RebootRequired
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing" /v RebootPending
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v PendingFileRenameOperations
reg query "HKLM\SYSTEM\ControlSet001\Control\Session Manager" /v PendingFileRenameOperations
reg query "HKLM\SYSTEM\ControlSet002\Control\Session Manager" /v PendingFileRenameOperations

# set "HKLM\SOFTWARE\Microsoft\Windows\Updates\UpdateExeVolatile" to 0
# reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v PendingFileRenameOperations
# reg delete "HKLM\SYSTEM\ControlSet001\Control\Session Manager" /v PendingFileRenameOperations
# reg delete "HKLM\SYSTEM\ControlSet002\Control\Session Manager" /v PendingFileRenameOperations