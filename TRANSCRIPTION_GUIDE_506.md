# 🎯 Pipeline Transcription Appels 506+ → Annotation

## 🚀 Démarrage rapide

### Option 1: Whisper (Rapide, GPU/CPU)
```bash
python transcribe_from_506.py --start 506 --auto-launch
```
Ou double-cliquer: `run_transcription_506.bat`

### Option 2: Qwen3-ASR (Mieux pour Kabyle, nécessite GPU)
```bash
python transcribe_qwen3_from_506.py --start 506
```
Ou double-cliquer: `run_qwen3_transcription_506.bat`

---

## 📊 Workflow Complet

```
1. TRANSCRIPTION
   ├─ Cherche: audio_processed/appelle 506.wav, 507.wav, etc.
   ├─ Transcrit: Whisper ou Qwen3-ASR
   └─ Enregistre: dataset/506_onwards_transcriptions.csv
   
2. DATASET
   └─ Crée CSV avec colonnes: ID, File, Transcription, incident_type, etc.
   
3. ANNOTATION (Streamlit)
   ├─ Lance: annotation_app/dgpc_annotation_local.py
   ├─ Ouvre: http://localhost:8501
   └─ Remplir: incident_type, urgency, localisation, etc. avec IA
```

---

## 🔧 Options Avancées

### Transcription d'une plage spécifique
```bash
python transcribe_from_506.py --start 506 --end 510
```

### Lancer sans auto-annotation
```bash
python transcribe_from_506.py --start 506
```

### Forcer CPU (Qwen3-ASR)
```bash
python transcribe_qwen3_from_506.py --use-cpu
```

---

## 📁 Fichiers Créés

| Fichier | Contenu |
|---------|---------|
| `506_onwards_transcriptions.csv` | Données des appels 506+ (Whisper) |
| `506_onwards_transcriptions_qwen3.csv` | Données des appels 506+ (Qwen3-ASR) |

### Colonnes du Dataset
```
ID                    → Identifiant unique (CALL_0506_Appe)
File                  → Nom du fichier audio
Transcription         → Texte transcrit
incident_type         → Type d'incident (medical_emergency, fire, etc.)
injury_severity       → Sévérité (minor, moderate, severe)
victims_count         → Nombre de victimes
fire_present          → Feu présent? (yes/no)
trapped_persons       → Personnes piégées? (yes/no)
weapons_involved      → Armes? (yes/no)
hazmat_involved       → Matières dangereuses? (yes/no)
intent                → Intention de l'appel (request_help, report_incident, etc.)
urgency_human         → Urgence perçue (high, medium, low)
daira                 → Circonscription (Béjaïa, Seddouk, etc.)
commune               → Commune
lieu                  → Type de lieu (Home, Street, Hospital, etc.)
location_description  → Description du lieu
summary               → Résumé de l'incident
notes_cot             → Notes Chain-of-Thought (résonning)
_annotation_status    → Statut (pending, annotated, verified)
```

---

## ⚙️ Requirements

### Whisper
```bash
pip install openai-whisper google-generativeai python-dotenv streamlit --quiet
```

### Qwen3-ASR
```bash
pip install qwen-asr transformers torch torchaudio numpy --quiet
```

> **GPU recommandé** pour Qwen3-ASR (sinon 30+ secondes par appel)

---

## 🐛 Dépannage

### Problème: "ModuleNotFoundError: No module named 'whisper'"
```bash
pip install openai-whisper
```

### Problème: Transcription très lente
- Vérifier GPU: `python -c "import torch; print(torch.cuda.is_available())"`
- Si False: installer CUDA drivers, ou utiliser `--use-cpu`

### Problème: "CALL_0506 already exists"
- Les enregistrements en double seront ignorés (safe merge)
- Vous pouvez relancer sans risque

---

## 🎯 Après la Transcription

### 1️⃣ Vérifier les données
```bash
# Ouvrir le dataset
python -c "import pandas as pd; df = pd.read_csv('dataset/506_onwards_transcriptions.csv'); print(df.head()); print(f'\\nTotal: {len(df)} appels')"
```

### 2️⃣ Lancer l'outil d'annotation
```bash
cd annotation_app
streamlit run dgpc_annotation_local.py
```

### 3️⃣ Alternative: Batch annotation
```bash
python annotation_app/dgpc_annotation_local.py --batch
```

---

## 📝 Modèles Disponibles

| Modèle | Pros | Cons | Temps/appel |
|--------|------|------|------------|
| **Whisper (base)** | Rapide, simple | Générique | ~5s GPU |
| **Qwen3-ASR** | Optimisé Kabyle | Lourd (~8GB RAM) | ~10s GPU |

---

## 🔗 Intégration Continue

Pour automatiser chaque jour:
```bash
# Windows Task Scheduler
# Créer une tâche: python transcribe_from_506.py --start 506
```

---

## 📞 Support

- **Questions Whisper?** → https://github.com/openai/whisper
- **Questions Qwen3?** → https://huggingface.co/Qwen/Qwen3-ASR-1.7B
- **Annotation? ** → Voir `annotation_app/README.md`

