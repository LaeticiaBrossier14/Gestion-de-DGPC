# 🎯 INSTRUCTIONS - Pipeline Appels 506+

## 📍 Résumé (LIRE D'ABORD!)

Vous avez maintenant un **pipeline complet** pour:
1. ✅ Transcrire les appels 506+ (audio Kabyle)
2. ✅ Créer un dataset structuré
3. ✅ Annoter automatiquement avec l'IA

**Démarrage:** Double-cliquer sur `LancerMenu.bat` 👈

---

## ⭐ 3 FAÇONS DE DÉMARRER

### Option 1️⃣ Menu Interactif (RECOMMANDÉ)
```
➊ Double-cliquer: LancerMenu.bat
➋ Choisir option dans le menu
➌ Suivre les instructions
```
✅ **Conseil:** Si vous ne savez pas par où commencer, c'est l'option à choisir!

### Option 2️⃣ Transcription Directe (Whisper)
```
➊ Double-cliquer: run_transcription_506.bat
➋ Attendre transcription
➌ Outil d'annotation se lance automatiquement
```
⏱️ Temps: 2-3h pour 304 appels (avec GPU)

### Option 3️⃣ Vérification d'abord (Recommandé si nouveau)
```
➊ Double-cliquer: check_health.bat
➋ Vérifier que tout est vert (✅)
➌ Si OK → Lancer LancerMenu.bat
```

---

## 🔧 AVANT DE COMMENCER: Checklist

- [ ] Python 3.8+ installé? (`python --version`)
- [ ] Audio présent? (Vérifier `audio_processed/appelle 506.wav` existe)
- [ ] GPU disponible? (Optionnel mais recommandé)
- [ ] Internet stable? (Télécharge modèles)

**Oublié quelque chose?** → Lancer: `check_health.bat`

---

## 🚀 ÉTAPES PRINCIPALES

### ÉTAPE 1: Choisir modèle de transcription

**Question:** Vous préférez?
- **A) Rapidité** → Choisir Whisper (5-10 sec par appel)
- **B) Qualité Kabyle** → Choisir Qwen3-ASR (10-15 sec par appel, mieux pour dialectes)

**Comment:**
```
1. Lancer: LancerMenu.bat
2. Choisir:
   - Option 1 = Whisper (rapide)
   - Option 2 = Qwen3-ASR (Kabyle optimisé)
```

### ÉTAPE 2: Attendre transcription

Le script:
```
✓ Cherche fichiers audio (appelle 506.wav, 507.wav, etc.)
✓ Télécharge le modèle (première fois = 2-4 GB)
✓ Transcrit chaque appel
✓ Crée CSV dans dataset/
```

**Indicateurs normaux:**
- ✅ "🎙️ Transcription: appelle 506.wav... ✓"
- ✅ "✅ Dataset sauvegardé"
- ❌ Si erreur: vérifier fichiers audio existent

### ÉTAPE 3: Lancer annotation

```
1. Menu principal
2. Option 3 = Lancer ANNOTATION
3. Navigateur ouvre: http://localhost:8501
4. Voir interface Streamlit
```

### ÉTAPE 4: Annoter les appels

Dans Streamlit:
```
- Écouter audio
- Voir transcription
- Remplir formule:
  ├─ Incident Type (medical_emergency, fire, etc.)
  ├─ Severity (low, medium, high)
  ├─ Location (city, address)
  └─ etc.
- Cliquer "Sauvegarder"
```

---

## 📊 Résultats

Après transcription, vous aurez dans `dataset/`:
```
✅ 506_onwards_transcriptions.csv
   Colonnes: ID, File, Transcription, incident_type, urgency, etc.
   Lignes: 304 (appels 506-809)
   Status: Prêt pour annotation
```

---

## ⚡ RACCOURCIS CLAVIER

| Commande | Effet |
|----------|--------|
| `CTRL+C` | Arrêter transcription (safe) |
| `CTRL+C` | Arrêter Streamlit |

---

## 🐛 PROBLÈMES COURANTS

### ❓ "ModuleNotFoundError: No module named 'whisper'"
**Solution:**
```bash
pip install openai-whisper
```
Ou relancer `check_health.bat` → il propose l'install automatique

### ❓ Transcription très lente (>30s par appel)
**Diagnostic:**
```
1. Vérifier GPU: check_health.bat → doit dire "GPU: ..."
2. Si pas de GPU → normal (CPU = 30s/appel)
3. Si GPU mais lent → vérifier drivers CUDA
```

### ❓ "Aucun fichier audio trouvé"
**Solution:**
```
1. Vérifier: C:\Users\warda\Desktop\dgpc_pipeline_ready\audio_processed\
2. Doit contenir: appelle 506.wav, appelle 507.wav, etc.
3. Si manquant → Copier fichiers audio dans ce dossier
4. Noms doivent contenir "506", "507", etc.
```

### ❓ Streamlit affiche page blanche
**Solution:**
```bash
streamlit cache clear
# Puis relancer
```

### ❓ GPU hors de mémoire (Out of Memory)
**Solution:**
```bash
# Option 1: Transcrire par petit batch
python transcribe_from_506.py --start 506 --end 520

# Option 2: Forcer CPU
python transcribe_from_506.py --start 506 --use-cpu
```

---

## 📖 DOCUMENTATION

| Fichier | Pour... |
|---------|---------|
| **TRANSCRIPTION_GUIDE_506.md** | Guide détaillé (options avancées) |
| **PIPELINE_506_README.md** | Vue d'ensemble du pipeline |
| **PIPELINES_SUMMARY.txt** | Résumé des fichiers créés |
| **INSTRUCTIONS.md** | Ce fichier (vous êtes ici!) |

---

## 🎯 WORKFLOWS RECOMMANDÉS

### Workflow 1: Le plus simple (sans en savoir plus)
```
LancerMenu.bat
  ↓
Choisir 1 ou 2 (transcription)
  ↓
Attendre (2-3h)
  ↓
Choisir 3 (annotation)
  ↓
Annoter dans Streamlit
```

### Workflow 2: Pour tester (5 appels d'abord)
```
python transcribe_from_506.py --start 506 --end 510
  ↓ (~30 sec)
cd annotation_app
streamlit run dgpc_annotation_local.py
  ↓
Tester / Vérifier résultats
  ↓
Si OK → Lancer pour appels 506-809
```

### Workflow 3: Batch production (automatisé)
```
check_health.bat ✓
  ↓
python transcribe_from_506.py --start 506
  ↓ (background)
Pendant ce temps: Autre travail
  ↓
Une fois fini: LancerMenu.bat → Option 3 (annotation)
```

---

## 🔐 NOTES DE SÉCURITÉ

- ✅ Les données restent locales (pas d'upload)
- ✅ API keys lues depuis `.env` (configure dans annotation_app/.env)
- ✅ Audit log dans dataset CSV (_annotation_status)
- ✅ Pas de suppression accidentelle (safe merge, backups)

---

## 📞 AIDE RAPIDE

**"Je veux juste tester"**
```bash
python transcribe_from_506.py --start 506 --end 510
```

**"Je veux la meilleure qualité Kabyle"**
```bash
python transcribe_qwen3_from_506.py --start 506
```

**"Je veux tout automatisé"**
```bash
double-cliquer: run_transcription_506.bat
```

**"Je ne sais pas par où commencer"**
```bash
double-cliquer: check_health.bat (vérifier)
double-cliquer: LancerMenu.bat (menu)
```

---

## ✅ SUCCESS CHECKLIST

À la fin, vous devriez avoir:
- [ ] ✅ 300+ appels transcrits
- [ ] ✅ CSV avec colonnes structurées
- [ ] ✅ Outil d'annotation qui marche
- [ ] ✅ Données prêtes pour ML/analyse

---

## 🎉 ET APRÈS?

Une fois terminée la phase appels 506+:
1. **Vérification:** Utiliser `verification_tool/`
2. **Génération synthétique:** Utiliser `augmentation/generate_synthetic.py`
3. **Fusion:** Combiner avec 500 appels existants
4. **Export:** Exporter en format final (JSON, Parquet, DB)

---

## 📞 QUESTIONS?

Consultez:
- `TRANSCRIPTION_GUIDE_506.md` → Options avancées
- `PIPELINE_506_README.md` → Architecture complète
- `annotation_app/README.md` → Interface d'annotation

---

**🚀 PRÊT À LANCER?**

```
👉 Double-cliquer: LancerMenu.bat
```

OU

```bash
python pipeline_menu.py
```

---

**Version:** 1.0  
**Date:** 4 Mars 2026  
**Status:** ✅ Prêt à l'emploi
