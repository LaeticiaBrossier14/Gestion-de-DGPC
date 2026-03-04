"""
monitor_and_sync.py
===================
Monitore le CSV de transcription et lance la synchronisation automatiquement
"""

import os
import sys
import time
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR / "dataset"
CSV_FILE = DATASET_DIR / "506_onwards_transcriptions.csv"

def check_csv_exists():
    """Vérifier si le CSV existe et est complet"""
    return CSV_FILE.exists()

def count_csv_lines():
    """Compter les lignes du CSV"""
    if not CSV_FILE.exists():
        return 0
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def wait_for_transcription(timeout=7200):
    """Attendre que la transcription soit terminée (max 2h)"""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║      ⏳ ATTENTE TRANSCRIPTION (Timeout: 2h)              ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    start_time = time.time()
    last_count = 0
    stable_count = 0
    
    print("Monitoring CSV...")
    
    while True:
        elapsed = time.time() - start_time
        
        if check_csv_exists():
            count = count_csv_lines()
            
            # Afficher progrès
            if count != last_count:
                print(f"⏳ Lignes: {count} | Temps: {int(elapsed)}s", end="\r")
                stable_count = 0
            else:
                stable_count += 1
            
            # Si pas de changement pendant 60s = probablement fini
            if stable_count > 60 and count > 100:
                print(f"\n✅ Transcription terminée: {count} lignes")
                return True
            
            last_count = count
        
        # Timeout
        if elapsed > timeout:
            print(f"\n❌ Timeout après {int(elapsed/60)} minutes")
            return False
        
        time.sleep(1)

def run_sync():
    """Lancer la synchronisation"""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║         🔄 LANCEMENT SYNCHRONISATION CSV ↔ JSON          ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    try:
        result = subprocess.run(
            [sys.executable, "sync_csv_json.py"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation: {e}")
        return False

def main():
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║      📊 MONITOR TRANSCRIPTION & SYNCHRONISATION          ║
║         Appels 506+ → CSV → JSON → Formats Multiples    ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Attendre transcription
    if wait_for_transcription():
        # Lancer sync
        if run_sync():
            print(f"""
╔═══════════════════════════════════════════════════════════╗
║                    ✅ SUCCÈS COMPLET                     ║
║                                                          ║
║ Fichiers créés:                                          ║
║   ✓ CSV (transcriptions)                                 ║
║   ✓ JSON (structuré)                                     ║
║   ✓ Metadata (stats)                                     ║
║   ✓ Parquet (compressé)                                  ║
║   ✓ Excel (tableur)                                      ║
║   ✓ JSONL (line delimited)                               ║
║                                                          ║
║ Prêt pour:                                               ║
║   → Annotation IA                                        ║
║   → Analyse                                              ║
║   → ML Training                                          ║
╚═══════════════════════════════════════════════════════════╝
""")
            return 0
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                    ❌ ERREUR DÉTECTÉE                    ║
╚═══════════════════════════════════════════════════════════╝
""")
    return 1

if __name__ == "__main__":
    sys.exit(main())
