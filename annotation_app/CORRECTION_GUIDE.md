# 🔧 Guide de Réparation des Transcriptions Manquantes

## Résumé du Problème

6 appels ont des transcriptions vides dans votre base de données:
- **appelle 512.wav** - Urgence médicale (Béjaïa)
- **appelle 518.wav** - Urgence médicale (Béjaïa)
- **appelle 526.wav** - Urgence médicale (El Kseur)
- **appelle 533.wav** - Urgence médicale (Souk El-Ténine)
- **appelle 534.wav** - Autre/Non-urgence (El Kseur)
- **appelle 577.wav** - (Identifiée lors du scan)

## ✅ Corrections Appliquées

### 1. **Validation de la Transcription (FAIT)**
   - Modifié `dgpc_annotation_local.py`
   - Le champ "Transcription" est maintenant **obligatoire**
   - Message d'erreur s'affiche si tentative de sauvegarde sans transcription

### 2. **Marquage des Vides (FAIT)**
   - Les transcriptions manquantes sont identifiées et marquées
   - Fichiers JSON et CSV synchronisés
   - Les données d'extraction (location, summary, etc.) sont intactes

## 🚀 Étapes pour Compléter les Vraies Transcriptions

### Option 1: Via l'Application Streamlit (Recommandé)
```bash
# 1. Assurez-vous que l'application est en cours d'exécution
cd annotation_app
streamlit run dgpc_annotation_local.py

# 2. Naviguez jusqu'à "appelle 512.wav" via le sidebar
# 3. Cliquez sur "DÉMARRER ANALYSE IA"
#    (Assurez-vous que GEMINI_API_KEY est configurée)
# 4. La transcription sera générée par Gemini 3.0
# 5. Cliquez sur "APPROUVER ET ENREGISTRER LE DOSSIER"
```

### Option 2: Via le Script de Réparation
```bash
# 1. Créez un fichier .env
cd annotation_app
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 2. Exécutez le script de réparation
python fix_missing_transcriptions.py
```

## 📋 Comment Configurer Votre Clé API Gemini

### Étape 1: Obtenir une Clé API
1. Visitez: https://ai.google.dev/
2. Cliquez sur "Get API Key"
3. Connectez-vous avec votre compte Google
4. Créez une nouvelle clé API

### Étape 2: Configurer la Clé
**Option A: Fichier .env (Recommandé)**
```bash
# annotation_app/.env
GEMINI_API_KEY=your_api_key_here_sk_xxxxx
```

**Option B: Variable d'Environnement Windows**
```powershell
# PowerShell
$env:GEMINI_API_KEY = "your_api_key_here"

# Ou via les paramètres système Windows
# Paramètres > Système > Variables d'environnement
```

## 🔍 Vérification

Après correction, vérifiez que les transcriptions sont complètes:

```bash
# Vérifier le JSON
python -c "
import json
with open('dataset/annotations_local.json') as f:
    data = json.load(f)
    for entry in data:
        if 'appelle 512' in entry.get('audio_file', ''):
            transcript = entry.get('transcription', '(empty)')
            print(f'512: {len(transcript)} chars - {transcript[:100]}...')
"

# Ou ouvrir manuel avec Excel/VS Code
# dataset/annotations_local.csv
```

## ⚠️ Important

- **N'exposez pas votre clé API** sur Internet ou GitHub
- Utilisez `.env` et `.gitignore` pour protéger votre clé
- La clé Gemini gratuite a des limites de requêtes; attention à l'utilisation

## 📞 Support

**Problèmes courants:**

1. **"GEMINI_API_KEY not found"**
   - Vérifiez que le fichier `.env` existe
   - Vérifiez que la clé n'a pas d'espaces
   - Redémarrez l'application

2. **"Invalid API Key"**
   - Générez une nouvelle clé sur ai.google.dev
   - Utilisez la clé complète sans modifications

3. **Audio processing error**
   - Vérifiez que les fichiers `.wav` existent dans `audio_raw/`
   - Vérifiez que ffmpeg est installé (pydub dépend)

## 📊 Résultats Attendus

Après completion, chaque appel devrait avoir:
- ✅ `Transcription`: Texte verbatim en arabizi du dialecte Béjaoui
- ✅ `incident_type`: medical_emergency, fire_building, etc.
- ✅ `summary`: Résumé en français
- ✅ `notes_cot`: Raisonnement d'extraction
- ✅ `location_description`: Repères géographiques
