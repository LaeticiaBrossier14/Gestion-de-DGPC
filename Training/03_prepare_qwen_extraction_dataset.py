# %% [markdown]
# # 03 — Préparation du Dataset d'Extraction Structurée (Qwen 2.5)
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script transforme le CSV annoté (`Donnée_réel.csv`) en un dataset
# d'instruction-tuning pour fine-tuner Qwen 2.5 avec QLoRA.
#
# **Format** : Chaque exemple = (transcription brute) -> (JSON structuré)
# Le modèle apprendra à extraire les entités d'urgence depuis le texte Arabizi.

# %% [markdown]
# ### 🔧 Configuration

# %%
import os
import sys
import json
import csv
import random
from pathlib import Path
from collections import Counter

IS_COLAB = "google.colab" in sys.modules if hasattr(sys, "modules") else False

if IS_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE_ROOT = Path("/content/drive/MyDrive")
else:
    DRIVE_ROOT = Path("f:/dgpc_pipeline_ready")

# Source
CSV_PATH = DRIVE_ROOT / "Pretraitement" / "dataset" / "Donnée_réel.csv"

# Sortie
OUTPUT_DIR = DRIVE_ROOT / "Training" / "qwen_extraction_dataset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Split
SPLIT_SEED = 42
SPLIT_RATIOS = (0.8, 0.1, 0.1)

# Champs cibles pour l'extraction JSON
TARGET_FIELDS = [
    "incident_type", "injury_severity", "victims_count",
    "fire_present", "trapped_persons", "weapons_involved",
    "hazmat_involved", "intent", "urgency_human",
    "daira", "commune", "lieu", "location_description", "summary"
]

print(f"CSV_PATH   : {CSV_PATH}")
print(f"OUTPUT_DIR : {OUTPUT_DIR}")

# %% [markdown]
# ### 1️⃣ Chargement et parsing du CSV

# %%
def load_csv_safe(csv_path):
    """Charge le CSV en gerant les encodages Windows."""
    for encoding in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        try:
            with open(csv_path, "r", encoding=encoding) as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            print(f"  CSV charge avec encodage {encoding} : {len(rows)} lignes")
            return rows
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Impossible de lire {csv_path}")

rows = load_csv_safe(CSV_PATH)

# Afficher les colonnes disponibles
if rows:
    print(f"  Colonnes : {list(rows[0].keys())}")

# %% [markdown]
# ### 2️⃣ Construction des exemples instruction-tuning
# Format ChatML pour Qwen 2.5 :
# - system : consigne d'extraction
# - user : transcription brute
# - assistant : JSON structuré (les labels annotas manuellement)

# %%
SYSTEM_PROMPT = """Tu es un expert en analyse d'appels d'urgence de la Protection Civile de Béjaïa (Algérie).
Les transcriptions sont en kabyle de Béjaïa avec du code-switching français et arabe, écrites en Arabizi.
À partir de la transcription fournie, extrais les informations structurées au format JSON.
Les champs à extraire sont :
- incident_type : type d'incident (medical_emergency, accident_vehicular, fire_building, fire_vehicle, assault_violence, accident_pedestrian, other, unknown)
- injury_severity : gravité (none, minor, severe, unknown)
- victims_count : nombre de victimes (chiffre ou 0)
- fire_present : présence de feu (yes/no)
- trapped_persons : personnes coincées (yes/no)
- weapons_involved : armes impliquées (yes/no)
- hazmat_involved : matières dangereuses (yes/no)
- intent : intention de l'appelant (report_incident, request_help, update_info, false_alarm, other)
- urgency_human : niveau d'urgence (low, medium, high, critical, unknown)
- daira : daïra administrative
- commune : commune
- lieu : lieu précis
- location_description : description détaillée du lieu
- summary : résumé de l'appel en français

Réponds UNIQUEMENT avec le JSON, sans texte supplémentaire."""


def build_instruction_example(row):
    """Construit un exemple d'instruction-tuning depuis une ligne CSV."""
    transcription = row.get("Transcription", "").strip()
    if not transcription or len(transcription) < 20:
        return None
    
    # Construire le JSON cible depuis les annotations
    target = {}
    for field in TARGET_FIELDS:
        value = row.get(field, "").strip()
        # Normaliser les valeurs vides
        if not value or value.lower() in ("", "nan", "none"):
            value = "unknown"
        # Convertir victims_count en nombre si possible
        if field == "victims_count":
            try:
                value = str(int(float(value)))
            except (ValueError, TypeError):
                value = "0"
        target[field] = value
    
    target_json = json.dumps(target, ensure_ascii=False, indent=2)
    
    # Format ChatML
    example = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcription},
            {"role": "assistant", "content": target_json}
        ],
        # Metadata pour debug
        "call_id": row.get("ID", ""),
        "file": row.get("File", ""),
    }
    
    # Optionnel : ajouter le Chain of Thought si disponible
    notes_cot = row.get("notes_cot", "").strip()
    if notes_cot and len(notes_cot) > 10:
        example["cot_reference"] = notes_cot
    
    return example


# Construire tous les exemples
examples = []
stats = Counter()

for row in rows:
    ex = build_instruction_example(row)
    if ex:
        examples.append(ex)
        stats["valid"] += 1
    else:
        stats["skipped"] += 1

print(f"\nExemples construits : {stats['valid']}")
print(f"Ignores            : {stats['skipped']}")

# %% [markdown]
# ### 3️⃣ Statistiques des labels

# %%
print("\nDistribution des incident_type :")
incident_counts = Counter()
urgency_counts = Counter()

for ex in examples:
    target = json.loads(ex["messages"][2]["content"])
    incident_counts[target["incident_type"]] += 1
    urgency_counts[target["urgency_human"]] += 1

for k, v in incident_counts.most_common():
    bar = "#" * (v // 5)
    print(f"  {k:25s}: {v:4d} {bar}")

print("\nDistribution urgency_human :")
for k, v in urgency_counts.most_common():
    bar = "#" * (v // 5)
    print(f"  {k:25s}: {v:4d} {bar}")

# %% [markdown]
# ### 4️⃣ Split et Export

# %%
random.seed(SPLIT_SEED)
indices = list(range(len(examples)))
random.shuffle(indices)

n = len(examples)
n_train = int(n * SPLIT_RATIOS[0])
n_val = int(n * SPLIT_RATIOS[1])

train = [examples[i] for i in indices[:n_train]]
val = [examples[i] for i in indices[n_train:n_train + n_val]]
test = [examples[i] for i in indices[n_train + n_val:]]

for name, data in [("train", train), ("validation", val), ("test", test)]:
    path = OUTPUT_DIR / f"{name}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for ex in data:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"  {name:12s}: {len(data):4d} exemples -> {path.name}")

# Exemple de ce que va voir le modele
print("\n--- Exemple d'instruction (premier du train) ---")
ex0 = train[0]
print(f"USER (extrait) : {ex0['messages'][1]['content'][:120]}...")
print(f"ASSISTANT       : {ex0['messages'][2]['content'][:200]}...")

print(f"\nDataset d'extraction sauvegarde dans : {OUTPUT_DIR}")
print("Prochaine etape : executer 04_train_qwen_qlora.py")
