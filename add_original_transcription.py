"""
Enrichit verification_progress.json en ajoutant le champ 'original_transcription'
depuis les fichiers CSV sources pour chaque entrée qui ne l'a pas déjà.
"""
import json
import csv
from pathlib import Path

BASE = Path(__file__).parent
PROGRESS_FILE = BASE / "verification_tool" / "verification_progress.json"

CSV_SOURCES = [
    BASE / "dataset" / "500annotations_local.csv",
    BASE / "annotation_app" / "dataset" / "annotations_local.csv",
]

# ── 1. Charger toutes les transcriptions originales depuis les CSVs
print("Chargement des transcriptions originales depuis les CSVs...")
original_map = {}  # filename -> transcription originale

for csv_path in CSV_SOURCES:
    if not csv_path.exists():
        print(f"  [SKIP] CSV introuvable : {csv_path}")
        continue
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row.get("File", "").strip()
            transcription = row.get("Transcription", "").strip()
            if filename and filename not in original_map:
                original_map[filename] = transcription
    print(f"  [OK] {csv_path.name} -> {len(original_map)} transcriptions chargees")

print(f"\nTotal transcriptions originales disponibles : {len(original_map)}")

# ── 2. Charger le fichier de progression
print("\nChargement de verification_progress.json...")
with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
    progress = json.load(f)
print(f"Entrées dans progress.json : {len(progress)}")

# ── 3. Ajouter 'original_transcription' là où elle est absente
added = 0
not_found = 0

for key, entry in progress.items():
    if "original_transcription" not in entry:
        original = original_map.get(key, "")
        entry["original_transcription"] = original
        added += 1
        if not original:
            not_found += 1

print(f"\n  -> Champ 'original_transcription' ajoute a {added} entrees")
print(f"  -> {not_found} entrees sans transcription originale trouvee dans les CSV (cle introuvable)")

# ── 4. Sauvegarder
print("\nSauvegarde du fichier enrichi...")
with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
    json.dump(progress, f, ensure_ascii=False, indent=2)

print("[OK] Termine ! verification_progress.json mis a jour avec les transcriptions originales.")
print("   Faites POST /api/reload dans l'outil pour rafraichir.")
