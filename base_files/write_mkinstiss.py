from glob import glob
from pathlib import Path
files = glob(".\\dist\\main\\**\\*",recursive=True)


version_line = open("readme.md","r",encoding="utf-8").read().split("\n")
__name__ = [v for v in version_line if v.find("APPNAME:")==0][0].lstrip("APNAME").lstrip(": ")
__version__ = [v for v in version_line if v.find("VERSION:")==0][0].lstrip("VERSION").lstrip(": ")

initxt = f"""
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName={__name__}
AppVersion={__version__}
WizardStyle=modern
OutputBaseFilename={__name__}
DefauktDirName={{autof}}\\{__name__}
DefaultGroupName={__name__}
UninstallDisplayIcon={{app}}\{__name__}.exe
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:{__name__}

[Files]
"""

"""
Source: "MyProg-x64.exe"; DestDir: "{app}"; DestName: "MyProg.exe"
Source: "MyProg.chm"; DestDir: "{app}"
Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

"""

files = [f.replace(".\\","") for f in files if f!='.\\dist\\main\\main.exe']
for f in files:
    tmp_files = glob(f'{f}\\*')
    flag = 0
    for tf in tmp_files:
        p = Path(tf)
        if p.is_file():
            flag += 1
    if flag == 0:
        continue
    p = Path(f)
    if p.is_dir():
        tmp_path = f.replace("dist\\main","")
        initxt += f'Source: "{f}\\*"; DestDir: "{{app}}{tmp_path}"\n'
initxt += f'Source: "dist\\main\\README.pdf"; DestDir: "{{app}}\\"\n'
initxt+=f"""
[Icons]
; Create a shortcut in the Start Menu
Name: "{{group}}\{__name__}"; Filename: "{{app}}\main.exe"
"""

with open("mkinst.iss","w",encoding="utf-8") as f:
    f.write(initxt)