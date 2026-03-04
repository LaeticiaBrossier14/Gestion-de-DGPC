"""
transcribe_from_506.py
======================
Pipeline complet pour transcription des appels à partir de 506 et annotation automatique.

Workflow:
  1. Charge les fichiers audio (appelle 506.wav, 507.wav, etc.)
  2. Les transcrit en utilisant Whisper
  3. Les ajoute au dataset
  4. Lance l'outil d'annotation en Streamlit

Usage:
  python transcribe_from_506.py
  python transcribe_from_506.py --start 506 --end 510
  python transcribe_from_506.py --start 506 --auto-launch
"""

import os
import sys
import csv
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from glob import glob
import re

# Essayer d'importer les libs nécessaires
try:
    import whisper
except ImportError:
    print("[!] Whisper non installé. Installation en cours...")
    subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper", "-q"], check=False)
    import whisper

try:
    import google.generativeai as genai
except ImportError:
    print("[!] google-generativeai non installé. Installation en cours...")
    subprocess.run([sys.executable, "-m", "pip", "install", "google-generativeai", "-q"], check=False)
    import google.generativeai as genai

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
PROJECT_DIR = Path(__file__).resolve().parent
AUDIO_DIR = PROJECT_DIR / "audio_processed"
DATASET_DIR = PROJECT_DIR / "dataset"
DATASET_FILE = DATASET_DIR / "506_onwards_transcriptions.csv"
BACKUPFILE = DATASET_DIR / "500annotations_local.csv"  # Pour référence

# Colonnes du dataset
DATASET_COLUMNS = [
    "ID", "File", "Transcription", "incident_type", "injury_severity",
    "victims_count", "fire_present", "trapped_persons", "weapons_involved",
    "hazmat_involved", "intent", "urgency_human", "daira", "commune",
    "lieu", "location_description", "summary", "notes_cot", "_annotation_status"
]

# ── Initialiser Whisper ──
print("🔄 Initialisation de Whisper (model: base)...")
try:
    whisper_model = whisper.load_model("base", device="cuda")
except Exception:
    print("  (GPU non disponible, utilisation CPU)")
    whisper_model = whisper.load_model("base", device="cpu")


def extract_call_number(filename):
    """Extraire le numéro d'appel du nom du fichier"""
    # Gère "appelle 506.wav", "Appelle 506.wav", etc.
    match = re.search(r'appelle?\s+(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def get_audio_files(start_call=506, end_call=None):
    """Récupère les fichiers audio entre start_call et end_call (inclus)"""
    audio_files = sorted(glob(str(AUDIO_DIR / "*.wav")) + glob(str(AUDIO_DIR / "*.m4a")))
    
    filtered = []
    for audio_file in audio_files:
        call_num = extract_call_number(os.path.basename(audio_file))
        if call_num is not None:
            if end_call is None:
                if call_num >= start_call:
                    filtered.append((call_num, audio_file))
            else:
                if start_call <= call_num <= end_call:
                    filtered.append((call_num, audio_file))
    
    # Trier par numéro d'appel
    filtered.sort(key=lambda x: x[0])
    return filtered


def transcribe_audio(audio_path):
    """Transcrit un fichier audio avec Whisper"""
    try:
        print(f"  🎙️ Transcription: {os.path.basename(audio_path)}...", end=" ", flush=True)
        result = whisper_model.transcribe(str(audio_path), language="fr")
        transcription = result.get("text", "").strip()
        print(f"✓ ({len(transcription)} chars)")
        return transcription
    except Exception as e:
        print(f"✗ Erreur: {str(e)[:50]}")
        return None


def load_existing_dataset():
    """Charge le dataset existant pour voir les colonnes et le format"""
    if BACKUPFILE.exists():
        with open(BACKUPFILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            first_row = next(reader, {})
            return first_row
    return {}


def create_initial_record(call_num, audio_filename, transcription):
    """Crée un enregistrement initial de l'appel"""
    record = {col: "" for col in DATASET_COLUMNS}
    record["ID"] = f"CALL_{str(call_num).zfill(4)}_Appe"
    record["File"] = audio_filename
    record["Transcription"] = transcription
    record["_annotation_status"] = "pending"
    # Les autres champs seront remplis par l'outil d'annotation
    return record


def save_to_dataset(records):
    """Sauvegarde les enregistrements dans le fichier CSV"""
    # Créer le dossier s'il n'existe pas
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    
    # Ajouter aux enregistrements existants
    existing_records = []
    if DATASET_FILE.exists():
        with open(DATASET_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_records = list(reader)
    
    # Fusionner et dédupliquer par ID
    all_records = existing_records + records
    unique_records = {}
    for record in all_records:
        unique_records[record["ID"]] = record
    
    # Trier par ID
    sorted_records = sorted(unique_records.values(), key=lambda x: int(x["ID"].split("_")[1]))
    
    # Écrire
    with open(DATASET_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=DATASET_COLUMNS)
        writer.writeheader()
        writer.writerows(sorted_records)
    
    print(f"\n✅ Dataset sauvegardé: {DATASET_FILE}")
    print(f"   Total: {len(sorted_records)} appels")


def transcribe_range(start_call, end_call=None):
    """Transcrit une plage d'appels"""
    print(f"\n🎯 Récupération des fichiers audio...")
    audio_files = get_audio_files(start_call=start_call, end_call=end_call)
    
    if not audio_files:
        print(f"❌ Aucun fichier audio trouvé entre appel {start_call} et {end_call or 'fin'}")
        return False
    
    print(f"📊 {len(audio_files)} fichiers à transcrire\n")
    
    records = []
    for call_num, audio_path in audio_files:
        transcription = transcribe_audio(audio_path)
        if transcription:
            record = create_initial_record(
                call_num,
                os.path.basename(audio_path),
                transcription
            )
            records.append(record)
    
    if records:
        save_to_dataset(records)
        return True
    else:
        print("❌ Aucune transcription réussie")
        return False


def launch_annotation_tool():
    """Lance l'outil d'annotation en Streamlit"""
    print("\n🚀 Lancement de l'outil d'annotation...")
    print("=" * 60)
    
    annotation_py = PROJECT_DIR / "annotation_app" / "dgpc_annotation_local.py"
    
    if not annotation_py.exists():
        print(f"❌ Erreur: {annotation_py} non trouvé")
        return False
    
    try:
        # Changer vers le répertoire annotation_app
        os.chdir(PROJECT_DIR / "annotation_app")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(annotation_py),
            "--logger.level=warning"
        ])
        return True
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Transcription des appels 506+ et annotation automatique"
    )
    parser.add_argument("--start", type=int, default=506, help="Appel de départ (défaut: 506)")
    parser.add_argument("--end", type=int, default=None, help="Appel de fin (défaut: dernier)")
    parser.add_argument("--auto-launch", action="store_true", help="Lancer l'annotation automatiquement")
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  Pipeline Transcription & Annotation (Appel {args.start}+)      ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Transcription
    success = transcribe_range(args.start, args.end)
    
    if success and args.auto_launch:
        # Auto-lancer l'annotation
        input("\n📝 Appuyez sur Entrée pour lancer l'outil d'annotation...")
        launch_annotation_tool()


if __name__ == "__main__":
    main()
