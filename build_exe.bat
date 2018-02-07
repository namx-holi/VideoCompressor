@echo off
echo CREATES THE FILE
echo MAKE SURE YOU HAVE pyinstaller
echo use pip install pyinstaller to get it
echo.
echo make sure the Converter.py is closed before rebuilding
echo otherwise you'll get a "WindowsError: [Error 5] Access is denied"

pyinstaller Converter.py --onefile --noconsole