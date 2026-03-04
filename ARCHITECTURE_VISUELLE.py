"""
ARCHITECTURE VISUELLE - Pipeline DGPC 506+
============================================
"""

ARCHITECTURE = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                   🛡️  PIPELINE DGPC - ARCHITECTURE COMPLÈTE                   ║
╚════════════════════════════════════════════════════════════════════════════════╝

                            👤 UTILISATEUR
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
            🖱️ LancerMenu.bat  🖱️ .bat files  🖱️ check_health.bat
                    │             │             │
                    └─────────────┼─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            📜 pipeline_menu.py      check_health.py
            (menu interactif)        (vérification setup)
                    │                           │
         ┌──────────┼──────────┐               │
         │          │          │               │
         ↓          ↓          ↓               ↓
    ╔════════╗ ╔═══════════╗ ╔═══════╗  ✓ Python version
    ║ Option ║ ║  Option   ║ ║Option ║  ✓ Dépendances
    ║   1    ║ ║     2     ║ ║   3   ║  ✓ GPU/CPU
    ║Whisper ║ ║ Qwen3-ASR ║ ║Annotat║  ✓ Fichiers audio
    ╚════╬═══╝ ╚═════╬═════╝ ╚═══╬═══╝  ✓ Dataset CSV
         │            │            │
         ↓            ↓            ↓
 ┌──────────────┬──────────────┬────────────────────┐
 │              │              │                    │
 │ transcribe_  │ transcribe_  │ annotation_app/    │
 │ from_506.py  │ qwen3_from_  │ dgpc_annotation_   │
 │              │ 506.py       │ local.py (Streamlit)
 │ (Whisper)    │ (Qwen3-ASR)  │                    │
 │              │              │                    │
 └──────║───────┴──────║────────┴────────────║─────┘
        ║               ║                      ║
        └───────────────┼──────────────────────┘
                        ↓
        ╔══════════════════════════════════════╗
        ║       📥 AUDIO_PROCESSED/           ║
        ║  appelle 506.wav, 507.wav, ...809   ║
        ║          (304 fichiers)              ║
        ╚══════════════════════════════════════╝
                        │
             ┌──────────┼──────────┐
             │          │          │
        TRANSCRIPTION (GPU/CPU)    │
        ├─ Whisper (5s)          │
        ├─ Qwen3-ASR (10s)       │
        └─ Output: Texte         │
             │                    │
             ↓                    │
        ╔══════════════════════════════════════╗
        ║    📊 DATASET CREATION (CSV)        ║
        ║                                     ║
        ║  Colonnes:                          ║
        ║  ├─ ID (CALL_0506_Appe)            ║
        ║  ├─ File (appelle 506.wav)         ║
        ║  ├─ Transcription (texte)          ║
        ║  ├─ incident_type (empty)          ║
        ║  ├─ urgency (empty)                ║
        ║  ├─ location (empty)               ║
        ║  └─ ... (15 colonnes)              ║
        ╚══════════════════════════════════════╝
                        │
             ┌──────────┴──────────┐
             │                     │
    506_onwards_         506_onwards_
    transcriptions        transcriptions_
    .csv (Whisper)       qwen3.csv (Q3)
             │                     │
             └──────────┬──────────┘
                        ↓
        ╔══════════════════════════════════════╗
        ║  📝 ANNOTATION (Streamlit)           ║
        ║                                     ║
        ║  1. Charger CSV                     ║
        ║  2. Pour chaque appel:              ║
        ║     ├─ Afficher audio              ║
        ║     ├─ Afficher transcription      ║
        ║     ├─ Appel Gemini API            ║
        ║     ├─ Correcteur Kabyle           ║
        ║     ├─ Formulaire interactif       ║
        ║     └─ Sauvegarder résultat        ║
        ║  3. Exporter CSV annoté2            ║
        ╚══════════════════════════════════════╝
                        │
                        ↓
        ╔══════════════════════════════════════╗
        ║  ✅ RÉSULTAT FINAL                  ║
        ║                                     ║
        ║  506_onwards_transcriptions_        ║
        ║  FINAL.csv                          ║
        ║                                     ║
        ║  Contient:                          ║
        ║  ├─ 304 appels (506-809)           ║
        ║  ├─ Transcription Whisper/Q3       ║
        ║  ├─ Incident_type (médical, feu)  ║
        ║  ├─ Urgency (high, medium, low)   ║
        ║  ├─ Location (daira, commune)      ║
        ║  ├─ Victims, fire, weapons, etc.   ║
        ║  └─ AI-generated summary           ║
        ╚══════════════════════════════════════╝
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ↓               ↓               ↓
    📊 ANALYZE      🔍 VERIFY        🤖 AUGMENT
    (Python)       (Flask UI)       (Synthétique)
    ├─ Stats        ├─ Geo-locate  ├─ TTS
    ├─ Graphs       ├─ Audio check ├─ Mix
    └─ Export       └─ Correct     └─ JSON
        │               │               │
        └───────────────┼───────────────┘
                        ↓
                🎯 ML TRAINING READY 🎯
"""

DATA_FLOW = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                        📊 FLUX DE DONNÉES COMPLET                             ║
╚════════════════════════════════════════════════════════════════════════════════╝

[ENTRÉE]
  └─ audio_processed/appelle 506.wav, 507.wav, ..., 809.wav (304 fichiers, MP3/WAV)

        │
        ├─ EXTRACTION NUMÉRO APPEL: CALL_0506_Appe → CALL_0809_Appe
        │
        ├─ TRANSCRIPTION VIA ASR
        │  ├─ Whisper (OpenAI): en-US + fr code-switched
        │  └─ Qwen3-ASR (Alibaba): Optimisé dialectes (Kabyle, Darija)
        │
        ├─ NORMALISATION TEXTE
        │  ├─ Minuscules: "APPEL" → "appel"
        │  ├─ Accents: "Béjaïa" → "Bejaïa"
        │  ├─ Espaces: "  " → " "
        │  └─ Caractères spéciaux
        │
        ├─ CRÉATION RECORD
        │  {
        │    ID: CALL_0506_Appe,
        │    File: appelle 506.wav,
        │    Transcription: "Allo, salam aleykoum...",
        │    incident_type: "" (à remplir),
        │    urgency_human: "" (à remplir),
        │    location: "" (à remplir),
        │    ... (18 colonnes)
        │    _annotation_status: "pending"
        │  }
        │
        ├─ SAFE MERGE (dedup par ID)
        │  └─ Ignore doublons, fusionne données existantes
        │
        ├─ ENREGISTREMENT CSV
        │  └─ dataset/506_onwards_transcriptions.csv

        │
        ├─ CHARGEMENT DANS STREAMLIT
        │
        ├─ ANNOTATION IA (Gemini)
        │  ├─ Entrée: Transcription (audio + texte)
        │  ├─ Appel API: "Extract incident type, location, severity"
        │  ├─ Output: JSON structuré
        │  └─ Cache: Évite rappels dupliqués
        │
        ├─ CORRECTION KABYLE
        │  ├─ Détecte Kabyle/Tamazight
        │  ├─ Applique lexique Kabyle personnalisé
        │  ├─ Corrige orthographe
        │  └─ Normalise translittération (Tifinagh/Latin)
        │
        ├─ ENRICHISSEMENT
        │  ├─ NER: Extraction noms, lieux, organisations
        │  ├─ Geo-localisation: Récupère coords lat/long
        │  ├─ Urgence: Score auto-calculé
        │  └─ Summary: Résumé CoT (Chain-of-Thought)
        │
        ├─ VALIDATION
        │  ├─ Vérification: All mandatory fields filled?
        │  ├─ Type check: Enum values valid?
        │  ├─ Length check: Text within limits?
        │  └─ Uniqueness: ID ne duplique pas existant?
        │
        ├─ ENREGISTREMENT CSV (annoté)
        │
        └─ EXPORT OPTIONS
           ├─ CSV (avec metadata)
           ├─ JSON (nested, easy to parse)
           ├─ Parquet (compressé, pour ML)
           ├─ SQLite (queryable)
           └─ API REST (accessible)

[SORTIE]
  ├─ 506_onwards_transcriptions_FINAL.csv (304 lignes, 18 colonnes)
  ├─ 506_onwards_data.json
  ├─ 506_onwards_data.parquet
  └─ Ready for ML training 🚀
"""

FILES_CREATED = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                        📁 FICHIERS CRÉÉS (COMPLET)                            ║
╚════════════════════════════════════════════════════════════════════════════════╝

📂 ROOT FOLDER
│
├── 🟢 SCRIPTS PYTHON (exécutables)
│   ├─ transcribe_from_506.py (~300 lines)
│   │  └─ Fonction: Transcription Whisper + enregistrement CSV
│   │
│   ├─ transcribe_qwen3_from_506.py (~300 lines)
│   │  └─ Fonction: Transcription Qwen3-ASR (meilleur Kabyle)
│   │
│   ├─ pipeline_menu.py (~380 lines)
│   │  └─ Fonction: Menu interactif central
│   │
│   └─ check_health.py (~250 lines)
│      └─ Fonction: Vérification setup (GPU, dépendances, fichiers)
│
├── 🟡 FICHIERS BATCH (double-cliquer)
│   ├─ LancerMenu.bat
│   │  └─ Lance: python pipeline_menu.py
│   │
│   ├─ run_transcription_506.bat
│   │  └─ Lance: python transcribe_from_506.py --auto-launch
│   │
│   ├─ run_qwen3_transcription_506.bat
│   │  └─ Lance: python transcribe_qwen3_from_506.py
│   │
│   ├─ Lancer_Annotation_506.bat
│   │  └─ Lance: streamlit run annotation_app/dgpc_annotation_local.py
│   │
│   └─ check_health.bat
│      └─ Lance: python check_health.py
│
├── 📖 DOCUMENTATION (markdown)
│   ├─ INSTRUCTIONS.md (LIRE D'ABORD!)
│   │  ├─ Guide pas-à-pas
│   │  ├─ Troubleshooting
│   │  └─ Quick start
│   │
│   ├─ TRANSCRIPTION_GUIDE_506.md
│   │  ├─ Options avancées
│   │  ├─ Configuration
│   │  └─ Exemples d'usage
│   │
│   ├─ PIPELINE_506_README.md
│   │  ├─ Vue d'ensemble
│   │  ├─ Architecture
│   │  └─ Intégration existante
│   │
│   └─ PIPELINES_SUMMARY.txt
│      ├─ Synthèse fichiers créés
│      ├─ Features
│      └─ Points forts/faibles
│
├── 📋 ARCHITECTURES & REFERENCES
│   ├─ ARCHITECTURE_VISUELLE.txt (ce fichier)
│   └─ CE_QUI_A_ETE_CREE.md
│
├── 📁 DOSSIERS EXISTANTS
│   ├─ audio_processed/
│   │  └─ appelle 506.wav → appelle 809.wav (304 fichiers)
│   │
│   ├─ dataset/
│   │  ├─ 500annotations_local.csv (original, 1-500)
│   │  ├─ 506_onwards_transcriptions.csv ← NOUVEAU (Whisper)
│   │  └─ 506_onwards_transcriptions_qwen3.csv ← NOUVEAU (Qwen3)
│   │
│   └─ annotation_app/
│      └─ dgpc_annotation_local.py (existant)
│
└── ✅ RÉSULTAT FINAL (après tout)
   ├─ dataset/506_onwards_transcriptions_FINAL.csv
   │  └─ 304 appels { ID, Transcription, incident_type, urgency, location, ... }
   │
   └─ Prêt pour:
      ├─ Machine Learning (training)
      ├─ Analyse statistique (Python/Pandas)
      ├─ Visualisation (Dashboards)
      ├─ Export (JSON, Parquet, DB)
      └─ Production deployment 🚀

═════════════════════════════════════════════════════════════════════════════════
"""

def show_architecture():
    print(ARCHITECTURE)
    print("\n")
    print(DATA_FLOW)
    print("\n")
    print(FILES_CREATED)

if __name__ == "__main__":
    show_architecture()
    print("\n" + "=" * 90)
    print("📊 ARCHITECTURE COMPLÈTE - v1.0")
    print("=" * 90)
    input("\nAppuyez sur Entrée pour fermer...\n")
