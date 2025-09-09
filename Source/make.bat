"D:\PycharmProjects\Nautilus\venv10\Scripts\pyinstaller" nautilus.py -n "Nautilus.exe" --onefile --noconsole --add-data "theme.json;." --upx-dir D:\PycharmProjects\UPX
rem -i "Nautilus.ico" --splash "splashfile.gif" 

copy "D:\PycharmProjects\Nautilus\theme.json" "D:\PycharmProjects\GeraniumsPot\dist\"
