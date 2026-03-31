# %% [markdown]
# # 04 — Fine-Tuning Qwen 2.5 avec QLoRA pour l'Extraction Structurée
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script fine-tune `Qwen/Qwen2.5-7B-Instruct` avec QLoRA (4-bit)
# pour apprendre à extraire des informations structurées (JSON) depuis
# des transcriptions d'appels d'urgence en Arabizi.
#
# **GPU requis** : T4 (16GB VRAM minimum) ou A100.
# **Prérequis** : `pip install transformers datasets peft bitsandbytes trl accelerate`

# %% [markdown]
# ### Installation (cellule Colab)

# %%
# !pip install -q transformers datasets peft bitsandbytes trl accelerate

# %% [markdown]
# ### 🔧 Configuration

# %%
import os
import sys
import json
import torch
from pathlib import Path

IS_COLAB = "google.colab" in sys.modules if hasattr(sys, "modules") else False

if IS_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE_ROOT = Path("/content/drive/MyDrive")
else:
    DRIVE_ROOT = Path("f:/dgpc_pipeline_ready")

# Chemins
DATASET_DIR = DRIVE_ROOT / "Training" / "qwen_extraction_dataset"
OUTPUT_DIR = DRIVE_ROOT / "Training" / "qwen_finetuned"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Modele
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

# QLoRA
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
LORA_TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

# Entrainement
BATCH_SIZE = 4 if IS_COLAB else 1
GRADIENT_ACCUM = 4 if IS_COLAB else 1
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3 if IS_COLAB else 1
MAX_SEQ_LENGTH = 2048
MAX_STEPS_LOCAL = 3

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device     : {DEVICE}")
print(f"Model      : {MODEL_ID}")
print(f"LoRA rank  : {LORA_R}")

# %% [markdown]
# ### 1️⃣ Chargement du dataset

# %%
from datasets import Dataset

def load_jsonl(path):
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries

train_data = load_jsonl(DATASET_DIR / "train.jsonl")
val_data = load_jsonl(DATASET_DIR / "validation.jsonl")

train_ds = Dataset.from_list(train_data)
val_ds = Dataset.from_list(val_data)

print(f"Train : {len(train_ds)} exemples")
print(f"Val   : {len(val_ds)} exemples")

# %% [markdown]
# ### 2️⃣ Chargement du modèle en 4-bit (QLoRA)

# %%
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

print(f"Chargement de {MODEL_ID} en 4-bit...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)

print(f"Modele charge. Parametres : {sum(p.numel() for p in model.parameters()) / 1e9:.1f}B")

# %% [markdown]
# ### 3️⃣ Configuration LoRA (PEFT)

# %%
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training, TaskType

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    target_modules=LORA_TARGET_MODULES,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# %% [markdown]
# ### 4️⃣ Formatage des données pour SFTTrainer

# %%
def format_chat(example):
    """Formate les messages en texte ChatML pour le tokenizer Qwen."""
    messages = example["messages"]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    return {"text": text}

train_ds_formatted = train_ds.map(format_chat, remove_columns=train_ds.column_names)
val_ds_formatted = val_ds.map(format_chat, remove_columns=val_ds.column_names)

print(f"Exemple formate (extrait) :")
print(train_ds_formatted[0]["text"][:300] + "...")

# %% [markdown]
# ### 5️⃣ Entraînement avec SFTTrainer (TRL)

# %%
from trl import SFTTrainer, SFTConfig

sft_config = SFTConfig(
    output_dir=str(OUTPUT_DIR),
    
    num_train_epochs=NUM_EPOCHS,
    max_steps=MAX_STEPS_LOCAL if not IS_COLAB else -1,
    
    per_device_train_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=GRADIENT_ACCUM,
    
    learning_rate=LEARNING_RATE,
    warmup_ratio=0.03,
    weight_decay=0.01,
    
    fp16=torch.cuda.is_available(),
    
    logging_steps=10,
    save_strategy="steps",
    save_steps=200,
    save_total_limit=2,
    
    max_seq_length=MAX_SEQ_LENGTH,
    dataset_text_field="text",
    
    report_to="none",
    seed=42,
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=train_ds_formatted,
    eval_dataset=val_ds_formatted,
    processing_class=tokenizer,
)

print("Debut de l'entrainement Qwen + QLoRA...")
train_result = trainer.train()

# Sauvegarder l'adaptateur LoRA
model.save_pretrained(str(OUTPUT_DIR / "lora_adapter"))
tokenizer.save_pretrained(str(OUTPUT_DIR / "lora_adapter"))

print(f"\nEntrainement termine !")
print(f"  Loss finale  : {train_result.training_loss:.4f}")
print(f"  Adaptateur   : {OUTPUT_DIR / 'lora_adapter'}")

# %% [markdown]
# ### 6️⃣ Test d'inférence rapide

# %%
from transformers import pipeline

print("\nTest d'inference sur un exemple...")

test_data = load_jsonl(DATASET_DIR / "test.jsonl")
if test_data:
    test_ex = test_data[0]
    test_messages = test_ex["messages"][:2]  # system + user uniquement
    
    prompt = tokenizer.apply_chat_template(test_messages, tokenize=False, add_generation_prompt=True)
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.1)
    
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    
    print(f"Transcription (extrait) : {test_ex['messages'][1]['content'][:100]}...")
    print(f"\nPrediction du modele :")
    print(response[:500])
    
    # Comparer avec la reference
    print(f"\nReference :")
    print(test_ex["messages"][2]["content"][:500])

print(f"\nPipeline Qwen termine !")
