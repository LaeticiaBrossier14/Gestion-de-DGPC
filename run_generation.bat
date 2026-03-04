@echo off
setlocal

set PROJECT_DIR=g:\AZ\Documents\gestion des appelles telephoniques
set PYTHON="%PROJECT_DIR%\.venv\Scripts\python.exe"
set GEN_SCRIPT="%PROJECT_DIR%\augmentation\generate_synthetic.py"
set ORG_SCRIPT="%PROJECT_DIR%\merge_and_organize.py"
set PENDING="%PROJECT_DIR%\ml_pipeline\dataset\synthetic_generation\pending_tasks.jsonl"

echo ============================================
echo  PIPELINE DE GENERATION SYNTHETIQUE
echo ============================================
echo.

cd /d "%PROJECT_DIR%"

:: --- STEP 1: Organiser les donnees existantes + calculer ce qui reste ---
echo [STEP 1/3] Organisation des donnees existantes...
echo.
%PYTHON% %ORG_SCRIPT%

if not exist %PENDING% (
    echo.
    echo [INFO] Aucune tache en attente. Tout est genere!
    goto :END
)

:: --- STEP 2: Generer SEULEMENT les taches restantes ---
:: Fichier de sortie avec timestamp pour ne pas ecraser les anciens
for /f "tokens=*" %%i in ('%PYTHON% -c "from datetime import datetime; print(datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S'))"') do set TS=%%i
set OUTPUT_FILE=%PROJECT_DIR%\ml_pipeline\dataset\annotations_synthetic_%TS%.jsonl

echo.
echo ============================================
echo [STEP 2/3] Generation des taches en attente...
echo   Source: pending_tasks.jsonl
echo   Output: annotations_synthetic_%TS%.jsonl
echo ============================================
echo.

%PYTHON% %GEN_SCRIPT% --plan_path %PENDING% --output_jsonl "%OUTPUT_FILE%" %*

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERREUR] La generation a echoue.
    echo Les donnees existantes sont preservees.
    goto :END
)

:: --- STEP 3: Re-organiser avec les nouvelles donnees ---
echo.
echo ============================================
echo [STEP 3/3] Re-organisation avec les nouvelles donnees...
echo ============================================
echo.
%PYTHON% %ORG_SCRIPT%

:END
echo.
echo ============================================
echo  PIPELINE TERMINE
echo ============================================
endlocal
