# %% [markdown]
# # 00 — Préparation du Manifest ASR
# **Pipeline DGPC Béjaïa — PFE Master Data Science**
#
# Ce script prend le fichier `segments_asr_ready.jsonl` (produit par l'alignement forcé MMS)
# et produit des manifests propres `train.jsonl`, `validation.jsonl`, `test.jsonl`
# prêts pour construire un Dataset HuggingFace.
#
# **Étapes :**
# 1. Monter Drive (si Colab)
# 2. Charger les segments
# 3. Vérifier l'existence des fichiers audio
# 4. Nettoyer le texte (sans détruire l'Arabizi !)
# 5. Filtrer par durée et qualité
# 6. Split reproductible (seed=42)
# 7. Exporter + statistiques

# %% [markdown]
# ### 🔧 Configuration Centralisée
# Modifie ces chemins selon ton environnement (Colab ou local Windows).

# %%
import os
import sys
import json
import re
import random
from pathlib import Path
from collections import Counter

# ─── CONFIGURATION ───────────────────────────────────────────────────────────
# Détection automatique Colab vs Local
IS_COLAB = "google.colab" in sys.modules if hasattr(sys, "modules") else False

if IS_COLAB:
    from google.colab import drive
    drive.mount("/content/drive")
    DRIVE_ROOT = Path("/content/drive/MyDrive")
else:
    # En local Windows, pointe vers ton dossier projet
    DRIVE_ROOT = Path("f:/dgpc_pipeline_ready")

# Chemins des données source
SEGMENTS_JSONL = DRIVE_ROOT / "Pretraitement" / "partage_memoire" / "segments_asr_ready.jsonl"
AUDIO_BASE_DIR = DRIVE_ROOT / "Pretraitement" / "asr_dataset" / "wavs_16k"

# Dossier de sortie pour les manifests
OUTPUT_DIR = DRIVE_ROOT / "Training" / "manifests"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Paramètres de filtrage
MIN_DURATION = 1.0       # Segments < 1s = trop courts (bruits)
MAX_DURATION = 30.0      # Limitation architecturale Whisper
QUALITY_KEEP = {"gold", "silver"}  # On exclut "reject"
SPLIT_SEED = 42          # Reproductibilité absolue
SPLIT_RATIOS = (0.8, 0.1, 0.1)  # train / validation / test

print(f"📂 DRIVE_ROOT       : {DRIVE_ROOT}")
print(f"📂 SEGMENTS_JSONL   : {SEGMENTS_JSONL}")
print(f"📂 AUDIO_BASE_DIR   : {AUDIO_BASE_DIR}")
print(f"📂 OUTPUT_DIR       : {OUTPUT_DIR}")

# %% [markdown]
# ### 1️⃣ Chargement des segments bruts

# %%
def load_segments(jsonl_path):
    """Charge le fichier JSONL produit par l'alignement forcé."""
    segments = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                seg = json.loads(line)
                seg["_line"] = line_num
                segments.append(seg)
            except json.JSONDecodeError as e:
                print(f"  ⚠️  Ligne {line_num} invalide : {e}")
    return segments

raw_segments = load_segments(SEGMENTS_JSONL)
print(f"\n✅ {len(raw_segments)} segments chargés depuis {SEGMENTS_JSONL.name}")

# %% [markdown]
# ### 2️⃣ Résolution et vérification des chemins audio
# Les chemins dans le JSONL pointent vers `/content/aligned_segments/wavs/...`
# (chemins Colab). On les résout vers le vrai dossier audio local ou Drive.

# %%
def resolve_audio_path(original_path, audio_base_dir):
    """
    Transforme un chemin Colab absolu en chemin local.
    Ex: '/content/aligned_segments/wavs/Appelle 1_c003.wav'
     -> 'f:/dgpc_pipeline_ready/.../wavs_16k/Appelle 1_c003.wav'
    """
    filename = Path(original_path).name
    resolved = audio_base_dir / filename
    return resolved

stats_audio = Counter()
valid_segments = []

for seg in raw_segments:
    audio_path = resolve_audio_path(seg["audio"], AUDIO_BASE_DIR)
    
    if audio_path.exists():
        seg["audio_resolved"] = str(audio_path)
        valid_segments.append(seg)
        stats_audio["found"] += 1
    else:
        # Essayer aussi sans le suffixe _cXXX (audio original complet)
        call_name = seg.get("call_file", "")
        alt_path = AUDIO_BASE_DIR / f"{call_name}.wav"
        if alt_path.exists():
            seg["audio_resolved"] = str(alt_path)
            valid_segments.append(seg)
            stats_audio["found_alt"] += 1
        else:
            stats_audio["missing"] += 1

print(f"\n📊 Résolution audio :")
print(f"   ✅ Trouvés direct  : {stats_audio['found']}")
print(f"   ✅ Trouvés (alt)   : {stats_audio['found_alt']}")
print(f"   ❌ Manquants       : {stats_audio['missing']}")
print(f"   Total valides     : {len(valid_segments)}")

# %% [markdown]
# ### 3️⃣ Nettoyage du texte (Conservateur — On préserve l'Arabizi !)
# **IMPORTANT** : On ne touche PAS aux chiffres 3, 7, 9, 5 quand ils sont
# utilisés comme lettres Arabizi (3likoum, 7imaya, etc.).
# On nettoie uniquement la ponctuation excessive et les espaces.

# %%
def clean_text_for_asr(text):
    """
    Nettoyage conservateur du texte pour l'entraînement ASR.
    Préserve : Arabizi (3, 7, 9, 5), mots français, mots kabyles.
    Supprime : ponctuation excessive, labels de locuteurs, espaces multiples.
    """
    t = text.strip()
    
    # Supprimer les labels de locuteurs (Caller:, Operator:, P:, C:, etc.)
    t = re.sub(
        r'(?:Caller|Operator|Appelant|Repondant|Op|Cal|S1|S2|R|B|P|C|A|F|M)\s*:\s*',
        ' ', t, flags=re.IGNORECASE
    )
    
    # Supprimer les tirets longs (em-dash) utilisés comme séparateurs de tours
    t = t.replace('\u2014', ' ').replace('\u2013', ' ')
    
    # Garder les apostrophes (l'7imaya, d'accord) mais retirer la ponctuation lourde
    t = re.sub(r'[,;:!?\[\]{}«»""\u2026_*#@&%$^~`()\.]', ' ', t)
    
    # Normaliser les tirets simples entre mots (wa3likoum-salam -> wa3likoum salam)
    t = re.sub(r'(?<=\w)-(?=\w)', ' ', t)
    
    # Normaliser les espaces
    t = re.sub(r'\s+', ' ', t).strip()
    
    # Mettre en minuscules (Whisper fonctionne mieux en lowercase)
    t = t.lower()
    
    return t

# Test rapide sur un exemple réel
test_text = "Caller: ma3lishe, wich9a ma tzemrem ad t deplacim? Operator: Anda a Madame?"
cleaned = clean_text_for_asr(test_text)
print(f"  IN  : {test_text}")
print(f"  OUT : {cleaned}")
print()

# Appliquer le nettoyage
for seg in valid_segments:
    seg["text_clean"] = clean_text_for_asr(seg["text"])

print(f"✅ Texte nettoyé pour {len(valid_segments)} segments")

# %% [markdown]
# ### 4️⃣ Filtrage par durée et qualité

# %%
stats_filter = Counter()
filtered_segments = []

for seg in valid_segments:
    dur = seg.get("duration", 0)
    quality = seg.get("quality", "unknown")
    text = seg.get("text_clean", "")
    
    # Filtre durée
    if dur < MIN_DURATION:
        stats_filter["too_short"] += 1
        continue
    if dur > MAX_DURATION:
        stats_filter["too_long"] += 1
        continue
    
    # Filtre qualité
    if quality not in QUALITY_KEEP:
        stats_filter["rejected_quality"] += 1
        continue
    
    # Filtre texte vide
    if len(text.split()) < 2:
        stats_filter["too_few_words"] += 1
        continue
    
    stats_filter["kept"] += 1
    stats_filter[f"quality_{quality}"] += 1
    filtered_segments.append(seg)

print(f"\n📊 Filtrage :")
for k, v in sorted(stats_filter.items()):
    print(f"   {k:25s}: {v}")
print(f"\n   ✅ Segments retenus : {len(filtered_segments)}")

total_hours = sum(s["duration"] for s in filtered_segments) / 3600
print(f"   ⏱️  Durée totale    : {total_hours:.2f} heures")

# %% [markdown]
# ### 5️⃣ Split Train / Validation / Test (reproductible)

# %%
def split_dataset(segments, ratios, seed):
    """Split reproductible avec shuffle déterministe."""
    random.seed(seed)
    indices = list(range(len(segments)))
    random.shuffle(indices)
    
    n = len(segments)
    n_train = int(n * ratios[0])
    n_val = int(n * ratios[1])
    
    train_idx = indices[:n_train]
    val_idx = indices[n_train:n_train + n_val]
    test_idx = indices[n_train + n_val:]
    
    train = [segments[i] for i in train_idx]
    val = [segments[i] for i in val_idx]
    test = [segments[i] for i in test_idx]
    
    return train, val, test

train_segs, val_segs, test_segs = split_dataset(
    filtered_segments, SPLIT_RATIOS, SPLIT_SEED
)

print(f"\n📊 Split (seed={SPLIT_SEED}) :")
for name, segs in [("train", train_segs), ("val", val_segs), ("test", test_segs)]:
    dur = sum(s["duration"] for s in segs) / 3600
    gold = sum(1 for s in segs if s.get("quality") == "gold")
    silver = sum(1 for s in segs if s.get("quality") == "silver")
    print(f"   {name:12s}: {len(segs):5d} segments | {dur:.2f}h | gold={gold} silver={silver}")

# %% [markdown]
# ### 6️⃣ Export des manifests JSONL

# %%
def export_manifest(segments, output_path):
    """Exporte un manifest JSONL propre avec les champs nécessaires."""
    with open(output_path, "w", encoding="utf-8") as f:
        for seg in segments:
            entry = {
                "audio_path": seg["audio_resolved"],
                "text": seg["text_clean"],
                "duration": round(seg["duration"], 3),
                "quality": seg.get("quality", "unknown"),
                "call_file": seg.get("call_file", "unknown"),
                "source": "donnee_reel"
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return output_path

for name, segs in [("train", train_segs), ("validation", val_segs), ("test", test_segs)]:
    path = export_manifest(segs, OUTPUT_DIR / f"{name}.jsonl")
    print(f"💾 {name:12s} -> {path.name} ({len(segs)} segments)")

# %% [markdown]
# ### 7️⃣ Statistiques finales

# %%
print("\n" + "=" * 60)
print("📊 RÉSUMÉ FINAL DU MANIFEST ASR")
print("=" * 60)

all_segs = train_segs + val_segs + test_segs
total_dur = sum(s["duration"] for s in all_segs)
avg_dur = total_dur / len(all_segs) if all_segs else 0

# Distribution des durées
dur_bins = Counter()
for s in all_segs:
    d = s["duration"]
    if d < 3: dur_bins["< 3s"] += 1
    elif d < 5: dur_bins["3-5s"] += 1
    elif d < 10: dur_bins["5-10s"] += 1
    elif d < 15: dur_bins["10-15s"] += 1
    elif d < 20: dur_bins["15-20s"] += 1
    else: dur_bins["> 20s"] += 1

print(f"\n  Total segments      : {len(all_segs)}")
print(f"  Durée totale        : {total_dur/3600:.2f} heures")
print(f"  Durée moyenne       : {avg_dur:.1f}s")
print(f"\n  Distribution durées :")
for k in ["< 3s", "3-5s", "5-10s", "10-15s", "15-20s", "> 20s"]:
    v = dur_bins.get(k, 0)
    bar = "█" * (v // 5)
    print(f"    {k:8s}: {v:4d} {bar}")

# Exemples de texte nettoyé
print(f"\n  📝 Exemples de texte nettoyé :")
for seg in all_segs[:3]:
    txt = seg["text_clean"][:80]
    print(f"    [{seg.get('quality','?'):6s}] {txt}...")

print(f"\n✅ Manifests exportés dans : {OUTPUT_DIR}")
print("   Prochaine étape : exécuter 01_build_hf_asr_dataset.py")
