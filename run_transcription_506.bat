@echo off
REM =====================================================================
REM Lancer la transcription des appels 506+ avec annotation
REM =====================================================================

title DGPC - Pipeline Transcription Appels 506+
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   DGPC: TRANSCRIPTION & ANNOTATION (Appels 506+)          ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM --- Installation des dépendances ---
echo [1/3] Vérification des dépendances...
pip install openai-whisper google-generativeai python-dotenv pydub streamlit --quiet

echo.
REM --- Transcription ---
echo [2/3] Transcription des appels 506+...
echo.
python transcribe_from_506.py --start 506 --auto-launch

echo.
echo ✅ Pipeline terminé!
pause
