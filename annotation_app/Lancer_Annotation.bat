@echo off
title DGPC - Outil d'Annotation V6
echo ==================================================
echo   DGPC : OUTIL D'ANNOTATION - PROTECTION CIVILE
echo   Bejaia - Version 6.0
echo ==================================================
echo.

echo [1/3] Installation des dependances...
pip install streamlit google-generativeai pydub pandas geopy --quiet

echo.
echo [2/3] Creation des dossiers...
if not exist "audio_raw" mkdir audio_raw
if not exist "audio_processed" mkdir audio_processed
if not exist "dataset" mkdir dataset

echo.
echo [3/3] Lancement de l'application...
echo.
echo ============================================
echo   INSTRUCTIONS:
echo   - Deposez vos fichiers audio dans: audio_raw/
echo   - Le navigateur s'ouvrira automatiquement
echo   - Si non, allez sur: http://localhost:8501
echo ============================================
echo.

start http://localhost:8501
streamlit run dgpc_annotation_local.py --server.headless true

pause
