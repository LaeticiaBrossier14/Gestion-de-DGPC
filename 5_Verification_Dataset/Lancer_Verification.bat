@echo off
chcp 65001 > nul
echo ===================================================
echo 🎙️ Serveur de Verification Audio - Bejaia
echo ===================================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe sur cet ordinateur !
    echo Merci d'installer Python depuis le Microsoft Store ou https://www.python.org/downloads/
    pause
    exit 
)

echo.
echo Lancement du serveur en cours... (Ne fermez pas cette fenetre noire !)
echo Une page web devrait s'ouvrir dans votre navigateur dans quelques secondes.
echo.
python launch_review.py

echo.
echo Le serveur a ete arrete.
pause
