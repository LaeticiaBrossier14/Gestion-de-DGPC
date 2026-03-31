# %% [markdown]
# # 06 — Entraînement BERT Classifier (Baseline Académique)
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script fine-tune `bert-base-multilingual-cased` pour classifier :
# - `incident_type` (10 classes)
# - `urgency_human` (4 classes)
#
# C'est la baseline académique de référence pour le mémoire.
# On utilise les poids de classe pour gérer le déséquilibre.
#
# **Prérequis** : `pip install transformers datasets scikit-learn accelerate`

# %% [markdown]
# ### Installation (cellule Colab)

# %%
# !pip install -q transformers datasets scikit-learn accelerate

# %% [markdown]
# ### 🔧 Configuration

# %%
import os
import sys
import json
import csv
import torch
import numpy as np
from pathlib import Path

IS_COLAB = "google.colab" in sys.modules if hasattr(sys, "modules") else False

if IS_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE_ROOT = Path("/content/drive/MyDrive")
else:
    DRIVE_ROOT = Path("f:/dgpc_pipeline_ready")

# Quelle tâche entraîner ? Changer ici :
TASK = "incident_type"  # ou "urgency_human"

DATASET_DIR = DRIVE_ROOT / "Training" / "bert_classification_dataset" / TASK
OUTPUT_DIR = DRIVE_ROOT / "Training" / f"bert_finetuned_{TASK}"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_ID = "bert-base-multilingual-cased"

# Hyperparamètres
BATCH_SIZE = 16 if IS_COLAB else 4
NUM_EPOCHS = 10 if IS_COLAB else 1
LEARNING_RATE = 2e-5
MAX_LENGTH = 512   # BERT supporte max 512 tokens
MAX_STEPS_LOCAL = 5
FP16 = torch.cuda.is_available()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Task       : {TASK}")
print(f"Device     : {DEVICE}")
print(f"Model      : {MODEL_ID}")
print(f"Dataset    : {DATASET_DIR}")

# %% [markdown]
# ### 1️⃣ Chargement des données et du label mapping

# %%
from datasets import Dataset

def load_csv_dataset(csv_path):
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "text": row["text"],
                "label": int(row["label_id"]),
            })
    return Dataset.from_list(rows)

train_ds = load_csv_dataset(DATASET_DIR / "train.csv")
val_ds = load_csv_dataset(DATASET_DIR / "val.csv")
test_ds = load_csv_dataset(DATASET_DIR / "test.csv")

# Charger le mapping
with open(DATASET_DIR / "label_config.json", "r", encoding="utf-8") as f:
    label_config = json.load(f)

label2id = label_config["label2id"]
id2label = {int(k): v for k, v in label_config["id2label"].items()}
num_labels = label_config["num_labels"]

# Charger les poids de classe
with open(DATASET_DIR / "class_weights.json", "r", encoding="utf-8") as f:
    class_weights_raw = json.load(f)

# Convertir en tensor ordonné par label_id
class_weights = torch.tensor(
    [class_weights_raw[id2label[i]] for i in range(num_labels)],
    dtype=torch.float32
)

print(f"\nTrain : {len(train_ds)} | Val : {len(val_ds)} | Test : {len(test_ds)}")
print(f"Labels ({num_labels}) : {id2label}")
print(f"Poids  : {class_weights.tolist()}")

# %% [markdown]
# ### 2️⃣ Tokenisation

# %%
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

def tokenize_fn(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
    )

train_ds = train_ds.map(tokenize_fn, batched=True, desc="Tokenize train")
val_ds = val_ds.map(tokenize_fn, batched=True, desc="Tokenize val")
test_ds = test_ds.map(tokenize_fn, batched=True, desc="Tokenize test")

print("Tokenisation terminee")

# %% [markdown]
# ### 3️⃣ Chargement du modèle BERT

# %%
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_ID,
    num_labels=num_labels,
    id2label=id2label,
    label2id=label2id,
)

total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Modele charge : {total_params / 1e6:.1f}M params ({trainable_params / 1e6:.1f}M trainables)")

# %% [markdown]
# ### 4️⃣ Métriques (Accuracy, F1 Macro, Classification Report)

# %%
from sklearn.metrics import accuracy_score, f1_score, classification_report

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    acc = accuracy_score(labels, predictions)
    f1_macro = f1_score(labels, predictions, average="macro", zero_division=0)
    f1_weighted = f1_score(labels, predictions, average="weighted", zero_division=0)
    
    return {
        "accuracy": acc,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
    }

print("Metriques configurees (accuracy, F1 macro, F1 weighted)")

# %% [markdown]
# ### 5️⃣ Trainer avec poids de classe (Weighted CrossEntropy)

# %%
from transformers import Trainer, TrainingArguments

class WeightedTrainer(Trainer):
    """Trainer personnalise avec ponderation des classes."""
    
    def __init__(self, class_weights=None, **kwargs):
        super().__init__(**kwargs)
        if class_weights is not None:
            self.class_weights = class_weights.to(self.args.device)
        else:
            self.class_weights = None
    
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        
        if self.class_weights is not None:
            loss_fn = torch.nn.CrossEntropyLoss(weight=self.class_weights)
        else:
            loss_fn = torch.nn.CrossEntropyLoss()
        
        loss = loss_fn(logits, labels)
        return (loss, outputs) if return_outputs else loss


training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR),
    
    num_train_epochs=NUM_EPOCHS,
    max_steps=MAX_STEPS_LOCAL if not IS_COLAB else -1,
    
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    
    learning_rate=LEARNING_RATE,
    warmup_ratio=0.1,
    weight_decay=0.01,
    
    fp16=FP16,
    
    eval_strategy="epoch" if IS_COLAB else "no",
    save_strategy="epoch",
    save_total_limit=3,
    load_best_model_at_end=True if IS_COLAB else False,
    metric_for_best_model="f1_macro",
    greater_is_better=True,
    
    logging_steps=10,
    report_to="none",
    seed=42,
    
    push_to_hub=False,
)

trainer = WeightedTrainer(
    class_weights=class_weights,
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    compute_metrics=compute_metrics,
    processing_class=tokenizer,
)

print("Trainer configure avec CrossEntropy ponderee")

# %% [markdown]
# ### 6️⃣ Entraînement

# %%
print(f"\nDebut de l'entrainement BERT ({TASK})...")
train_result = trainer.train()

trainer.save_model(str(OUTPUT_DIR / "final"))
tokenizer.save_pretrained(str(OUTPUT_DIR / "final"))

print(f"\nEntrainement termine !")
print(f"  Loss finale : {train_result.training_loss:.4f}")

# %% [markdown]
# ### 7️⃣ Évaluation finale sur le test set + Classification Report

# %%
print(f"\nEvaluation sur le test set ({len(test_ds)} exemples)...")
predictions = trainer.predict(test_ds)

pred_labels = np.argmax(predictions.predictions, axis=-1)
true_labels = predictions.label_ids

# Métriques globales
acc = accuracy_score(true_labels, pred_labels)
f1_m = f1_score(true_labels, pred_labels, average="macro", zero_division=0)
f1_w = f1_score(true_labels, pred_labels, average="weighted", zero_division=0)

print(f"\n{'='*50}")
print(f"  RESULTATS TEST — {TASK}")
print(f"{'='*50}")
print(f"  Accuracy     : {acc:.4f}")
print(f"  F1 Macro     : {f1_m:.4f}")
print(f"  F1 Weighted  : {f1_w:.4f}")

# Classification report détaillé
target_names = [id2label[i] for i in range(num_labels)]
report = classification_report(
    true_labels, pred_labels,
    target_names=target_names,
    zero_division=0,
)
print(f"\n{report}")

# Sauvegarder le rapport
report_path = OUTPUT_DIR / "classification_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"Task: {TASK}\n")
    f.write(f"Model: {MODEL_ID}\n")
    f.write(f"Accuracy: {acc:.4f}\n")
    f.write(f"F1 Macro: {f1_m:.4f}\n")
    f.write(f"F1 Weighted: {f1_w:.4f}\n\n")
    f.write(report)

print(f"Rapport sauvegarde : {report_path}")
print(f"Modele sauvegarde  : {OUTPUT_DIR / 'final'}")
print(f"\nPipeline BERT baseline termine pour la tache '{TASK}' !")
print(f"Pour la 2eme tache, changez TASK = 'urgency_human' et relancez.")
