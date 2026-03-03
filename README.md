# 🛡️ DGPC Pipeline — Gestion des Appels d'Urgence

Pipeline complet pour la gestion, transcription et annotation des appels téléphoniques d'urgence de la Protection Civile de Béjaïa (DGPC).

## 📦 Composants

| App | Dossier | Lancement | Description |
|-----|---------|-----------|-------------|
| 🎙️ **Collecte** | `data_collection_app/` | `python serve_https.py` | App web pour collecter des enregistrements de simulation |
| 📝 **Annotation** | `annotation_app/` | `streamlit run dgpc_annotation_local.py` | Annotation IA des transcriptions (Gemini + correcteur Kabyle) |
| ✅ **Vérification** | `verification_tool/` | `python server.py` | Vérification qualité des transcriptions du dataset 500 |
| 🤖 **Génération** | `augmentation/` | `python generate_synthetic.py --plan ...` | Génération synthétique de données d'entraînement |

## 🚀 Setup rapide

### Option 1 : Codespaces (recommandé)
1. Cliquer sur **Code → Codespaces → Create codespace**
2. Attendre l'installation automatique
3. Lancer l'app voulue (voir tableau ci-dessus)

### Option 2 : Local
```bash
git clone https://github.com/VOTRE_USER/dgpc-pipeline.git
cd dgpc-pipeline
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.template .env    # Ajouter votre clé API Gemini
```

## 🎧 Fichiers audio

Les fichiers audio ne sont **pas dans le repo** (trop gros). Copiez-les dans :
- `annotation_app/audio_raw/` → pour l'annotation
- `verification_tool/audio/` → pour la vérification

## 👥 Workflow collaboratif

### Règles d'or
1. **`git pull`** avant de commencer
2. **`git push`** dès que vous finissez une session
3. **Répartissez-vous les appels** : ex. Rayan 1→250, Ami 251→500

### Commandes quotidiennes
```bash
git pull                          # Récupérer le travail des autres
# ... travailler ...
git add -A
git commit -m "Vérifié appels 1-50"
git push
```

## 🔑 Clé API Gemini

Créer un fichier `.env` à la racine :
```
GEMINI_API_KEY=votre_clé_ici
```

> ⚠️ Ne JAMAIS commit le fichier `.env` (il est dans `.gitignore`)

## 📁 Structure

```
├── data_collection_app/    # App de collecte audio
├── annotation_app/         # Annotation Streamlit + IA
├── verification_tool/      # Vérification qualité transcription
├── augmentation/           # Génération synthétique + moteur Kabyle
│   ├── engine/             # Correcteur, assembleur, morphologie
│   ├── config/             # Géographie, règles, templates YAML
│   ├── *.yaml              # Lexiques et glossaires
│   └── generate_synthetic.py
├── dataset/                # Datasets partagés (CSV, JSON)
└── ml_pipeline/dataset/    # Enums, tâches de génération, données synthétiques
```
