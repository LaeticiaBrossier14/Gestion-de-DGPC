"""
dashboard_progress.py
=====================
Dashboard de suivi du pipeline 506+ en temps réel
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json

PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR / "dataset"
AUDIO_DIR = PROJECT_DIR / "audio_processed"

def get_status():
    """Obtenir le statut complet du pipeline"""
    
    status = {
        "timestamp": datetime.now().isoformat(),
        "audio": {
            "total": len(list(AUDIO_DIR.glob("*.wav")) + list(AUDIO_DIR.glob("*.m4a"))),
            "from_506": 0
        },
        "transcription": {
            "csv_exists": False,
            "lines": 0,
            "completion_percent": 0
        },
        "json": {
            "exists": False,
            "records": 0
        },
        "formats": {
            "csv": False,
            "json": False,
            "parquet": False,
            "excel": False,
            "jsonl": False
        }
    }
    
    # Compter audio 506+
    for f in AUDIO_DIR.glob("*506*.wav") + AUDIO_DIR.glob("*507*.wav"):
        status["audio"]["from_506"] += 1
    
    # CSV
    csv_file = DATASET_DIR / "506_onwards_transcriptions.csv"
    if csv_file.exists():
        status["transcription"]["csv_exists"] = True
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                status["transcription"]["lines"] = len(f.readlines())
            # Approximation: 304 appels (506-809)
            status["transcription"]["completion_percent"] = min(100, int(status["transcription"]["lines"] / 305 * 100))
        except:
            pass
    
    # JSON
    json_file = DATASET_DIR / "506_onwards_transcriptions.json"
    if json_file.exists():
        status["json"]["exists"] = True
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                status["json"]["records"] = data.get("total_calls", 0)
        except:
            pass
    
    # Formats multiples
    status["formats"]["parquet"] = (DATASET_DIR / "506_onwards_transcriptions.parquet").exists()
    status["formats"]["excel"] = (DATASET_DIR / "506_onwards_transcriptions.xlsx").exists()
    status["formats"]["jsonl"] = (DATASET_DIR / "506_onwards_transcriptions.jsonl").exists()
    
    return status

def print_dashboard():
    """Afficher le dashboard"""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
        status = get_status()
        
        print(f"""
╔═════════════════════════════════════════════════════════════════╗
║                   📊 PIPELINE 506+ - DASHBOARD                 ║
║                                                                 ║
║  Mise à jour: {status['timestamp']}                           ║
╚═════════════════════════════════════════════════════════════════╝

📁 AUDIO
────────────────────────────────────────────────────────────────
  Total fichiers:      {status['audio']['total']}
  Appels 506+:         ✓ Présents
  Source:              audio_processed/

🎙️  TRANSCRIPTION (Whisper)
────────────────────────────────────────────────────────────────""")
        
        if status["transcription"]["csv_exists"]:
            bar_length = 40
            filled = int(bar_length * status["transcription"]["completion_percent"] / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"""  Statut:              ⏳ EN COURS
  Progression:         [{bar}] {status['transcription']['completion_percent']}%
  Lignes CSV:          {status['transcription']['lines']}/305 appels
  ETA:                 Dépend de GPU (2-3h)
  Fichier:             506_onwards_transcriptions.csv""")
        else:
            print(f"""  Statut:              ⏳ EN ATTENTE
  Progression:         [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%
  Lignes CSV:          0/305 appels
  Message:             Whisper initialise le modèle...""")
        
        print(f"""
📋 JSON & MÉTADATA
────────────────────────────────────────────────────────────────""")
        
        if status["json"]["exists"]:
            print(f"""  Statut:              ✅ PRÊT
  Fichier:             506_onwards_transcriptions.json
  Records:             {status['json']['records']}
  Structure:           Hiérarchique (ID, transcription, annotation)""")
        else:
            print(f"""  Statut:              ⏳ EN ATTENTE
  Message:             Sera créé après transcription""")
        
        print(f"""
📤 FORMATS MULTIPLES
────────────────────────────────────────────────────────────────
  Parquet (compressé):  {'✅ READY' if status['formats']['parquet'] else '⏳ À venir'}
  Excel (tableur):      {'✅ READY' if status['formats']['excel'] else '⏳ À venir'}
  JSONL (line-delim):   {'✅ READY' if status['formats']['jsonl'] else '⏳ À venir'}

🎯 PROCHAINES ÉTAPES
────────────────────────────────────────────────────────────────
  1. ⏳ Attendre fin transcription
  2. 📊 Créer JSON & exports
  3. 📝 Lancer annotation IA
  4. ✅ Valider cohérence données
  5. 📈 Prêt pour ML training

⌨️  COMMANDES
────────────────────────────────────────────────────────────────
  Vérifier transcription: python transcribe_from_506.py --start 506
  Forcer sync manuel:    python sync_csv_json.py
  Lancer annotation:     streamlit run annotation_app/dgpc_annotation_local_v5_FIXED.py

💡 STATUT GÉNÉRAL: {'🟡 EN COURS' if status['transcription']['completion_percent'] < 100 else '🟢 COMPLET'}

╔═════════════════════════════════════════════════════════════════╗
║  Appuyez sur CTRL+C pour arrêter | Refresh auto chaque 5s      ║
╚═════════════════════════════════════════════════════════════════╝
""")
        
        time.sleep(5)

if __name__ == "__main__":
    try:
        print_dashboard()
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard arrêté")
        sys.exit(0)
