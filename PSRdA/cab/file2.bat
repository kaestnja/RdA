Makecab -f test.ddf
pause
exit

for %%A in (*.cab) do (
	cabarc x "d:\sw_2014_rev\plastics\%%~A" "C:\SW_TEMP\"
	cabarc /m none n "c:\sw_temp\%%~A" "C:\SW_TEMP\*.*"
	xcopy "C:\SW_TEMP\%%~A" /v /y
	del "C:\SW_TEMP\*.*" /q
)

dir "W:\Scripts\Attack Surface Analyzer\data"
makecab.exe C:\files\program.jpg C:\files\program.cab
makecab.exe 
advfirewall.xml 
bcd.xml 
config.xml 
desktops.xml 
files.xml 
firewall.xml 
gac.xml 
handles.xml 
log.xml 
logons.xml 
mailslotlist.xml 
objects.xml 
pages.xml 
pipelist.xml 
ports.xml 
processes.xml 
rpc.xml 
security-events.xml 
services.xml 
shares.xml 
threads.xml 
windows.xml
