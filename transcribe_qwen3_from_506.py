"""
transcribe_qwen3_from_506.py
=============================
Alternative: Utiliser Qwen3-ASR pour une meilleure transcription Kabyle.

Qwen3-ASR d'Alibaba est optimisé pour les langues low-resource et dialectes,
ce qui devrait donner de meilleurs résultats pour le Kabyle que Whisper.

Usage:
  python transcribe_qwen3_from_506.py
  python transcribe_qwen3_from_506.py --start 506 --end 520
  python transcribe_qwen3_from_506.py --use-cpu (plus lent, mais moins de RAM)

Requirement: Un GPU est vivement recommandé (sinon très lent).
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
import warnings
warnings.filterwarnings("ignore")

try:
    from qwen_asr import Qwen3ASRModel
except ImportError:
    print("[!] Qwen3-ASR non installé. Installation en cours...")
    subprocess.run([sys.executable, "-m", "pip", "install", "qwen-asr", "-q"], check=False)
    from qwen_asr import Qwen3ASRModel

try:
    import google.generativeai as genai
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "google-generativeai", "-q"], check=False)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
PROJECT_DIR = Path(__file__).resolve().parent
AUDIO_DIR = PROJECT_DIR / "audio_processed"
DATASET_DIR = PROJECT_DIR / "dataset"
DATASET_FILE = DATASET_DIR / "506_onwards_transcriptions_qwen3.csv"

DATASET_COLUMNS = [
    "ID", "File", "Transcription", "incident_type", "injury_severity",
    "victims_count", "fire_present", "trapped_persons", "weapons_involved",
    "hazmat_involved", "intent", "urgency_human", "daira", "commune",
    "lieu", "location_description", "summary", "notes_cot", "_annotation_status"
]

# Configuration du modèle Qwen3-ASR
device = "cuda"  # Sera changé à cpu si demandé


def extract_call_number(filename):
    """Extraire le numéro d'appel du nom du fichier"""
    match = re.search(r'appelle?\s+(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def get_audio_files(start_call=506, end_call=None):
    """Récupère les fichiers audio entre start_call et end_call"""
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
    
    filtered.sort(key=lambda x: x[0])
    return filtered


def transcribe_audio_qwen3(model, audio_path):
    """Transcrit un fichier audio avec Qwen3-ASR"""
    try:
        print(f"  🎙️  Qwen3-ASR: {os.path.basename(audio_path)}...", end=" ", flush=True)
        
        # Qwen3-ASR API
        results = model.transcribe(
            audio=str(audio_path),
            language="auto",  # Auto-détection
            word_level_timestamps=False,
        )
        
        # Qwen3-ASR retourne une liste de résultats
        if isinstance(results, list):
            transcription = " ".join([r.get("text", "") for r in results])
        else:
            transcription = results.get("text", "").strip()
        
        transcription = transcription.strip()
        print(f"✓ ({len(transcription)} chars)")
        return transcription
    except Exception as e:
        print(f"✗ Erreur: {str(e)[:50]}")
        return None


def create_initial_record(call_num, audio_filename, transcription):
    """Crée un enregistrement initial"""
    record = {col: "" for col in DATASET_COLUMNS}
    record["ID"] = f"CALL_{str(call_num).zfill(4)}_Appe"
    record["File"] = audio_filename
    record["Transcription"] = transcription
    record["_annotation_status"] = "pending"
    return record


def save_to_dataset(records):
    """Sauvegarde dans le dataset CSV"""
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    
    existing_records = []
    if DATASET_FILE.exists():
        with open(DATASET_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_records = list(reader)
    
    all_records = existing_records + records
    unique_records = {}
    for record in all_records:
        unique_records[record["ID"]] = record
    
    sorted_records = sorted(unique_records.values(), key=lambda x: int(x["ID"].split("_")[1]))
    
    with open(DATASET_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=DATASET_COLUMNS)
        writer.writeheader()
        writer.writerows(sorted_records)
    
    print(f"\n✅ Dataset (Qwen3-ASR) sauvegardé: {DATASET_FILE}")
    print(f"   Total: {len(sorted_records)} appels")


def transcribe_range(start_call, end_call=None, use_cpu=False):
    """Transcrit une plage d'appels avec Qwen3-ASR"""
    global device
    if use_cpu:
        device = "cpu"
        print("⚠️  Mode CPU: La transcription sera plus lente (considérez un GPU)\n")
    else:
        print("🔥 Mode GPU activé (plus rapide)\n")
    
    print(f"📥 Chargement du modèle Qwen3-ASR-1.7B...")
    print("   (Cela peut prendre 2-3 minutes la première fois)\n")
    
    try:
        model = Qwen3ASRModel.from_pretrained(
            "Qwen/Qwen3-ASR-1.7B",
            device_map=device,
            torch_dtype="auto"
        )
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
        print("  Conseil: Installer les dépendances manquantes ou forcer CPU:")
        print("  pip install -U transformers torch torchaudio numpy --upgrade")
        return False
    
    print(f"\n🎯 Récupération des fichiers audio...")
    audio_files = get_audio_files(start_call=start_call, end_call=end_call)
    
    if not audio_files:
        print(f"❌ Aucun fichier audio trouvé entre appel {start_call} et {end_call or 'fin'}")
        return False
    
    print(f"📊 {len(audio_files)} fichiers à transcrire\n")
    
    records = []
    for call_num, audio_path in audio_files:
        transcription = transcribe_audio_qwen3(model, audio_path)
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


def main():
    parser = argparse.ArgumentParser(
        description="Transcription Qwen3-ASR des appels 506+"
    )
    parser.add_argument("--start", type=int, default=506, help="Appel de départ")
    parser.add_argument("--end", type=int, default=None, help="Appel de fin")
    parser.add_argument("--use-cpu", action="store_true", help="Forcer CPU (plus lent)")
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  Qwen3-ASR Pipeline (Appel {args.start}+)                       ║
║  Optimisé pour les langues low-resource (Kabyle)          ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    transcribe_range(args.start, args.end, use_cpu=args.use_cpu)


if __name__ == "__main__":
    main()
