# %% [markdown]
# # 01 — Construction du Dataset HuggingFace pour Whisper
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script charge les manifests JSONL (produits par le script 00),
# construit un `DatasetDict` HuggingFace avec les features audio
# (Log-Mel Spectrogram) et les labels tokenisés (BPE), puis sauvegarde
# le tout sur disque pour l'entraînement.
#
# **Prérequis :** `pip install datasets transformers librosa soundfile`

# %% [markdown]
# ### Installation (cellule Colab)

# %%
# !pip install -q datasets transformers librosa soundfile

# %% [markdown]
# ### 🔧 Configuration

# %%
import os
import sys
import json
import librosa
import numpy as np
from pathlib import Path

IS_COLAB = "google.colab" in sys.modules if hasattr(sys, "modules") else False

if IS_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE_ROOT = Path("/content/drive/MyDrive")
else:
    DRIVE_ROOT = Path("f:/dgpc_pipeline_ready")

MANIFEST_DIR = DRIVE_ROOT / "Training" / "manifests"
OUTPUT_DIR = DRIVE_ROOT / "Training" / "hf_dataset_whisper"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Modèle Whisper de base pour le Processor
MODEL_ID = "openai/whisper-small"

# Test local : ne traiter que N exemples (None = tout traiter)
LOCAL_TEST_LIMIT = 5 if not IS_COLAB else None

print(f"MANIFEST_DIR : {MANIFEST_DIR}")
print(f"OUTPUT_DIR   : {OUTPUT_DIR}")
print(f"MODEL_ID     : {MODEL_ID}")
print(f"TEST_LIMIT   : {LOCAL_TEST_LIMIT}")

# %% [markdown]
# ### 1️⃣ Chargement du Processor Whisper

# %%
from transformers import WhisperProcessor

print(f"Chargement du processor {MODEL_ID}...")
processor = WhisperProcessor.from_pretrained(
    MODEL_ID, language="french", task="transcribe"
)

SAMPLING_RATE = processor.feature_extractor.sampling_rate  # 16000
print(f"Processor charge. Sampling rate = {SAMPLING_RATE} Hz")

# %% [markdown]
# ### 2️⃣ Chargement des manifests

# %%
from datasets import Dataset, DatasetDict

def load_manifest(jsonl_path):
    """Charge un manifest JSONL en liste de dicts."""
    entries = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries

splits = {}
for split_name in ["train", "validation", "test"]:
    path = MANIFEST_DIR / f"{split_name}.jsonl"
    if path.exists():
        data = load_manifest(path)
        if LOCAL_TEST_LIMIT:
            data = data[:LOCAL_TEST_LIMIT]
        splits[split_name] = Dataset.from_list(data)
        print(f"  {split_name:12s}: {len(splits[split_name])} exemples")
    else:
        print(f"  {split_name:12s}: FICHIER MANQUANT ({path})")

raw_ds = DatasetDict(splits)
print(f"\nDatasetDict cree : {raw_ds}")

# %% [markdown]
# ### 3️⃣ Fonction de préparation des features
# C'est le coeur du prétraitement ML :
# - Audio brut -> Log-Mel Spectrogram (via WhisperFeatureExtractor)
# - Texte Arabizi -> Token IDs (via WhisperTokenizer, BPE)

# %%
def prepare_example(example):
    """
    Transforme un seul exemple (audio_path + text) en features Whisper.
    
    Entrée:
        example["audio_path"] : chemin vers le fichier WAV
        example["text"]       : transcription nettoyée (Arabizi)
    
    Sortie:
        example["input_features"] : Log-Mel Spectrogram [80, T]
        example["labels"]         : Token IDs (BPE)
    """
    audio_path = example["audio_path"]
    
    # Charger l'audio et resampler a 16kHz (librosa gere tous les formats)
    try:
        audio_array, sr = librosa.load(audio_path, sr=SAMPLING_RATE, mono=True)
    except Exception as e:
        print(f"  ERREUR chargement {audio_path}: {e}")
        # Retourner un silence de 1s en cas d'erreur
        audio_array = np.zeros(SAMPLING_RATE, dtype=np.float32)
    
    # Audio -> Log-Mel Spectrogram (80 canaux, standard Whisper)
    input_features = processor.feature_extractor(
        audio_array, sampling_rate=SAMPLING_RATE
    ).input_features[0]
    
    # Texte -> Token IDs (BPE)
    labels = processor.tokenizer(example["text"]).input_ids
    
    example["input_features"] = input_features
    example["labels"] = labels
    
    return example

# %% [markdown]
# ### 4️⃣ Application du prétraitement (Map)

# %%
print("Lancement du pretraitement (Spectrogrammes + Tokens)...")
print("  Cela peut prendre plusieurs minutes sur Colab...")

processed_ds = raw_ds.map(
    prepare_example,
    remove_columns=raw_ds["train"].column_names,
    desc="Feature Extraction",
    num_proc=1,  # 1 en local, augmenter sur Colab si multi-CPU
)

print(f"\nDataset pretraite : {processed_ds}")
for split_name, ds in processed_ds.items():
    print(f"  {split_name:12s}: {len(ds)} exemples | colonnes: {ds.column_names}")

# %% [markdown]
# ### 5️⃣ Sauvegarde sur disque (format Arrow optimisé)

# %%
print(f"\nSauvegarde vers {OUTPUT_DIR}...")
processed_ds.save_to_disk(str(OUTPUT_DIR))
print(f"Dataset sauvegarde dans : {OUTPUT_DIR}")

# Sauvegarder aussi le processor pour l'entrainement
processor_dir = DRIVE_ROOT / "Training" / "whisper_processor"
processor_dir.mkdir(parents=True, exist_ok=True)
processor.save_pretrained(str(processor_dir))
print(f"Processor sauvegarde dans : {processor_dir}")

print("\nProchaine etape : executer 02_train_whisper.py")
