if (Test-Path -Path "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools") {
  Write-Host "Found VS 2019 Build Tools - Excellent"
} else {
  Write-Host "VS 2019 Build Tools not found"
  Write-Host "Read windows installation guide https://github.com/MrPowerScripts/reddit-karma-farming-bot/blob/master/docs/3-windows.md"
  exit 1
}

# Invoke-WebRequest -Uri https://download.lfd.uci.edu/pythonlibs/z4tqcw5k/PyStemmer-2.0.1-cp39-cp39-win_amd64.whl -OutFile ./deps/windows/PyStemmer-2.0.1-cp39-cp39-win_amd64.whl

