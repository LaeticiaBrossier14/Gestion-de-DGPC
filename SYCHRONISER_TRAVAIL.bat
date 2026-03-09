@echo off
setlocal
cd /d "%~dp0"
echo [SYNC] Démarrage de la synchronisation intelligente du travail...
echo.

:: Vérifier si Python est disponible
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH.
    pause
    exit /b 1
)

:: Lancer le script de synchronisation
python sync_work.py

echo.
echo [INFO] Terminé ! Vous pouvez continuer votre vérification dans l'outil.
echo.
pause
