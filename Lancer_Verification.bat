@echo off
setlocal
cd /d "%~dp0"
title DGPC - Verification Tool

set "PY_EXE=C:\Users\warda\AppData\Local\Programs\Python\Python314\python.exe"
set "OUT_LOG=verification_tool\launcher.out.log"
set "ERR_LOG=verification_tool\launcher.err.log"

if exist "%PY_EXE%" goto start_server

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY_EXE=py -3"
    goto start_server
)

where python >nul 2>nul
if %errorlevel%==0 (
    set "PY_EXE=python"
    goto start_server
)

echo [ERREUR] Python introuvable.
echo.
pause
exit /b 1

:start_server
echo Demarrage du serveur de verification...
del /q "%OUT_LOG%" "%ERR_LOG%" >nul 2>nul

if "%PY_EXE%"=="C:\Users\warda\AppData\Local\Programs\Python\Python314\python.exe" (
    start "DGPC Verification Server" /min cmd /c ""%PY_EXE%" launch_verification_tool.py 1>\"%OUT_LOG%\" 2>\"%ERR_LOG%\"" 
) else (
    start "DGPC Verification Server" /min cmd /c "%PY_EXE% launch_verification_tool.py 1>\"%OUT_LOG%\" 2>\"%ERR_LOG%\""
)

echo Attente du serveur sur http://127.0.0.1:5000 ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$deadline=(Get-Date).AddSeconds(20); $ok=$false; while((Get-Date) -lt $deadline){ try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:5000/api/stats -TimeoutSec 2 | Out-Null; $ok=$true; break } catch { Start-Sleep -Milliseconds 500 } }; if($ok){ exit 0 } else { exit 1 }"

if errorlevel 1 (
    echo.
    echo [ERREUR] Le serveur n'a pas demarre correctement.
    if exist "%ERR_LOG%" (
        echo.
        echo Dernieres erreurs:
        powershell -NoProfile -Command "Get-Content '%ERR_LOG%' -Tail 20"
    )
    echo.
    pause
    exit /b 1
)

echo.
echo Execution du git pull...
git pull

start "" http://127.0.0.1:5000
echo.
echo Application ouverte: http://127.0.0.1:5000
echo Vous pouvez fermer cette fenetre.
pause
