@ECHO OFF
if not exist ".env-created" (
  echo. 2>.env-created
  echo no virtualenv detected doing setup before running
  Powershell.exe -executionpolicy bypass -File ./deps/windows/windows.ps1
  pip3 install pipenv
  pip3 install ./deps/windows/PyStemmer-2.0.1-cp39-cp39-win_amd64.whl
  pipenv install
)
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