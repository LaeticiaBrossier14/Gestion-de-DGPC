# 🛡️ DGPC Annotation Tool

**Outil d'annotation pour la Protection Civile de Béjaïa**

## 🚀 Lancement

Double-cliquez sur **`Lancer_Annotation.bat`**

## 📁 Structure

```
annotation_app/
├── Lancer_Annotation.bat    ← Double-cliquez ici!
├── dgpc_annotation_local.py ← Code de l'application
├── audio_raw/               ← Déposez vos fichiers audio ici
├── audio_processed/         ← Conversions automatiques
└── dataset/
    ├── annotations_local.json
    └── annotations_local.csv
```

## 📋 Fonctionnalités

- 🤖 Analyse IA avec Gemini (transcription + extraction)
- 📅 Date et heure de l'appel
- 🏛️ Daïra (18 daïras de Béjaïa)
- 🗺️ GPS → Adresse (reverse geocoding)
- ✅ Suivi des fichiers traités
- 📊 Export CSV pour Excel

## 🔑 Configuration

1. Obtenez une clé API Gemini: https://ai.google.dev/
2. Entrez-la dans la sidebar de l'application

## 📞 Workflow

1. Déposez vos fichiers audio dans `audio_raw/`
2. Lancez l'application
3. Cliquez "🤖 LANCER L'ANALYSE IA"
4. Corrigez si nécessaire
5. Cliquez "💾 ENREGISTRER & SUIVANT"
