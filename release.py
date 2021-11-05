import os

release_version = "广告工具1.2.0"

if __name__ == '__main__':
    os.system("pyinstaller -F --onefile -w -i .\\ico\\logo.ico --add-data \".\\ico;ico\" .\\run.py")
    os.system("del .\\dist\\" + release_version + ".exe")
    os.system("ren .\\dist\\run.exe " + release_version + ".exe")
