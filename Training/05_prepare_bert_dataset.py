# %% [markdown]
# # 05 — Préparation du Dataset BERT (Classification Baseline)
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script prépare les données pour une baseline académique BERT :
# - Tâche 1 : Classification `incident_type` (multi-classe)
# - Tâche 2 : Classification `urgency_human` (multi-classe)
#
# On utilise les transcriptions textuelles annotées du CSV.
# BERT ne génère pas de JSON — il classifie directement.

# %% [markdown]
# ### 🔧 Configuration

# %%
import os
import sys
import csv
import json
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

CSV_PATH = DRIVE_ROOT / "Pretraitement" / "dataset" / "Donnée_réel.csv"
OUTPUT_DIR = DRIVE_ROOT / "Training" / "bert_classification_dataset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SPLIT_SEED = 42
SPLIT_RATIOS = (0.8, 0.1, 0.1)

# Classes minimum : on fusionne les classes rares ayant < MIN_CLASS_COUNT exemples
MIN_CLASS_COUNT = 5

print(f"CSV_PATH   : {CSV_PATH}")
print(f"OUTPUT_DIR : {OUTPUT_DIR}")

# %% [markdown]
# ### 1️⃣ Chargement du CSV

# %%
def load_csv(csv_path):
    for enc in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        try:
            with open(csv_path, "r", encoding=enc) as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Impossible de lire {csv_path}")

rows = load_csv(CSV_PATH)
print(f"CSV charge : {len(rows)} lignes")

# %% [markdown]
# ### 2️⃣ Nettoyage du texte pour BERT
# BERT lit du texte brut. On garde l'Arabizi, on enlève juste
# les labels de locuteurs et la ponctuation excessive.

# %%
import re

def clean_for_bert(text):
    """Nettoyage léger pour BERT : on garde la richesse linguistique."""
    t = text.strip()
    # Retirer les labels de locuteurs
    t = re.sub(
        r'(?:Caller|Operator|Appelant|Repondant|Op|Cal|S1|S2|R|B|P|C|A|F|M)\s*:\s*',
        ' ', t, flags=re.IGNORECASE
    )
    t = t.replace('\u2014', ' ').replace('\u2013', ' ')
    # Garder la ponctuation de base (point, virgule) mais retirer le bruit
    t = re.sub(r'[_*#@&%$^~`\[\]{}«»"""]', ' ', t)
    t = re.sub(r'\.{3,}', ' ', t)  # Retirer les "..." (séparateurs de tours)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

# Test
test = "Caller: ma3lishe... Operator: Anda a Madame?"
print(f"  IN  : {test}")
print(f"  OUT : {clean_for_bert(test)}")

# %% [markdown]
# ### 3️⃣ Construction des exemples pour les deux tâches

# %%
def normalize_label(value, valid_set=None):
    """Normalise un label. Retourne None si invalide."""
    if not value or not isinstance(value, str):
        return None
    v = value.strip().lower()
    if v in ("", "nan", "none", "inconnu"):
        return None
    if valid_set and v not in valid_set:
        return None
    return v

# Tâche 1 : incident_type
incident_examples = []
# Tâche 2 : urgency_human
urgency_examples = []

for row in rows:
    text = row.get("Transcription", "").strip()
    if len(text) < 30:
        continue
    
    text_clean = clean_for_bert(text)
    
    # incident_type
    inc_type = normalize_label(row.get("incident_type"))
    if inc_type and inc_type != "unknown":
        incident_examples.append({"text": text_clean, "label": inc_type})
    
    # urgency_human
    urg = normalize_label(row.get("urgency_human"))
    if urg and urg != "unknown":
        urgency_examples.append({"text": text_clean, "label": urg})

print(f"\nExemples incident_type : {len(incident_examples)}")
print(f"Exemples urgency_human : {len(urgency_examples)}")

# %% [markdown]
# ### 4️⃣ Fusion des classes rares
# Les classes avec trop peu d'exemples sont fusionnées dans "other"
# pour éviter les problèmes de classification avec des classes à 1-2 exemples.

# %%
def merge_rare_classes(examples, min_count, merge_into="other"):
    """Fusionne les classes ayant moins de min_count exemples."""
    counts = Counter(ex["label"] for ex in examples)
    rare = {k for k, v in counts.items() if v < min_count}
    
    if rare:
        print(f"  Classes fusionnees dans '{merge_into}' (< {min_count} ex) : {rare}")
        for ex in examples:
            if ex["label"] in rare:
                ex["label"] = merge_into
    
    return examples

print("\nincident_type :")
incident_examples = merge_rare_classes(incident_examples, MIN_CLASS_COUNT)
print("\nurgency_human :")
urgency_examples = merge_rare_classes(urgency_examples, MIN_CLASS_COUNT)

# Distribution finale
print("\nDistribution incident_type finale :")
for k, v in Counter(ex["label"] for ex in incident_examples).most_common():
    print(f"  {k:25s}: {v}")

print("\nDistribution urgency_human finale :")
for k, v in Counter(ex["label"] for ex in urgency_examples).most_common():
    print(f"  {k:25s}: {v}")

# %% [markdown]
# ### 5️⃣ Création du mapping label -> ID

# %%
def build_label_map(examples):
    """Construit un mapping label -> index trié."""
    labels = sorted(set(ex["label"] for ex in examples))
    label2id = {label: i for i, label in enumerate(labels)}
    id2label = {i: label for label, i in label2id.items()}
    return label2id, id2label

inc_label2id, inc_id2label = build_label_map(incident_examples)
urg_label2id, urg_id2label = build_label_map(urgency_examples)

print(f"\nincident_type labels ({len(inc_label2id)}) : {inc_label2id}")
print(f"urgency_human labels ({len(urg_label2id)}) : {urg_label2id}")

# %% [markdown]
# ### 6️⃣ Split et Export en CSV

# %%
def split_and_export(examples, label2id, task_name, output_dir, seed, ratios):
    """Split reproductible et export CSV pour chaque split."""
    random.seed(seed)
    indices = list(range(len(examples)))
    random.shuffle(indices)
    
    n = len(examples)
    n_train = int(n * ratios[0])
    n_val = int(n * ratios[1])
    
    splits = {
        "train": [examples[i] for i in indices[:n_train]],
        "val": [examples[i] for i in indices[n_train:n_train + n_val]],
        "test": [examples[i] for i in indices[n_train + n_val:]],
    }
    
    task_dir = output_dir / task_name
    task_dir.mkdir(parents=True, exist_ok=True)
    
    for split_name, data in splits.items():
        csv_path = task_dir / f"{split_name}.csv"
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["text", "label", "label_id"])
            writer.writeheader()
            for ex in data:
                writer.writerow({
                    "text": ex["text"],
                    "label": ex["label"],
                    "label_id": label2id[ex["label"]],
                })
        print(f"  {task_name}/{split_name:5s} : {len(data):4d} exemples -> {csv_path.name}")
    
    # Sauvegarder le mapping
    meta = {"label2id": label2id, "id2label": {str(k): v for k, v in 
            {v: k for k, v in label2id.items()}.items()}, "num_labels": len(label2id)}
    with open(task_dir / "label_config.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    # Sauvegarder les poids de classe (pour gérer le déséquilibre)
    counts = Counter(ex["label"] for ex in examples)
    total = sum(counts.values())
    weights = {label: total / (len(counts) * count) for label, count in counts.items()}
    with open(task_dir / "class_weights.json", "w", encoding="utf-8") as f:
        json.dump(weights, f, ensure_ascii=False, indent=2)
    print(f"  Poids de classe sauvegardes dans class_weights.json")

print("Export incident_type :")
split_and_export(incident_examples, inc_label2id, "incident_type", OUTPUT_DIR, SPLIT_SEED, SPLIT_RATIOS)

print("\nExport urgency_human :")
split_and_export(urgency_examples, urg_label2id, "urgency_human", OUTPUT_DIR, SPLIT_SEED, SPLIT_RATIOS)

print(f"\nDataset BERT sauvegarde dans : {OUTPUT_DIR}")
print("Prochaine etape : executer 06_train_bert_classifier.py")
