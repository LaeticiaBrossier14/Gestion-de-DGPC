# %% [markdown]
# # 🚀 ÉTAPE 2 : DATASET BUILDER (PRÉTRAITEMENT MACHINE LEARNING)
# **Mémoire Protection Civile - DGPC Béjaïa**
#
# **Objectif :** Prendre les "chunks" audio parfaits (résultant du nettoyage et de l'alignement)
# et les transformer en données mathématiques pures compréhensibles par les IAs comme Whisper ou Qwen.
#
# **Processus SOTA (State Of The Art) :**
# 1. Échantillonnage du son (16kHz strict).
# 2. Remplacement des vieux MFCC par des **Log-Mel Spectrograms**.
# 3. Tokenisation du texte Arabizi en Identifiants (IDs) avec Byte-Pair Encoding (BPE).
# 4. Création d'une structure de données ultra-rapide (HuggingFace `Dataset`).

# %% [markdown]
# ### 1️⃣ Importation des Librairies Industrielles
# Nous utilisons `datasets` pour la RAM optimisée et `transformers` pour l'extraction de pointe.

# %%
import os
import json
import librosa
import numpy as np
from pathlib import Path
from datasets import Dataset, DatasetDict

# Ces modules transforment le Son en Image (FeatureExtractor)
# et l'Arabizi en Chiffres (Tokenizer)
from transformers import WhisperFeatureExtractor, WhisperTokenizer, WhisperProcessor

print("✅ Librairies MLOps chargées !")

# %% [markdown]
# ### 2️⃣ Configuration du Feature Extractor & Tokenizer
# Whisper exige exactement **16 000 Hz**. Si tes audios sont en 44.1kHz ou 48kHz (téléphones),
# l'IA ne comprendra rien et entendra le son au ralenti ou en accéléré.

# %%
# On choisit le modèle de base (Whisper small est excellent pour QLoRA car très rapide)
MODEL_ID = "openai/whisper-small"

print(f"🔄 Téléchargement de la configuration pour {MODEL_ID}...")
feature_extractor = WhisperFeatureExtractor.from_pretrained(MODEL_ID)
tokenizer = WhisperTokenizer.from_pretrained(MODEL_ID, language="french", task="transcribe")
processor = WhisperProcessor.from_pretrained(MODEL_ID, language="french", task="transcribe")

SAMPLING_RATE = feature_extractor.sampling_rate # Par défaut : 16000
print(f"✅ Configuration chargée. Taux d'échantillonnage requis : {SAMPLING_RATE} Hz")

# %% [markdown]
# ### 3️⃣ Chargement des Métadonnées (Le fichier JSONL des Chunks)
# Ici on va lire le tableau des petits audios (12 secondes) créés à l'Étape 1.

# %%
# Chemin vers ton fichier généré par MMS Forced Alignment (après correction Colab !)
JSONL_PATH = "f:/dgpc_pipeline_ready/Pretraitement/partage_memoire/segments_asr_ready.jsonl"

def load_metadata(jsonl_file):
    examples = []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            # On s'assure que le son dure moins de 30 secondes (Limitation stricte de Whisper)
            if data["duration"] < 30.0:
                examples.append({
                    "audio_path": data["audio"],
                    "text": data["text"]
                })
    return examples

examples = load_metadata(JSONL_PATH)
print(f"✅ {len(examples)} chunks audio chargés et filtrés (< 30s) !")

# %% [markdown]
# ### 4️⃣ Fonction de Transformation Magique (Audio → Mel + Texte → IDs)
# Voici le cœur de ton Mémoire ! C'est ce bloc qui remplace les ancestrales fonctions MFCC+TF-IDF
# par des Spectrogrammes Mel et du BPE.

# %%
def prepare_dataset(batch):
    """
    Cette fonction va traiter une liste d'exemples en parallèle.
    """
    # 1. Charger et resampler l'audio brut à 16kHz
    audio_path = batch["audio_path"]
    
    # librosa.load avec sr=16000 s'occupe de faire le resampling proprement sans bug !
    audio_array, _ = librosa.load(audio_path, sr=SAMPLING_RATE)
    
    # 2. Audio -> Log-Mel Spectrogram
    # C'est l'image des fréquences que lira le modèle.
    batch["input_features"] = feature_extractor(
        audio_array, 
        sampling_rate=SAMPLING_RATE
    ).input_features[0]

    # 3. Texte Arabizi -> Token IDs
    # Le modèle reçoit une liste de chiffres (ex: [124, 550, 4810]) représentant la grammaire
    batch["labels"] = tokenizer(batch["text"]).input_ids

    return batch

# %% [markdown]
# ### 5️⃣ Création et Exécution du Super-Dataset (Map)
# On convertit tout cela en un format ultra-rapide (Arrow) utilisé par HuggingFace.

# %%
print("⚙️  Création de la base de données HuggingFace...")
raw_dataset = Dataset.from_list(examples)

print("🚀 Lancement du Prétraitement lourd (Spectrogrammes + Tokens)...")
# Note : En local, on peut tester sur 5 exemples avec 'raw_dataset.select(range(5))'
# Sur Google Colab, on fera tout avec map(num_proc=4) pour utiliser le CPU au maximum !

# TEST LOCAL (On prend juste 2 exemples pour vérifier que ça marche sans bloquer ton PC)
test_dataset = raw_dataset.select(range(2))

processed_dataset = test_dataset.map(
    prepare_dataset,
    remove_columns=raw_dataset.column_names, # On garde uniquement input_features et labels
    desc="Extraction Features"
)

print("\\n✅ Prétraitement terminé ! Voici les données prêtes pour l'Entraînement Neuronal :")
print(processed_dataset)

# %% [markdown]
# ### 6️⃣ Sauvegarde du Dataset Prêt-à-l'Emploi
# On le sauvegarde sur le disque. C'est CE DOSSIER qu'on passera ensuite à QLoRA/Whisper pour apprendre.

# %%
output_dir = "f:/dgpc_pipeline_ready/Training/hf_dataset_ready"
processed_dataset.save_to_disk(output_dir)
print(f"💾 Dataset sauvegardé de manière optimisée (Arrow) dans : {output_dir}")
