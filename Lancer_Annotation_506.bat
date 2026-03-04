@echo off
REM =====================================================================
REM Lancer l'outil d'annotation pour appels 506+
REM =====================================================================

title DGPC - Outil d'Annotation (Appels 506+)
echo ==================================================
echo   DGPC: OUTIL D'ANNOTATION - Appels 506+
echo   Protection Civile - Bejaia
echo ==================================================
echo.

echo [1/2] Installation des dependances...
pip install streamlit google-generativeai pydub pandas geopy --quiet

echo.
echo [2/2] Lancement de l'application...
echo.

REM Aller dans le dossier annotation_app
cd annotation_app

REM Lancer Streamlit
streamlit run dgpc_annotation_local.py

cd ..
echo.
pause
