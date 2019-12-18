cd %USERPROFILE%\source\repos
FOR /F "tokens=*" %%G IN ('DIR /B /AD /S __pycache__') DO RMDIR /S /Q "%%G"
FOR /F "tokens=*" %%G IN ('DIR /B /AD /S bin') DO RMDIR /S /Q "%%G"
FOR /F "tokens=*" %%G IN ('DIR /B /AD /S obj') DO RMDIR /S /Q "%%G"
pause
del /F /S /Q thumbs.db
del /F /S *.mta
del /F /S desktop*.ini
del /F /S *.pyc
exit
