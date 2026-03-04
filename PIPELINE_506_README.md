# 🚀 Pipeline Complet: Transcription 506+ → Annotation

## 📋 Vue d'ensemble

Ce pipeline fournit une solution **clé en main** pour:
- ✅ **Transcrire** les appels 506+ (audio → texte)
- ✅ **Enregistrer** dans un dataset structuré (CSV)
- ✅ **Annoter** automatiquement avec l'IA (Gemini + Correcteur Kabyle)
- ✅ **Vérifier** et corriger les données

---

## 🎯 Démarrage Rapide (3 clics)

### Option A: Menu Interactif (Recommandé)
```bash
Double-cliquer: LancerMenu.bat
```
Choose options dynamiquement

### Option B: Whisper (Rapide)
```bash
Double-cliquer: run_transcription_506.bat
```

### Option C: Qwen3-ASR (Kabyle optimisé)
```bash
Double-cliquer: run_qwen3_transcription_506.bat
```

---

## 📁 Fichiers du Pipeline

| Fichier | Fonction |
|---------|----------|
| **transcribe_from_506.py** | Transcription Whisper + Enregistrement dataset |
| **transcribe_qwen3_from_506.py** | Transcription Qwen3-ASR (alternative) |
| **pipeline_menu.py** | Menu interactif pour gérer le pipeline |
| **run_transcription_506.bat** | Lance Whisper avec auto-annotation |
| **run_qwen3_transcription_506.bat** | Lance Qwen3-ASR |
| **Lancer_Annotation_506.bat** | Lance l'outil d'annotation |
| **LancerMenu.bat** | Lance le menu principal |
| **TRANSCRIPTION_GUIDE_506.md** | Documentation détaillée |

---

## 🔄 Workflow Complet

```
1. RÉCUPÉRATION AUDIO
   ↓
   audio_processed/appelle 506.wav, 507.wav, ..., 809.wav
   
2. TRANSCRIPTION
   ↓
   Whisper OR Qwen3-ASR (choisissez selon vos besoins)
   
3. DATASET CSV
   ↓
   dataset/506_onwards_transcriptions.csv
   Colonnes: ID, File, Transcription, incident_type, urgency, etc.
   
4. ANNOTATION IA
   ↓
   Streamlit App → Gemini → Correcteur Kabyle
   Remplit: incident_type, location, severity, etc.
   
5. EXPORT
   ↓
   dataset/506_onwards_transcriptions_ANNOTATED.csv
```

---

## 🎙️ Comparaison Modèles

| Aspect | Whisper | Qwen3-ASR |
|--------|---------|-----------|
| **Vitesse** | ⚡ Rapide (5s/appel GPU) | 🐢 Lent (10s/appel GPU) |
| **Qualité générique** | ✅ Excellente | ✅ Bonne |
| **Qualité Kabyle** | ⚠️ Moyenne | ✅ Excellente |
| **Dépendances** | 🟢 Légères | 🔴 Lourdes |
| **GPU** | Optionnel | Recommandé |
| **Premier lancement** | 1-2 min | 3-5 min |

**Recommandation:**
- Pour Kabyle pur → **Qwen3-ASR**
- Pour texte mixte/français → **Whisper**
- Pas de GPU? → **Whisper + CPU**

---

## 🚀 Étapes Détaillées

### 1️⃣ Lancer la Transcription

#### Avec Menu (Recommandé)
```bash
python pipeline_menu.py
# Choisir option 1 ou 2
```

#### Ou directement en CLI
```bash
# Whisper
python transcribe_from_506.py --start 506 --end 520

# Qwen3-ASR
python transcribe_qwen3_from_506.py --start 506 --end 520 --use-cpu
```

### 2️⃣ Vérifier les Transcriptions
```bash
# Voir statistiques
python -c "import pandas as pd; df = pd.read_csv('dataset/506_onwards_transcriptions.csv'); print(f'Appels: {len(df)}'); print(df.head())"
```

### 3️⃣ Lancer l'Annotation
```bash
python pipeline_menu.py
# Choisir option 3
# OU
cd annotation_app
streamlit run dgpc_annotation_local.py
```

### 4️⃣ Exporter Résultats
```bash
# Convertir en JSON
python -c "import pandas as pd; pd.read_csv('dataset/506_onwards_transcriptions.csv').to_json('506_data.json')"

# Convertir en Excel
python -c "import pandas as pd; pd.read_csv('dataset/506_onwards_transcriptions.csv').to_excel('506_data.xlsx')"
```

---

## ⚙️ Installation des Dépendances

### Automatique (via batch)
```bash
# Les fichiers .bat gèrent l'installation
Double-cliquer: run_transcription_506.bat
```

### Manuel
```bash
# Whisper
pip install openai-whisper

# Qwen3-ASR
pip install qwen-asr transformers torch torchaudio

# Annotation & Tools
pip install streamlit google-generativeai pandas python-dotenv pydub
```

---

## 🐛 Dépannage

### ❓ "Module not found"
```bash
pip install -r requirements.txt
```

### ❓ Transcription très lente
- Vérifier GPU: `torch.cuda.is_available()` 
- Si False, installer CUDA drivers
- Utiliser `--use-cpu` (sacrifie la vitesse)

### ❓ Annotation blanche (Streamlit)
```bash
# Nettoyer le cache
streamlit cache clear
# Ou relancer
```

### ❓ Fichiers .wav non trouvés
- Vérifier: `C:\Users\warda\Desktop\dgpc_pipeline_ready\audio_processed\`
- Doit contenir: `appelle 506.wav`, `appelle 507.wav`, etc.

---

## 📊 Résultats Attendus

Après transcription, vous aurez:
```
dataset/
├── 506_onwards_transcriptions.csv      (Whisper)
├── 506_onwards_transcriptions_qwen3.csv (Qwen3-ASR)
└── 500annotations_local.csv            (Original 1-500)
```

Chaque CSV contient:
- **500+ lignes** (une par appel)
- **18 colonnes** (ID, transcription, metadata, annotation)
- **Format structuré** prêt pour ML/analyse

---

## 🎯 Cas d'Usage

### Cas 1: Transcription rapide d'une petite batch
```bash
python transcribe_from_506.py --start 506 --end 510
```
✅ 5 appels en ~30s

### Cas 2: Tout transcrire (506-809)
```bash
python transcribe_from_506.py --start 506
```
⏳ ~2h sur GPU

### Cas 3: Qualité Kabyle optimale
```bash
python transcribe_qwen3_from_506.py --start 506
```
✅ Meilleure transcription pour Kabyle

### Cas 4: Automatisation (cron/scheduled task)
```bash
# Windows Task Scheduler → python transcribe_from_506.py --start 506
# Linux crontab → 0 9 * * * python transcribe_from_506.py --start 506
```

---

## 📚 Documentation Complète

Voir: [TRANSCRIPTION_GUIDE_506.md](TRANSCRIPTION_GUIDE_506.md)

---

## 🔗 Intégration Existante

Ce pipeline s'intègre avec:
- ✅ `annotation_app/` - Annotation IA Streamlit
- ✅ `augmentation/` - Post-traitement et correction Kabyle
- ✅ `verification_tool/` - Vérification qualité dataset
- ✅ `dataset/` - Stockage centralisé

---

## 💡 Prochaines Étapes

1. ✅ **Transcription** → Créé ✓
2. ✅ **Annotation** → Existant ✓
3. 🔄 **Vérification** → Utiliser `verification_tool/`
4. 🔄 **Génération Synthétique** → Utiliser `augmentation/generate_synthetic.py`
5. 🔄 **Export & Analyse** → À venir

---

## 📞 Support & Questions

- **Whisper:** https://github.com/openai/whisper
- **Qwen3-ASR:** https://huggingface.co/Qwen/Qwen3-ASR-1.7B
- **Annotation:** Voir `annotation_app/README.md`
- **Vérification:** Voir `verification_tool/README.md`

---

## 📜 Licence & Attribution

Développé pour le projet DGPC (Protection Civile Béjaïa)
Données : Enregistrements d'appels d'urgence
Modèles : OpenAI (Whisper), Alibaba (Qwen3-ASR), Google (Gemini)

---

**Version:** 1.0  
**Date:** March 2026  
**Status:** ✅ Production Ready
