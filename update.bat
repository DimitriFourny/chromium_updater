@echo off
bash -c "python3 update.py"

:choice
set /P c=Do you want to run chromium_installer.exe [Y/N]?
if /I "%c%" EQU "Y" goto :install
if /I "%c%" EQU "N" goto :end
goto :choice

:install
echo Installing the new chrome version
chromium_installer.exe
echo Done

:end
@pause