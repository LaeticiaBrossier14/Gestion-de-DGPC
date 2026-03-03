# 🤖 AGENT GUIDE — DGPC Pipeline

**À L'ATTENTION DE L'ASSISTANT IA (ChatGPT, Claude, Gemini, Cursor, etc.)**

Tu vas assister un développeur sur le projet **DGPC Pipeline** (Protection Civile Béjaïa).
Ce document contient tout le contexte et les règles dont tu as besoin pour l'aider efficacement.

---

## 🏗️ Architecture du Projet

Le dépôt est organisé en 4 applications distinctes et des données partagées.
**Ne modifie pas les chemins absolus ou relatifs sans en informer l'utilisateur.**

### 1. `verification_tool/` (Outil de Vérification)
- **Stack** : Flask (Python) + HTML/JS vanilla (UI premium sombre)
- **But** : Vérifier manuellement un dataset de 506 appels (écouter l'audio + corriger texte + modifier métadonnées).
- **Fichiers clés** : `server.py` (API et gestion de la progression), `index.html` (Interface riche).
- **Données** : Lit `dataset/500annotations_local.csv` et sauvegarde la progression dans `verification_tool/verification_progress.json`.
- **Audio** : Chargé depuis `verification_tool/audio/`.

### 2. `annotation_app/` (Application d'Annotation)
- **Stack** : Streamlit + Google Generative AI (Gemini)
- **But** : Ajouter automatiquement des métadonnées complexes (incident, gravité, entités) via IA sur les transcriptions brutes.
- **Fichier** : `dgpc_annotation_local.py`.

### 3. `augmentation/` (Génération Synthétique & Moteur)
- **Stack** : Bibliothèque Python avancée
- **But** : Générer des données synthétiques en reproduisant les patterns du Kabyle de Béjaïa via BPE (Byte Pair Encoding) et des règles linguistiques expertes.
- **Fichiers clés** : `generate_synthetic.py`, dossier `engine/` (corrector, assembler, etc.), configs expertes YAML (`kabyle_lexicon.yaml`, `kabyle_guard_rules.yaml`).

### 4. `data_collection_app/` (Outil de Collecte)
- **Stack** : HTML/JS statique servi via `serve_https.py` (Flask avec SSL)
- **But** : Enregistrer des audios réels lors d'exercices de simulation, connectés à un Google Apps Script.

### 5. Datasets (Partagés)
- `dataset/500annotations_local.csv` : Le dataset de référence.
- `ml_pipeline/dataset/enums.py` : La source de vérité absolue de l'ontologie (types d'incidents, gravité, dairas, etc.).

---

## 🛡️ Règles de Collaboration (Multi-Utilisateurs)

Le projet utilise GitHub (via Codespaces ou en local). Le risque majeur est le **conflit sur le fichier `verification_progress.json`** si plusieurs personnes vérifient les mêmes appels en même temps.

**Si l'utilisateur te demande de l'aide sur la vérification, rappelle-lui :**
1. De bien vérifier sa "plage d'appels" assignée (ex: "Tu fais 251 à 500").
2. De faire un `git pull` AVANT de commmencer pour récupérer la progression des autres.
3. De faire un `git add -A && git commit -m "..." && git push` IMMEDIATEMENT après la session.

---

## 🛠️ Stack Technique & Dépendances
- **Local Setup (Option 3)** : Le collaborateur va travailler localement sur sa machine.
- **`requirements.txt`** : Contient uniquement l'essentiel (Flask, Streamlit, etc.). **Pas de PyTorch/Transformers ici** (ces frameworks sont sur un autre pipe pour l'entrainement).
- **`.gitignore`** : Exclut les fichiers audio (`*.wav`), les tokens `.env`, et les environnements virtuels. **Il GARDE intentionnellement les fichiers `.csv`, `.json`, `.yaml` de configuration et de dataset pour qu'ils se synchronisent entre les membres de l'équipe.**

---

## 🚀 Lancement des Outils

**Toujours se placer à la racine du projet.**

**Prérequis (A faire une seule fois) :**
1. Cloner le repo : `git clone <URL_DU_REPO>`
2. Créer un environnement virtuel : `python -m venv .venv`
3. Activer l'environnement : `.venv\Scripts\activate` (Windows) ou `source .venv/bin/activate` (Mac/Linux)
4. Installer les dépendances : `pip install -r requirements.txt`
5. Créer un fichier `.env` basé sur `.env.template` (ajouter la clé API Gemini).

**Démarrage des apps :**
- **Vérification** : `python verification_tool/server.py` (Port 5000)
- **Annotation** : `streamlit run annotation_app/dgpc_annotation_local.py` (Port 8501)
- **Collecte** : `python data_collection_app/serve_https.py` (Port 5000 + HTTPS requis)

Si tu aides le développeur, respecte ces ports et n'essaie pas de réinstaller la stack entière si tu constates une erreur, regarde plutôt dans les fichiers `.py` pour débugger le code.
