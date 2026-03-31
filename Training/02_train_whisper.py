# %% [markdown]
# # 02 — Fine-Tuning Whisper ASR
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script fine-tune `openai/whisper-small` sur le dataset DGPC
# en utilisant HuggingFace `Seq2SeqTrainer` avec support fp16.
#
# **Prérequis :** `pip install datasets transformers evaluate jiwer accelerate`

# %% [markdown]
# ### Installation (cellule Colab)

# %%
# !pip install -q datasets transformers evaluate jiwer accelerate

# %% [markdown]
# ### 🔧 Configuration

# %%
import os
import sys
import torch
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Union

IS_COLAB = "google.colab" in sys.modules if hasattr(sys, "modules") else False

if IS_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE_ROOT = Path("/content/drive/MyDrive")
else:
    DRIVE_ROOT = Path("f:/dgpc_pipeline_ready")

# Chemins
DATASET_DIR = DRIVE_ROOT / "Training" / "hf_dataset_whisper"
PROCESSOR_DIR = DRIVE_ROOT / "Training" / "whisper_processor"
OUTPUT_DIR = DRIVE_ROOT / "Training" / "whisper_finetuned"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Modele de base
MODEL_ID = "openai/whisper-small"

# Hyperparametres
BATCH_SIZE = 16 if IS_COLAB else 2       # 16 sur GPU, 2 en local
GRADIENT_ACCUM = 2 if IS_COLAB else 1
LEARNING_RATE = 1e-5
NUM_EPOCHS = 10 if IS_COLAB else 1        # 1 epoch en local pour test
WARMUP_STEPS = 100
FP16 = torch.cuda.is_available()
MAX_STEPS_LOCAL = 5                       # Test local rapide

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device          : {DEVICE}")
print(f"Batch size      : {BATCH_SIZE}")
print(f"FP16            : {FP16}")
print(f"Epochs          : {NUM_EPOCHS}")
print(f"Dataset dir     : {DATASET_DIR}")

# %% [markdown]
# ### 1️⃣ Chargement du dataset et du processor

# %%
from datasets import DatasetDict
from transformers import WhisperProcessor, WhisperForConditionalGeneration

print("Chargement du dataset preprocesse...")
dataset = DatasetDict.load_from_disk(str(DATASET_DIR))
print(f"Dataset : {dataset}")

print(f"\nChargement du processor depuis {PROCESSOR_DIR}...")
processor = WhisperProcessor.from_pretrained(str(PROCESSOR_DIR))

print(f"Chargement du modele {MODEL_ID}...")
model = WhisperForConditionalGeneration.from_pretrained(MODEL_ID)

# Configurer le modele pour le francais (la langue la plus proche du code-switching)
model.generation_config.language = "french"
model.generation_config.task = "transcribe"
model.generation_config.forced_decoder_ids = None

print(f"Modele charge : {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M parametres")

# %% [markdown]
# ### 2️⃣ Data Collator personnalisé pour Whisper
# Whisper nécessite un padding spécial : les labels doivent être paddés à -100
# (ignorés par la loss) et les features audio doivent être paddées à la même longueur.

# %%
@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any
    decoder_start_token_id: int

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # Séparer input_features et labels
        input_features = [{"input_features": f["input_features"]} for f in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")
        
        # Pad les labels avec -100 (ignore_index pour CrossEntropy)
        label_features = [{"input_ids": f["labels"]} for f in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")
        
        # Remplacer le padding token par -100
        labels = labels_batch["input_ids"].masked_fill(
            labels_batch.attention_mask.ne(1), -100
        )
        
        # Retirer le token BOS si présent au début
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]
        
        batch["labels"] = labels
        return batch

data_collator = DataCollatorSpeechSeq2SeqWithPadding(
    processor=processor,
    decoder_start_token_id=model.config.decoder_start_token_id,
)

print("Data Collator configure")

# %% [markdown]
# ### 3️⃣ Métrique WER (Word Error Rate)

# %%
import evaluate

wer_metric = evaluate.load("wer")

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids
    
    # Remplacer -100 par le pad_token_id pour le décodage
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id
    
    # Décoder les prédictions et les références
    pred_str = processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)
    
    wer = 100 * wer_metric.compute(predictions=pred_str, references=label_str)
    
    return {"wer": wer}

print("Metrique WER configuree")

# %% [markdown]
# ### 4️⃣ Configuration de l'entraînement

# %%
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer

training_args = Seq2SeqTrainingArguments(
    output_dir=str(OUTPUT_DIR),
    
    # Epochs / Steps
    num_train_epochs=NUM_EPOCHS,
    max_steps=MAX_STEPS_LOCAL if not IS_COLAB else -1,
    
    # Batch
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUM,
    
    # Optimisation
    learning_rate=LEARNING_RATE,
    warmup_steps=WARMUP_STEPS,
    weight_decay=0.01,
    
    # Precision
    fp16=FP16,
    
    # Evaluation
    eval_strategy="steps" if IS_COLAB else "no",
    eval_steps=500,
    
    # Sauvegarde
    save_strategy="steps",
    save_steps=500,
    save_total_limit=3,
    load_best_model_at_end=True if IS_COLAB else False,
    metric_for_best_model="wer",
    greater_is_better=False,
    
    # Génération (pour calculer le WER pendant l'évaluation)
    predict_with_generate=True,
    generation_max_length=225,
    
    # Logging
    logging_steps=25,
    report_to="none",
    
    # Reproductibilité
    seed=42,
    
    # Divers
    remove_unused_columns=False,
    label_names=["labels"],
    push_to_hub=False,
)

print("TrainingArguments configures")

# %% [markdown]
# ### 5️⃣ Lancement de l'entraînement

# %%
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset.get("validation", None),
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    processing_class=processor.feature_extractor,
)

print("Debut de l'entrainement...")
train_result = trainer.train()

# Sauvegarder le modèle final
trainer.save_model(str(OUTPUT_DIR / "final"))
processor.save_pretrained(str(OUTPUT_DIR / "final"))

print(f"\nEntrainement termine !")
print(f"  Loss finale   : {train_result.training_loss:.4f}")
print(f"  Modele sauve  : {OUTPUT_DIR / 'final'}")

# %% [markdown]
# ### 6️⃣ Évaluation finale sur le test set

# %%
if "test" in dataset:
    print("\nEvaluation sur le test set...")
    test_results = trainer.evaluate(dataset["test"])
    print(f"  WER test : {test_results.get('eval_wer', 'N/A'):.2f}%")
else:
    print("Pas de test set disponible")

print("\nPipeline ASR termine !")
print(f"Le modele fine-tune est dans : {OUTPUT_DIR / 'final'}")
