# Running the bot on Windows 10

1. Download and install Python for Windows. You can find [all the releases here](https://www.python.org/downloads/windows/). Make sure you have at least v3.7. You can [click here](https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe) to download the installer for 3.9.1 directly. **Make sure to check the "add python to PATH" option** or the script won't be able to find it.

2. Download the Visual Studio 2019 Build tools [from this link](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16). Then install the C++ build tools workload. You can disable all optional packages except for the `windows 10 SDK`, `C++ CMake tools for Windows`, and `MSVC v142 VS2019 C++ x64/x86 build tools`. See the screenshot below, and looked at the options checked on the right side. That should be all you need.

![image](https://user-images.githubusercontent.com/1307942/104216961-a77cbd00-5432-11eb-9aec-c56fcef58d2f.png)

3. Run `run_windows.bat`
