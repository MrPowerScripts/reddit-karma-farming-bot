@ECHO OFF

Powershell.exe -executionpolicy bypass -File ./deps/windows/windows.ps1
if errorlevel 1 pause & exit 

if "%1"=="" (
  echo running without menu
  pipenv run python ./src/init.py
)

if "%1"=="menu" (
  echo running with menu
  pipenv run python ./src/menu.py
)

echo exiting...
pause