
setlocal

set "files=readme.pdf main.spec mkinstiss.py"
set "allExist=True"

for %%f in(files%) do (
    if not exist "%%f" (
        echo %%f is not existed
        set "allExist=false"
    )
)

if "%allExist%"=="false" (
    echo any files not found, abort the process
    exit /b 1
)

endlocal

SETLOCAL enabledelayedexpansion

SET "inputFile=readme.md"
SET "versioninfo="

FOR /f "usebackq delims=" %%a in ("%inpputFile%") do (
    set "line=%%a"
    if "!line:~0,8!"=="VERSION:" (
        set "versioninfo=!line:~9!"
    )
)

REM init directories

DEL /q /s output
del /q dist\main\

REM build
MKDIR output
echo y|pyinstaller main.spec

REM COPY NECCESSARY DIRECTORIES

setlocal

REM 対象外にするファイル/フォルダ名をカンマで区切って指定
set "exclude_list=main.ipynb,build,dist,data,log"

REM 現在のディレクトリにあるすべてのファイルとフォルダを処理
for /f "delims=" %%i in ('dir /b /a') do (
    REM 対象外リストにあるか確認
    echo %exclude_list% | findstr /i /c:"%%i" >nul
    if errorlevel 1 (
        REM 対象外リストにない場合、特定の処理を実行
        ECHO y |xcopy /s /y "%%i" "dist/main/%%i"
    ) else (
        echo Skipping %%i
    )
)

endlocal

REM create installer

python write_mkinstiss.py
"C:\Program Files (x86)\Inno Setup 6\Compil32.exe" /cc mkinst.iss
