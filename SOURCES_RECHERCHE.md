# 📚 SOURCES & RÉFÉRENCES — Projet DGPC Pipeline

**Document de référence pour tous les collaborateurs du projet.**
Toutes les sources académiques, modèles, datasets, repos et documents utilisés dans ce projet.

---

## 📄 1. Papers Académiques (arXiv / Conférences)

### ASR & Code-Switching
| # | Titre | Auteurs | Source | Pertinence |
|---|-------|---------|--------|------------|
| 1 | **Leveraging Data Collection and Unsupervised Learning for Code-switched Tunisian Arabic ASR** | Ben Abdallah, Kabboudi, Kanoun, Zaiem | [arXiv:2309.11327](https://arxiv.org/abs/2309.11327) (2023) | wav2vec2.0 multilingue, self-supervised, SOTA Tunisian Arabic CS |
| 2 | **Leveraging LLM for Augmenting Textual Data in Code-Switching ASR: Arabic as an Example** | Alharbi, Binmuqbil, Ali et al. | ISCA SynData4GenAI (2024) | GPT-4 → génération phrases CS, Whisper, N-gram LM rescoring, -5.5% WER |
| 3 | **A Survey of Code-switched Arabic NLP: Progress, Challenges, and Future Directions** | Hamed, Sabty, Abdennadher, Vu, Solorio, Habash | [arXiv 2025 / ACL Anthology](https://aclanthology.org/) | Survey complet CS arabe Maghreb, LinCE, GLUECoS, gaps identifiés |
| 4 | **Whisper Multilingual Fine-tuning** (Swiss German) | — | [arXiv:2412.15726](https://arxiv.org/abs/2412.15726) | Stratégie fine-tuning dialecte + FLEURS |
| 5 | **Community-Powered Language Tech for Tamazight** | Öktem et al. | [arXiv:2510.27407](https://arxiv.org/abs/2510.27407) (2025) | Review NLP Tamazight, état des lieux complet |

### NLP Low-Resource & Information Extraction
| # | Titre | Source | Pertinence |
|---|-------|--------|------------|
| 6 | **NoLoR Framework** (4-step ASR low-resource) | [arXiv:2412.04717](https://arxiv.org/abs/2412.04717) | Neo-Aramaic, 6.3× speedup transcription |
| 7 | **DziriBERT** — Transformer pour l'Algérien | [arXiv:2109.12346](https://arxiv.org/abs/2109.12346) | SOTA sentiment analysis arabe algérien |
| 8 | **chDzDT** — Character-level morphology LM | [arXiv:2509.01772](https://arxiv.org/abs/2509.01772) | LM morphologique dialecte algérien |
| 9 | **Amharic ASR Fine-tuning** | [arXiv:2503.18485](https://arxiv.org/abs/2503.18485) | Langue agglutinative, FLEURS + local data mix |
| 10 | **Outlines** — Constrained Decoding for LLMs | [arXiv:2501.10868](https://arxiv.org/abs/2501.10868) | Extraction structurée JSON via grammaire |
| 11 | **APIE** — Active Prompting IE | [arXiv:2508.10036](https://arxiv.org/abs/2508.10036) | +3-5% F1 extraction entités |
| 12 | **QLoRA impact on Chain-of-Thought** | [arXiv:2411.15382](https://arxiv.org/abs/2411.15382) | Fine-tuning efficient, LoRA |

### ASR Avancé
| # | Titre | Source | Pertinence |
|---|-------|--------|------------|
| 13 | **Moonshine: Speech Recognition for Live Transcription** | [arXiv:2410.15608](https://arxiv.org/abs/2410.15608) | Alternative Whisper, edge, flexible input |
| 14 | **Flavors of Moonshine: Tiny Specialized ASR for Edge** | [arXiv:2509.02523](https://arxiv.org/abs/2509.02523) | Modèles mono-langue edge, Arabic inclus |
| 15 | **Moonshine Voice Streaming** | [arXiv:2602.12241](https://arxiv.org/abs/2602.12241) | Streaming ASR, beat Whisper Large V3 |

---

## 🤖 2. Modèles IA (HuggingFace / APIs)

### ASR (Speech-to-Text)
| Modèle | Architecture | Dataset | Lien |
|--------|-------------|---------|------|
| **openai/whisper-medium** | Whisper Medium | Multilingue | [HuggingFace](https://huggingface.co/openai/whisper-medium) |
| **openai/whisper-large-v3** | Whisper Large V3 | Multilingue | [HuggingFace](https://huggingface.co/openai/whisper-large-v3) |
| **facebook/mms-1b-all** | Meta MMS | 1162 langues dont Kabyle | [HuggingFace](https://huggingface.co/facebook/mms-1b-all) |
| **facebook/mms-tts-kab** | MMS TTS VITS | Bible Kabyle | [HuggingFace](https://huggingface.co/facebook/mms-tts-kab) |
| **aioxlabs/dvoice-kabyle** | Wav2Vec2 + CTC | DVoice Kabyle | [HuggingFace](https://huggingface.co/aioxlabs/dvoice-kabyle) |
| **Akashpb13/Kabyle_xlsr** | Wav2Vec2 XLS-R 300M | Common Voice | [HuggingFace](https://huggingface.co/Akashpb13/Kabyle_xlsr) — **WER 31.9%** |
| **yasminekaced/whisper-small-kab** | Whisper Small fine-tuné | Kabyle dataset | [HuggingFace](https://huggingface.co/yasminekaced/whisper-small-kab) |
| **Qwen/Qwen2-Audio-7B** | Qwen2-Audio | Multimodal | [HuggingFace](https://huggingface.co/Qwen/Qwen2-Audio-7B) |
| **Qwen/Qwen2.5-Omni-7B** | Qwen2.5-Omni | Multimodal + LoRA | [HuggingFace](https://huggingface.co/Qwen/Qwen2.5-Omni-7B) |

### NLP / Extraction
| Modèle | Usage | Lien |
|--------|-------|------|
| **CAMeLBERT** | NER arabe dialectal | [HuggingFace camel-lab](https://huggingface.co/CAMeL-Lab) |
| **Google Gemini 2.0/2.5 Flash** | Transcription + extraction structurée | [API Google](https://ai.google.dev/) |
| **Moonshine Voice** | ASR edge temps réel | [moonshine.ai](https://moonshine.ai) |

---

## 📊 3. Datasets

| Dataset | Contenu | Taille | Source |
|---------|---------|--------|--------|
| **Mozilla Common Voice Kabyle** | Audio + transcriptions Kabyle | 600+ heures, ~90k train | [commonvoice.mozilla.org](https://commonvoice.mozilla.org/) |
| **FLEURS** | Benchmark multilingue | 102 langues | [HuggingFace](https://huggingface.co/datasets/google/fleurs) |
| **DVoice Kabyle** | Audio Kabyle pour SpeechBrain | — | [HuggingFace DVoice](https://huggingface.co/datasets/aioxlabs/dvoice_kabyle) |
| **LinCE Benchmark** | LID + NER code-switching | — | [ritual.uh.edu/lince](https://ritual.uh.edu/lince/) |
| **GLUECoS** | Benchmark NLP code-switching | — | [microsoft/GLUECoS](https://github.com/microsoft/GLUECoS) |
| **MGB-3 Challenge** | Dialectal Arabic speech | Multi-genre | Standard ASR dialectal |
| **kabyle_asr** | 46.9k rows de phrases Kabyle audio | 46.9k | HuggingFace |
| **aqvaylis/Kabyle_Speech_Recognition** | ASR Kabyle | 700k+ phrases | [HuggingFace](https://huggingface.co/spaces/aqvaylis/kabyle-speech-to-text) |

---

## 📁 4. Repos GitHub Étudiés (external_repo_audit/)

| Repo | Contenu | Pertinence |
|------|---------|------------|
| **aqvaylis/kabyle-speech-to-text** | ASR Kabyle avec démo HF | Référence directe |
| **asafu-art/deepspeech-kabyle** | DeepSpeech fine-tuné Kabyle | Baseline historique |
| **MohammedBelkacem/KabyleNLP** | NLP Kabyle (détection langue, corpus) | Corpus + outils linguistiques |
| **MohammedBelkacem/KabyleCorporaGenerator** | Générateur de corpus Kabyle | Données textuelles |
| **MohammedBelkacem/corpus-kab** | Corpus Kabyle brut | Données textuelles |
| **YazidIflis/KabyleNLP** | NLP Kabyle alternatif | Outils POS, morphologie |
| **YazidIflis/Corpus-Tifyar-YBO** | Corpus poésie Kabyle | Données textuelles littéraires |
| **VocabKabyle/VocabKabyle** | Vocabulaire Kabyle structuré | Lexique de référence |
| **FarZ1/Kabyle-Arab-Game** | Jeu d'apprentissage Kabyle | Interface gamification |
| **LibreLingo/KAB-from-FR** | Cours Kabyle depuis le français | Linguistique appliquée |
| **moonshine-ai/moonshine** | ASR edge ultra-rapide | Alternative Whisper pour production |
| **VectifyAI/PageIndex** | RAG pour documents PDF | Architecture RAG applicable |

---

## 📕 5. Thèses & Documents Académiques (PDF)

### Dans `dataset/`
| Document | Contenu |
|----------|---------|
| **Thèse ASSOU corrigée.pdf** | Thèse de référence principale sur le sujet |
| **base-de-données-kabyles — collectes-de-données-et-applications-synchronisation-texte-son.pdf** | Collecte de données Kabyle, synchronisation texte-son |
| **kabylie_dialectologie_knz.pdf** | Dialectologie de la Kabylie |
| **prosodie1-2.pdf** | Prosodie du Kabyle (intonation, rythme) |

### À la racine
| Document | Contenu |
|----------|---------|
| **Fiche-technique-du-système-gestion-des-lignes-14.pdf** | Fiche technique système téléphonique urgences |
| **les traveaux a préparé a la wilya d'instalation.pdf** | Travaux préparatoires wilaya |

---

## 🗣️ 6. Références Linguistiques Kabyle

### Travaux universitaires cités
| Auteur | Titre | Université | Année |
|--------|-------|------------|-------|
| **Guenane, N.** | Étude des variables linguistiques entre Tasahlit et le Kabyle de Tazmalt | Université de Béjaïa | 2022 |
| **Hani, H. et al.** | Tanfalit Tasnilsant N Tesmekta Taqbaylit-Tacawit | Université de Béjaïa | 2017 |

### Documents internes du projet
| Fichier | Contenu |
|---------|---------|
| `ml_pipeline/dataset/bejaia_dialect_reference_grammar.md` | Grammaire de référence Tasahlit pour ASR : phonologie, morphosyntaxe, code-switching, emprunts |
| `augmentation/research/mms_kabyle_orthography.md` | Orthographe MMS Kabyle, mapping arabizi → diacritiques, stratégie TTS |
| `augmentation/research/bpe_corpus_analysis.py` | Analyse BPE du corpus réel (tokens, morphologie, ratio CS) |
| `augmentation/kabyle_lexicon.yaml` | Lexique Kabyle-Français structuré |
| `augmentation/kabyle_guard_rules.yaml` | Règles de validation linguistique pour la génération |
| `augmentation/config/geography.yaml` | Géographie Béjaïa (communes, daïras) |

---

## 🎯 7. Méthodologie & Frameworks

| Méthode | Usage dans le projet | Source |
|---------|---------------------|--------|
| **AHP** (Analytic Hierarchy Process) | Comparaison multicritère Cloud vs Local ASR | `THESE_M2_PLAN_RECHERCHE.md` |
| **TOPSIS / ELECTRE** | Alternatives MCDA | État de l'art |
| **Pseudo-Labeling** | IA génère → humain corrige (iterative loop) | `sota_methodology_asr.md` |
| **Matrix Language Frame** | Annotation code-switching (matrice Kabyle) | `bejaia_dialect_reference_grammar.md` |
| **BPE Analysis** | Validation qualité données synthétiques | `augmentation/research/bpe_corpus_analysis.py` |
| **QLoRA + Outlines** | Fine-tuning efficient + extraction structurée JSON | `NASDA Presentation Draft.md` |
| **Cohen's Kappa** | Accord inter-annotateur, validation qualité annotations | `THESE_M2_PLAN_RECHERCHE.md`, `NASDA Presentation Draft.md` |

---

## 📐 8. Documents Internes du Projet (docs/ & enregistrement/)

### Profil Linguistique & Grammaire
| Fichier | Contenu |
|---------|---------|
| `docs/PROFIL_LINGUISTIQUE_BEJAIA.md` | **Profil linguistique complet du dialecte de Béjaïa** : phonologie Tasahlit, code-switching patterns, morphosyntaxe, statistiques corpus |
| `enregistrement/Frameworks_Grammaticaux_NLP_Tasahlit.md` | Frameworks grammaticaux NLP adaptés au Tasahlit, structures morphologiques |
| `enregistrement/Kabyle_ASR_LLM_RAG_Guide.md` | Guide complet ASR+LLM+RAG pour le Kabyle, architecture pipeline, Tamazight NLP landscape |
| `enregistrement/Kabyle_Matrices_Diagrams.md` | Matrices et diagrammes du système Kabyle |

### Cadrage Académique & Présentations
| Fichier | Contenu |
|---------|---------|
| `docs/CADRAGE_ACADEMIQUE_SDAD.md` | Cadrage académique pour le Master SDAD (Science des Données et Aide à la Décision) |
| `docs/NASDA_PRESENTATION_DATA_ALGERIE_IA.md` | Présentation NASDA — Data & IA en Algérie |
| `docs/SESSION_7_FEVRIER_2026.md` | Session de travail du 7 février 2026 |
| `ml_pipeline/PLAN_MEMOIRE_REVISE.md` | Plan du mémoire révisé |

### Profils d'Annotation & Analyse Qualité
| Fichier | Contenu |
|---------|---------|
| `dataset/annotations_real_profile.json` | Profil statistique des annotations réelles (distribution types d'incidents, gravité, etc.) |
| `dataset/annotations_local_profile.json` | Profil statistique des annotations locales |
| `enregistrement/grammairekabyle.txt` | Grammaire Kabyle détaillée avec références arXiv (DziriBERT, NoLoR, chDzDT) |
| `enregistrement/resultas etat dart.txt` | Résultats état de l'art : Outlines, APIE, Whisper multilingual |

### Analyse Cohen's Kappa (Inter-Annotateur)
| Référence | Usage |
|-----------|-------|
| **Cohen's Kappa κ** | Mesure d'accord inter-annotateur pour valider la qualité des annotations |
| **Double annotation** | Protocole : 2 annotateurs sur un sous-ensemble → calcul κ |
| Cité dans | `THESE_M2_PLAN_RECHERCHE.md` (Phase 1 : Constitution du Dataset) |

### Analyse KPI de l'Ancien App DGPC (Legacy)
| Fichier | Contenu |
|---------|---------|
| `ml_pipeline/CHAPITRE_MEMOIRE_KPI_LEGACY_DGPC.md` | **Chapitre complet mémoire** : analyse KPI du système existant de gestion des appels DGPC |
| `ml_pipeline/dataset/legacy_exports_live/kpi_memoire_report.md` | Rapport KPI détaillé généré |
| `ml_pipeline/dataset/legacy_exports_live/generate_kpi_memoire_report.py` | Script de génération du rapport KPI |
| `ml_pipeline/dataset/legacy_exports_live/kpi_summary.json` | Résumé KPI en JSON |
| `ml_pipeline/dataset/legacy_exports_live/kpi_action_distribution.csv` | Distribution des actions par type |
| `ml_pipeline/dataset/legacy_exports_live/kpi_events_categories.csv` | Catégories d'événements |
| `ml_pipeline/dataset/legacy_exports_live/kpi_events_distribution.csv` | Distribution temporelle événements |
| `ml_pipeline/dataset/legacy_exports_live/kpi_hourly_calls.csv` | Volume d'appels par heure |
| `ml_pipeline/dataset/legacy_exports_live/kpi_monthly_calls.csv` | Volume d'appels mensuel |
| `ml_pipeline/dataset/legacy_exports_live/kpi_monthly_service_levels.csv` | Niveaux de service mensuels |
| `ml_pipeline/dataset/legacy_exports_live/kpi_line_reliability.csv` | Fiabilité des lignes téléphoniques |
| `ml_pipeline/dataset/legacy_exports_live/kpi_data_quality.csv` | Qualité des données |

---

## 📐 9. Conférences Cibles (Publication)

| Conférence | Focus | Pertinence |
|------------|-------|------------|
| **AfricaNLP** | Langues africaines NLP | Kabyle = langue africaine |
| **INTERSPEECH** | ASR, speech processing | Évaluation comparative ASR |
| **LREC-COLING** | Low-resource languages | Premier dataset Kabyle urgences |
| **ISCA SynData4GenAI** | Données synthétiques pour IA | Génération synthétique Kabyle |
| **ACL Workshops** | Code-switching | CS Kabyle/FR/AR |

---

## 🔑 10. APIs & Services

| Service | Usage | Accès |
|---------|-------|-------|
| **Google Gemini API** | Transcription, annotation, génération synthétique | Clé API (`.env`) |
| **Google Colab** | Entraînement GPU (Whisper, Qwen) | Gratuit (T4) ou Pro (A100) |
| **Mozilla Common Voice** | Téléchargement dataset audio Kabyle | [commonvoice.mozilla.org](https://commonvoice.mozilla.org/) |
| **HuggingFace Hub** | Téléchargement modèles/datasets | [huggingface.co](https://huggingface.co/) |

---

> **Contribution unique du projet** : Premier dataset annoté Kabyle/Français/Arabe pour les appels d'urgence de la Protection Civile (DGPC Béjaïa), avec pipeline complet ASR → NLU → Aide à la Décision.
