@echo off
REM =====================================================================
REM Lancer la transcription Qwen3-ASR (optimisé pour Kabyle)
REM =====================================================================

title DGPC - Qwen3-ASR Pipeline (Appels 506+)
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   DGPC: QWEN3-ASR TRANSCRIPTION (Appels 506+)            ║
echo ║   Optimisé pour les langues low-resource                 ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM --- Installation des dépendances ---
echo [1/3] Installation des dépendances...
echo.
pip install qwen-asr transformers torch torchaudio numpy --quiet

echo.
REM --- Transcription avec Qwen3-ASR ---
echo [2/3] Transcription Qwen3-ASR des appels 506+...
echo.
python transcribe_qwen3_from_506.py --start 506

echo.
echo ✅ Pipeline terminé!
echo.
echo 📝 Prochaine étape: Lancer 'Lancer_Annotation.bat' pour annoter
pause
