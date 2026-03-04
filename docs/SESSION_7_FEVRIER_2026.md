# 📋 SESSION DE TRAVAIL — 6-7 Février 2026
## Synthèse Complète : Analyse, Décisions & Architecture Finale

**Durée** : ~8h de discussion intensive  
**Objectif** : Analyser toutes les recherches, clarifier l'architecture, prendre des décisions définitives  
**Résultat** : Document de référence unique pour la suite du projet

---

## TABLE DES MATIÈRES

1. [Vue d'ensemble du projet](#1-vue-densemble)
2. [Audit du code existant (Lauren AI + vérification)](#2-audit-du-code)
3. [Analyse de toutes les recherches](#3-analyse-recherches)
4. [Architecture finale décidée](#4-architecture-finale)
5. [Le RAG : où, quand, et dans quel ordre](#5-rag)
6. [RAG pour Whisper vs Knowledge-in-the-weights](#6-rag-whisper)
7. [Comment le modèle apprend : kabyle → enum anglais](#7-mapping-semantique)
8. [Protections contre le "right by chance"](#8-protections-hallucination)
9. [Data augmentation : équilibre, pas volume](#9-data-augmentation)
10. [Knowledge-Grounded Data Generation (RAG inversé)](#10-rag-inverse)
11. [openSMILE : fusion prosodie pour urgence](#11-opensmile)
12. [Outlines : constrained decoding](#12-outlines)
13. [Audit annotation app](#13-audit-annotation-app)
14. [Sprints et ordre d'exécution](#14-sprints)

---

## 1. VUE D'ENSEMBLE DU PROJET <a name="1-vue-densemble"></a>

### Titre
**"Analyse Comparative des Solutions ASR pour le Traitement Automatique des Appels d'Urgence Multilingues"**

### 3 Objectifs parallèles
| # | Objectif | Livrable |
|---|----------|----------|
| 1 | **Diplôme M2 SDAD** — Université A. MIRA de Béjaïa | Mémoire + soutenance |
| 2 | **Label Startup "Data Algérie"** | Plateforme démontrable |
| 3 | **Plateforme décisionnelle DGPC** | Archive + analyse spatiotemporelle |

### Stack technique confirmé
- **ASR** : Whisper Large V3 fine-tuné sur Kabyle (modèle `whisper-kabyle-dgpc-v6`)
- **Extraction** : Qwen 2.5 7B Instruct + QLoRA 4-bit
- **Post-processing** : enums.py (14 types, TriState, compute_urgency 16 règles)
- **Annotation** : Streamlit app (dgpc_annotation_local.py)
- **RAG** : ChromaDB + multilingual-e5-large (planifié, pas encore implémenté)
- **Prosodie** : openSMILE + Random Forest (planifié)
- **Constrained decoding** : Outlines (planifié)

---

## 2. AUDIT DU CODE EXISTANT <a name="2-audit-du-code"></a>

### 7 bugs confirmés (Lauren AI review, tous vérifiés)

| # | Sévérité | Fichier | Bug | Status |
|---|----------|---------|-----|--------|
| 1 | 🔴 BLOQUANT | `validators.py` | Pydantic v1 API (`@validator`) avec Pydantic 2.11.7 installé | À fixer |
| 2 | 🔴 BLOQUANT | `agent3_pipeline_pseudocode.py:209` | `class QLo RADatasetGenerator` (espace dans le nom) | À fixer |
| 3 | 🔴 BLOQUANT | `test_agent3_sample.py` | Simule la sortie LLM, n'appelle jamais le vrai modèle | À fixer |
| 4 | 🟡 HIGH | Tous les fichiers | Noms de champs incohérents (`lieu_final` vs `location`) | À fixer |
| 5 | 🟡 HIGH | `dgpc_annotation_local.py` | Schéma non aligné avec Agent 3 / enums.py | À fixer |
| 6 | 🟡 MEDIUM | `convert_to_jsonl.py:135` | Division par zéro (`stats['ok']/stats['total_segments']*100`) | À fixer |
| 7 | 🟡 MEDIUM | Repo | 4 documents cités dans le recap n'existent pas (étaient dans cache Gemini) | Documenté |

### Fichiers analysés et verdict

| Fichier | Verdict | Action |
|---------|---------|--------|
| `enums.py` (378 lignes) | ✅ GARDER — ontologie solide, compute_urgency = innovation | Aucune |
| `validators.py` (178 lignes) | ✅ GARDER + FIXER — migrer Pydantic v2 | Sprint 0 |
| `agent3_pipeline_pseudocode.py` (479 lignes) | ⏸️ ARCHIVER — pseudo-code non exécutable | Sprint 0 (fix syntax) |
| `convert_to_jsonl.py` (218 lignes) | ✅ GARDER + FIXER — division par zéro | Sprint 0 |
| `test_agent3_sample.py` (257 lignes) | ✅ GARDER + FIXER — connecter au vrai LLM | Sprint 1 |
| `agent_3_prompt.txt` (120 lignes) | ✅ GARDER — bien structuré, aligné avec enums.py | Aucune |
| `schema_complete_lauren.json` (408 lignes) | ⏸️ DIFFÉRER — over-engineered pour maintenant | Post-diplôme |
| `qlora_finetune_data.json` (5002 lignes) | ⚠️ MIGRER — ancien format, données précieuses | Sprint 2 |
| `dgpc_pipeline.py` (286 lignes) | ✅ GARDER — pipeline fonctionnel | Enrichir prompt |
| `dgpc_knowledge_base.py` (428 lignes) | ✅ GARDER — 52 communes, essentiel | Aucune |
| `dgpc_annotation_local.py` (397 lignes) | ✅ GARDER + RÉALIGNER — UI bonne, schéma ancien | Sprint 1 |

---

## 3. ANALYSE DE TOUTES LES RECHERCHES <a name="3-analyse-recherches"></a>

### Documents analysés (8+ documents, >5000 lignes)

#### Documents à GARDER comme référence active :
| Document | Contenu | Qualité |
|----------|---------|---------|
| `resultas etat dart.txt` (920 lignes) | 7 approches architecturales, matrice de comparaison, SOTA 2025-2026 | ⭐ Le meilleur |
| `bejaia_dialect_grammar.md` | Guide dialecte Béjaïa (négation, genre, code-switching) | ⭐ Opérationnel |
| `sota_methodology_asr.md` | Gold standard annotation, stratégie itérative | Bon |
| `Kabyle_Matrices_Diagrams.md` (732 lignes) | Matrices décision ASR/embeddings/hyperparams, timeline | Bon |

#### Documents à ARCHIVER (consultables si besoin) :
| Document | Raison |
|----------|--------|
| `PAPERS_METHODOLOGIE.md` (196 lignes) | Conclusions absorbées dans l'état de l'art |
| `REFERENCES_ACADEMIQUES.md` | Recommandations dépassées (spaCy NER, text2num) |
| `Frameworks_Grammaticaux_NLP_Tasahlit.md` (812 lignes) | Trop deep pour le PFE (UD, ELAN 10 tiers = projet 18-24 mois) |
| `grn.txt` + images (données synthétiques) | CTGAN/TVAE pas applicable (données textuelles, pas tabulaires) |

### Classification des idées de recherche

#### ✅ IDÉES VALIDÉES ET GARDÉES :
1. Pipeline ASR → LLM → Post-processing (confirmé par ECA 2025, 92.7%)
2. Whisper Large V3 fine-tuné (confirmé par toutes les sources)
3. QLoRA 4-bit fine-tuning (bon compromis taille/perf)
4. School B pragmatique pour code-switching (consensus académique)
5. Ontologie 14 types + TriState (contribution originale)
6. Data mixing 70/30 pour éviter catastrophic forgetting (Swiss German + Amharic studies)

#### ⚡ IDÉES À INTÉGRER (faisables) :
1. **openSMILE** — fusion prosodie pour urgence (2-3 jours, +1 contribution)
2. **Outlines** — constrained decoding JSON (1 jour, production-ready)
3. **Data augmentation guidée par knowledge base** (RAG inversé)
4. **Enrichissement prompt Whisper** avec les 52 communes

#### ⏸️ IDÉES DIFFÉRÉES (post-diplôme) :
1. Phoneme-Direct Slot Filling (trop risqué, quasi aucune littérature)
2. Knowledge Graphs Neuro-Symboliques (latence >30s)
3. Universal Dependencies pour Kabyle (projet 18-24 mois)
4. W2V-BERT 2.0 comme ASR alternatif (Whisper v6 marche déjà)
5. Ragas/DeepEval (pertinent seulement quand RAG opérationnel)

#### ❌ IDÉES ÉLIMINÉES :
1. spaCy custom NER → remplacé par Qwen QLoRA
2. text2num → le LLM normalise nativement
3. CAMeLBERT → pour arabe, pas kabyle
4. N-gram LM rescoring → technique ancienne, LLM fait mieux
5. CTGAN/TVAE → données textuelles, pas tabulaires

---

## 4. ARCHITECTURE FINALE DÉCIDÉE <a name="4-architecture-finale"></a>

```
┌────────────────────────────────────────────────────────────────┐
│                    AUDIO (appel d'urgence)                     │
└─────────────┬────────────────────────────┬─────────────────────┘
              │                            │
    ┌─────────▼──────────┐      ┌──────────▼──────────┐
    │  WHISPER V3 FT     │      │  openSMILE          │
    │  (Kabyle + 30%mix) │      │  (prosody features) │
    │  + Prompt enrichi  │      │  → stress_score     │
    │  (52 communes)     │      │  (Random Forest)    │
    │  → Transcription   │      │                     │
    └─────────┬──────────┘      └──────────┬──────────┘
              │                            │
    ┌─────────▼──────────────────────────────────────────┐
    │  QWEN 2.5 7B QLoRA + Outlines (constrained JSON)  │
    │  + RAG contextuel (ChromaDB + Knowledge Base)      │
    │  → JSON structuré 100% valide                      │
    │    {incident_type, location, victims_count,        │
    │     injuries_severity, fire_present,               │
    │     trapped_persons, weapons_involved,             │
    │     hazmat_involved}                               │
    └─────────┬──────────────────────────────────────────┘
              │
    ┌─────────▼──────────────────────────────────────────┐
    │  POST-PROCESSING DÉTERMINISTE (code Python)        │
    │  ├─ compute_urgency() — 16 règles métier           │
    │  ├─ compute_dispatch() — table if/else             │
    │  ├─ Fusion urgence: texte × prosodie (stress_score)│
    │  ├─ TriState anti-hallucination                    │
    │  └─ Pydantic v2 validation                         │
    └─────────┬──────────────────────────────────────────┘
              │
    ┌─────────▼──────────┐
    │  OUTPUT CANONIQUE   │
    │  EmergencyCall JSON │
    └─────────────────────┘
```

### Décision clé : dispatch = CODE, pas LLM

Le LLM extrait les **faits** (incident_type, location, victims_count...).
Le **code** calcule les **décisions** (urgency, dispatch).

```python
# Le LLM ne fait PAS ça. C'est du code déterministe.
def compute_dispatch(extraction):
    if extraction.fire_present == "yes" and extraction.trapped_persons == "yes":
        return "dispatch_fire_unit + dispatch_ambulance"
    if extraction.incident_type == "drowning":
        return "dispatch_fire_unit_plongeurs"
    if extraction.incident_type.startswith("accident") and extraction.injuries_severity in ("severe", "fatal"):
        return "dispatch_ambulance + dispatch_police"
    # ... etc.
```

**Raison** : Les règles de dispatch sont des procédures DGPC fixes. Un LLM n'ajoute aucune valeur ici, et peut halluciner. Le code est déterministe, testable, auditable.

---

## 5. LE RAG : OÙ, QUAND, ET DANS QUEL ORDRE <a name="5-rag"></a>

### Conclusion clé : Le RAG est un MULTIPLICATEUR, pas un FONDEMENT

```
ORDRE OBLIGATOIRE:
                                                          Gain cumulé
1. Extraction de base fonctionnelle (fix bugs)           0% → ~85%
   ├─ Fix Pydantic v2
   ├─ Constrained decoding (Outlines)
   └─ Alignement schéma unique

2. Fine-tuning QLoRA sur données réelles                 85% → ~90-92%
   ├─ Migrer 5000 entrées au bon format
   └─ Entraîner Qwen sur données DGPC

3. RAG (maintenant ça a du sens)                         90% → ~94-95%
   ├─ ChromaDB + knowledge base géographique
   ├─ Le LLM SAIT déjà extraire
   └─ RAG corrige les cas limites (noms de lieux rares)

4. Prosodie openSMILE                                    94% → ~96%
   └─ Urgence acoustique en parallèle
```

**Pourquoi pas RAG d'abord ?** : Donner un meilleur contexte à un extracteur cassé ne corrige rien. RAG × 0 = 0. RAG × 0.9 = amélioration significative.

**Analogie** : Un stagiaire non formé avec tous les documents de référence sur le bureau → fiches mal remplies. Il faut le former (QLoRA) AVANT de lui donner les documents (RAG).

---

## 6. RAG POUR WHISPER VS KNOWLEDGE-IN-THE-WEIGHTS <a name="6-rag-whisper"></a>

### Le prompt Whisper actuel est déjà une forme primitive de RAG

```python
# Dans dgpc_pipeline.py — prompt statique de ~60 mots
KABYLE_PROMPT = """
Yella laccident, ulac abrid. Yettwat, ur yettwat ara.
Yemmut yiwen, mouten sin. Ijreh urgaz, jerhen tilawin.
Yella g Amizour, yusad seg Akbou, yedda ar Tichy.
...
"""
```

Ce prompt biaise le décodeur Whisper vers le vocabulaire kabyle (les mots dans le prompt deviennent plus probables dans la sortie).

### 3 niveaux d'aide pour Whisper

| Niveau | Méthode | Effort | Moment |
|--------|---------|--------|--------|
| **1. Enrichir le prompt statique** | Ajouter les 52 communes + routes + vocabulaire dans `KABYLE_PROMPT` | 30 min | Maintenant |
| **2. Post-correction fuzzy** | Après transcription, fuzzy match des mots contre le gazetteer avec `rapidfuzz` | 1 jour | Sprint 2 |
| **3. Double passe dynamique** | Passe 1 brute → chercher dans KB → prompt contextuel → Passe 2 corrigée | 2-3 jours | Si nécessaire |

### Décision prise : Knowledge-in-the-weights > RAG à l'inférence

**Au lieu de corriger Whisper à l'exécution (RAG), éliminer les faiblesses à l'entraînement** :

```
ENTRAÎNEMENT WHISPER ENRICHI:

1. Data augmentation guidée par le gazetteer
   Knowledge base → communes sous-représentées → Gemini génère phrases 
   → TTS → audio synthétique → ajouter au dataset

2. Prompt-conditioned fine-tuning
   Entraîner sur (audio, prompt_contextuel, texte) au lieu de (audio, texte)

3. SpecAugment + speed perturbation
   ├─ Masquage fréquences (1 ligne de config)
   ├─ Speed 0.9x/1.1x (1 ligne)
   ├─ Noise injection (bruit urbain)
   └─ Pitch shift ±2 semitones
   → ×3 taille effective du dataset

4. Data mixing
   70% données DGPC + 30% FLEURS/CommonVoice multilingue
   → empêche catastrophic forgetting (français/arabe)
```

**Avantages** : Zéro latence runtime, zéro complexité déploiement. Le modèle SAIT déjà.

---

## 7. COMMENT LE MODÈLE APPREND : KABYLE → ENUM ANGLAIS <a name="7-mapping-semantique"></a>

### C'est un mapping SÉMANTIQUE, pas une traduction

```
INPUT (kabyle mixte):  "times tech3el g wexxam g Tichy, sin n yirgazen jerhen"
                            ↓ mapping sémantique
OUTPUT (JSON structuré): {
    "incident_type": "fire_building",    ← times + wexxam = feu + maison
    "location": "Tichy",                 ← nom propre, gardé tel quel
    "victims_count": 2,                  ← sin = 2
    "injuries_severity": "minor",        ← jerhen = blessés (pas morts)
    "fire_present": "yes"                ← times = feu → oui
}
```

### Pourquoi des enums en ANGLAIS ?

| Option | Problème |
|--------|----------|
| Enum kabyle (`"times_wexxam"`) | Pas de terminologie standardisée. "times", "l7riq", "lḥriq", "l3afia" = même chose → impossible à normaliser |
| Enum français (`"incendie_batiment"`) | Accents/encodage, LLM pré-entraîné majoritairement en anglais |
| **Enum anglais (`"fire_building"`)** | ✅ Standard ML, pas d'ambiguïté, Qwen comprend nativement |

Les enums sont des **codes machine**, pas du texte humain.

### Dans l'annotation app : français pour l'humain, anglais pour la machine

```python
INCIDENT_LABELS = {
    "❓ Inconnu": "unknown",
    "🚗 Accident véhiculaire": "accident_vehicular",
    "🚶 Accident piéton": "accident_pedestrian",
    "🔥 Incendie bâtiment": "fire_building",
    "🌲 Feu de forêt": "fire_forest",
    "🚗🔥 Véhicule en feu": "fire_vehicle",
    "🏥 Urgence médicale": "medical_emergency",
    "🌊 Noyade": "drowning",
    "👊 Agression/Violence": "assault_violence",
    "🔓 Vol/Cambriolage": "theft_robbery",
    "🌍 Catastrophe naturelle": "natural_disaster",
    "☣️ Matières dangereuses": "hazmat",
    "🔍 Personne disparue": "lost_person",
    "🏚️ Effondrement": "structural_collapse",
    "📝 Autre": "other"
}
# L'annotateur voit "🔥 Incendie bâtiment", le JSON stocke "fire_building"
```

### Le dataset QLoRA final :

```json
{
  "instruction": "Extraire les informations d'un appel d'urgence kabyle/français. Répondre en JSON.",
  "input": "Azul yella times tech3el g wexxam g Tichy sin n yirgazen jerhen",
  "output": "{\"incident_type\":\"fire_building\",\"location\":\"Tichy\",\"victims_count\":2,\"injuries_severity\":\"minor\",\"fire_present\":\"yes\",\"trapped_persons\":\"unknown\",\"weapons_involved\":\"no\",\"hazmat_involved\":\"no\"}"
}
```

---

## 8. PROTECTIONS CONTRE LE "RIGHT BY CHANCE" <a name="8-protections-hallucination"></a>

### Le risque : le modèle apprend des raccourcis au lieu de raisonner

Si 80% des "times" dans le dataset → `fire_building`, le modèle fait `times → fire_building` par raccourci, sans comprendre que `times + tagant = fire_forest`.

### 3 protections :

#### Protection 1 : Diversité des exemples par type
Minimum 30-50 exemples par incident_type, avec formulations variées :
```
fire_building (50 exemples):
├─ "times tech3el g wexxam"          (kabyle pur)
├─ "l7riq g lbatima"                 (darija)
├─ "yella incendie g l'appartement"  (code-switch FR)
├─ "lḥriq yella g lmadrasa"         (kabyle + arabe)
└─ "ça brûle dans la maison"        (français pur)
```

#### Protection 2 : Contre-exemples explicites
Le MÊME mot dans des contextes différents → résultats différents :
```
"times tech3el g wexxam"   → fire_building   (feu + maison)
"times tech3el g tagant"   → fire_forest     (feu + forêt)
"times tech3el g tomobil"  → fire_vehicle    (feu + voiture)
"teqleb tomobil g tamdint" → accident_vehicular (renversé, PAS de feu)
```

#### Protection 3 : Champ `notes` comme Chain-of-Thought léger
```json
{
  "output": {
    "incident_type": "fire_building",
    "notes": "times=feu, wexxam=maison → fire_building. jerhen=blessés légers → minor"
  }
}
```
Force le modèle à verbaliser son raisonnement. Si le raisonnement est faux, on le voit immédiatement.

### Tests adversariaux post-entraînement :
```
TEST 1 (minimal pair — un mot change):
"times g wexxam"  → attend: fire_building ✓
"times g tagant"  → attend: fire_forest ✓
"times g tomobil" → attend: fire_vehicle ✓
→ Si les 3 corrects → le modèle utilise le contexte

TEST 2 (même contexte, verbe différent):
"yeqleb tomobil g Tichy"   → attend: accident_vehicular (pas de feu)
"tech3el tomobil g Tichy"  → attend: fire_vehicle (feu)
→ Le modèle distingue "renverser" de "brûler"

TEST 3 (ambiguïté volontaire):
"yella kra g tamdint"      → attend: "unknown" + notes indiquant ambiguïté
→ Si le modèle dit "unknown" plutôt que deviner → il est honnête
```

---

## 9. DATA AUGMENTATION : ÉQUILIBRE, PAS VOLUME <a name="9-data-augmentation"></a>

### Principe fondamental
La donnée synthétique n'est pas là pour "avoir plus de données". Elle est là pour **corriger les déséquilibres** des données réelles.

### Protocole en 10 étapes :

```
1.  ANNOTER les 320 appels réels (app Streamlit réalignée)
2.  COMPTER la distribution par type (script Python)
3.  IDENTIFIER les trous sur 4 axes :
    ├─ Axe 1: Par incident_type (ai-je ≥50 exemples par type ?)
    ├─ Axe 2: Par langue (kabyle pur / code-switch / français / darija)
    ├─ Axe 3: Par lieu (les 52 communes sont-elles couvertes ?)
    └─ Axe 4: Par combinaison rare (noyade à Aokas ? hazmat à Akbou ?)
4.  PLANIFIER l'augmentation (combien par type, quelles variations)
5.  GÉNÉRER avec Gemini (prompt structuré enrichi knowledge)
6.  VALIDER humainement (moi = locuteur natif, avantage unique)
7.  FUSIONNER réel + synthétique validé
8.  SPLIT train/eval/test
9.  ENTRAÎNER QLoRA
10. TESTER sur données RÉELLES uniquement
```

### Règle critique du split :
```
train.jsonl  ← 70% (réel + synthétique mélangés)
eval.jsonl   ← 15% (RÉEL UNIQUEMENT !!!)
test.jsonl   ← 15% (RÉEL UNIQUEMENT !!!)

JAMAIS de synthétique dans eval/test.
Sinon tu mesures la capacité du modèle à reproduire ce que Gemini génère,
pas à comprendre de vrais appels.
```

### Matrice de variation systématique :
Pour chaque incident_type, varier sur 5 dimensions :
```
1. QUI appelle:
   ├─ Témoin paniqué      → "Arwah-d! Arwah-d! S zerb!"
   ├─ Victime calme       → "Azul, yella kra n le problème dagi..."
   ├─ Famille en pleurs   → "Wallah yemmut! 3edjled!"
   ├─ Professionnel       → "Yella accident g RN9, sin blessés graves"
   └─ Enfant              → "Baba yejreḥ! Awi-d tabibte!"

2. COMBIEN de victimes: 0, 1, 2-3, 5+, "beaucoup", inconnu

3. OÙ: tourner sur les 52 communes, routes, quartiers, descriptions vagues

4. COMMENT il dit le type d'incident:
   Pour fire: "times", "l7riq", "lḥriq", "l3afia", "incendie", "ça brûle", "tech3el",
   implicite: "dukhan yetteffeɣ-d g ṭṭaq" (fumée sort de la fenêtre)

5. LANGUE dominante: kabyle 90%, 50/50 code-switch, français 80%, darija
```

### Organisation des fichiers :
```
ml_pipeline/dataset/
├── annotations_real.jsonl          ← 320 appels réels annotés
├── annotations_synthetic.jsonl     ← ~380 exemples synthétiques
├── distribution_report.json        ← comptages automatiques
├── augmentation_plan.json          ← plan de génération
├── synthetic_generation/
│   ├── gen_template.py             ← template réutilisable
│   └── human_review_log.json       ← suivi validation humaine
└── final/
    ├── train.jsonl                  ← 70% (réel + synthétique)
    ├── eval.jsonl                   ← 15% (RÉEL UNIQUEMENT)
    └── test.jsonl                   ← 15% (RÉEL UNIQUEMENT)
```

---

## 10. KNOWLEDGE-GROUNDED DATA GENERATION (RAG INVERSÉ) <a name="10-rag-inverse"></a>

### Le problème sans knowledge :
```
Gemini (sans contexte) génère:
├─ ❌ "Yeghraq g la piscine n Tichy"     ← Tichy n'a pas de piscine
├─ ❌ "Yeghraq g la rivière n Tichy"     ← La rivière s'appelle Soummam
├─ ❌ "Arwa-d s zerb"                     ← Grammaire fausse (manque -h)
└─ Gemini HALLUCINE parce qu'il ne connaît pas Béjaïa
```

### La solution : injecter le knowledge DANS le prompt de génération

```
PROMPT DE GÉNÉRATION ENRICHI = 5 BLOCS :

BLOC 1: KNOWLEDGE GÉOGRAPHIQUE (de dgpc_knowledge_base.py)
  "Plages: Tichy, Boulimat, Saket, Melbou, Aokas
   Cours d'eau: Oued Soummam, Oued Ghir, Oued Daas
   Barrages: Tichy-Haf, Ighil Emda
   RÈGLE: UNIQUEMENT cette liste, jamais inventer de lieu."

BLOC 2: LEXIQUE KABYLE D'URGENCE (de bejaia_dialect_grammar.md)
  "Noyade: yeghraq/ighriq/ghraqen
   Lieux: lbḥer (mer), assif (rivière), tala (source)
   Appel: arwah-d (venez), 3edjled (dépêchez)
   RÈGLE: Utiliser CES mots, pas des inventions."

BLOC 3: GRAMMAIRE KABYLE
  "Négation: Ur + verbe + ara
   Impératif: Arwah-d (avec -d directionnel)
   Conjugaison: i- + racine (iɣraq = il se noie)
   RÈGLE: Conjuguer correctement."

BLOC 4: EXEMPLES RÉELS VALIDÉS (2-3 gold standard)
  "1. 'Azul, yella wergaz yeghraq g lbḥer n Tichy, arwah-d s zerb!'
   2. 'Wesh 3edjled! Sin n warrac ghraqen g Boulimat bessah!'
   RÈGLE: Imiter CE style et CE mélange linguistique."

BLOC 5: CONSIGNE
  "GÉNÈRE 10 appels de DROWNING. Varie lieu/victimes/style/langue."
```

### Résultat :
| Sans knowledge | Avec knowledge (RAG inversé) |
|---|---|
| Invente des lieux | Utilise uniquement les vrais lieux |
| Grammaire approximative | Grammaire correcte |
| Vocabulaire générique | Vocabulaire spécifique bejaoui |
| Rejet ~40% des exemples | Rejet ~10-15% |

### Contribution thèse :
"Knowledge-Grounded Synthetic Data Generation for Low-Resource Emergency ASR"
→ Meilleur que Paper 2 (ISCA 2024) qui génère du code-switch arabe SANS contexte géographique.

---

## 11. OPENSMILE : FUSION PROSODIE POUR URGENCE <a name="11-opensmile"></a>

### Cas d'usage clé

```
SCÉNARIO B: Mots vagues + Voix paniquée
"Arwah-d s zerb! Yella kra dagi! 3edjled!" (hurlé, pleurs en fond)
→ LLM seul: incident_type = "unknown", urgency = "medium"
→ Prosodie: pitch élevé, speech rate rapide → stress_score = 0.95
→ FUSION: urgency = "high" ← LA PROSODIE CORRIGE LE LLM
```

### Intégration (10 lignes de code) :
```python
# Branche parallèle — n'impacte pas la pipeline existante
import opensmile
smile = opensmile.Smile(feature_set=opensmile.FeatureSet.ComParE_2016)
features = smile.process_file("appel.wav")
stress_score = random_forest_model.predict(features)

# Fusion dans compute_urgency
if stress_score > 0.8 and urgency_text in ("low", "medium"):
    final_urgency = "high"     # voix paniquée → on monte
elif stress_score < 0.2 and urgency_text == "critical":
    flag_for_review = True     # voix calme + mots critiques → vérifier
else:
    final_urgency = urgency_text
```

### Timing : Sprint 4 (après QLoRA)
Raison : le Random Forest a besoin de labels d'urgence → qui viennent de l'annotation (Sprint 2).

---

## 12. OUTLINES : CONSTRAINED DECODING <a name="12-outlines"></a>

### Le problème sans Outlines :
```json
// Sortie LLM non contrainte — INVALIDE
{"incident_type": "fire", "fire_present": "oui", "urgency": "très urgent"}
// → "fire" pas dans l'enum, "oui" pas dans TriState, "très urgent" pas dans UrgencyLevel
// → Pydantic crash, extraction perdue
```

### Avec Outlines :
```python
import outlines
from outlines import models, generate

model = models.transformers("Qwen/Qwen2.5-7B-Instruct")
schema = {
    "type": "object",
    "properties": {
        "incident_type": {
            "enum": ["unknown", "accident_vehicular", "accident_pedestrian",
                     "fire_building", "fire_forest", "fire_vehicle",
                     "medical_emergency", "drowning", "assault_violence",
                     "theft_robbery", "natural_disaster", "hazmat",
                     "lost_person", "structural_collapse", "other"]
        },
        "fire_present": {"enum": ["unknown", "yes", "no"]},
        "trapped_persons": {"enum": ["unknown", "yes", "no"]},
        "weapons_involved": {"enum": ["unknown", "yes", "no"]},
        "hazmat_involved": {"enum": ["unknown", "yes", "no"]},
        "location": {"type": "string"},
        "victims_count": {"type": ["integer", "null"]},
        "injuries_severity": {
            "enum": ["unknown", "none", "minor", "severe", "fatal"]
        }
    },
    "required": ["incident_type", "location", "fire_present"]
}

generator = generate.json(model, schema)
result = generator("Yella times g wexxam g Tichy, sin jerhen")
# result est GARANTI conforme au schema, 100% du temps
```

### Double usage :
1. **Production** : Qwen + Outlines → JSON toujours valide
2. **Génération données synthétiques** : chaque exemple généré automatiquement conforme

### Timing : Sprint 3 (avec QLoRA)
Non-négociable — sans ça, le système crash en production.

---

## 13. AUDIT ANNOTATION APP <a name="13-audit-annotation-app"></a>

### Problèmes identifiés :

| # | Sévérité | Problème |
|---|----------|----------|
| 1 | 🔴 | Schéma complètement différent de enums.py (`nature` vs `incident_type`, `urgence` 3 niveaux vs 5) |
| 2 | 🔴 | Clé API Gemini en clair dans `config.json` (dans le repo) |
| 3 | 🟡 | `agent_3_prompt.txt` existe mais n'est jamais utilisé par l'app |
| 4 | 🟡 | 17 daïras au lieu de 19 (manque Adekar et Beni Maouche) |

### Ce qui est BON :
- ✅ UI/UX Streamlit pro (design slate, layout compact)
- ✅ Workflow correct (audio → IA → correction → enregistrer)
- ✅ Conversion audio 16kHz mono
- ✅ SYSTEM_PROMPT linguistique excellent (code-switching, arabizi)
- ✅ Export CSV

### Modifications nécessaires (Sprint 1) :
1. `nature` → `incident_type` : selectbox avec 14 valeurs + labels français + emojis
2. `urgence` : 3 valeurs → 5 (`unknown/low/medium/high/critical`)
3. Garder `lieu/commune/daira` (bonne granularité pour annotation)
4. Ajouter 4 selectbox TriState : `fire_present`, `trapped_persons`, `weapons_involved`, `hazmat_involved`
5. `victimes` → `victims_count` (integer) + `injuries_severity` (selectbox)
6. Clé API → `.env` au lieu de `config.json`
7. Compléter `DAIRAS_BEJAIA` (19 au lieu de 17)
8. Le `SYSTEM_PROMPT` linguistique → NE PAS TOUCHER (excellent)

---

## 14. SPRINTS ET ORDRE D'EXÉCUTION <a name="14-sprints"></a>

```
SPRINT 0 — FIX BUGS BLOQUANTS (1 jour)
══════════════════════════════════════
├─ Migrer validators.py Pydantic v1 → v2
├─ Fixer syntax error agent3_pipeline_pseudocode.py
├─ Fixer division par zéro convert_to_jsonl.py
├─ Enrichir KABYLE_PROMPT avec 52 communes
└─ Sécuriser clé API (config.json → .env)

SPRINT 1 — RÉALIGNER ANNOTATION APP (2-3 jours)
══════════════════════════════════════════════════
├─ Remplacer EXTRACTION_PROMPT (ancien schéma → nouveau)
├─ Ajouter selectbox incident_type (14 valeurs)
├─ Ajouter selectbox urgency (5 valeurs)
├─ Ajouter 4 selectbox TriState
├─ victims_count (int) + injuries_severity (selectbox)
├─ Compléter daïras (19)
└─ Garder SYSTEM_PROMPT linguistique (excellent)

SPRINT 2 — ANNOTER + AUGMENTER (2-3 semaines)
══════════════════════════════════════════════════
├─ Annoter 320 appels réels via app réalignée
├─ Compter distribution, identifier trous
├─ Générer synthétique knowledge-grounded (Gemini + KB)
├─ Valider humainement
├─ Migrer 5000 entrées qlora_finetune_data.json (ancien → nouveau)
└─ Split train/eval/test (synthétique JAMAIS dans eval/test)

SPRINT 3 — QLORA + OUTLINES (1 semaine)
══════════════════════════════════════════
├─ Installer Outlines, compiler schema depuis enums.py
├─ QLoRA fine-tune Qwen 2.5 7B (Colab A100)
│  ├─ r=32, alpha=64, 4-bit
│  ├─ lr=2e-4, 5 epochs
│  └─ Avec constrained decoding
├─ Évaluer F1 per entity sur test set RÉEL
└─ Tests adversariaux (minimal pairs)

SPRINT 4 — PROSODIE + FUSION (2-3 jours)
══════════════════════════════════════════
├─ pip install opensmile
├─ Extraire features 6373-dim sur les 320 appels
├─ Entraîner Random Forest stress_score
├─ Intégrer fusion urgence: texte × prosodie
└─ Évaluer gain sur détection urgence

SPRINT 5 — RAG (1 semaine)
══════════════════════════════════════════
├─ ChromaDB setup
├─ Indexer knowledge_base (communes, vocabulaire, historique)
├─ Intégrer dans le prompt Qwen
├─ Évaluer gain sur précision lieu + incident_type
└─ A/B test: avec RAG vs sans RAG

SPRINT 6 — INTÉGRATION + DÉMO (1 semaine)
══════════════════════════════════════════
├─ Pipeline bout-en-bout: Audio → EmergencyCall JSON
├─ Benchmarks finaux
├─ Comparaison vs baseline (Gemini zero-shot)
└─ Préparer démo pour soutenance
```

---

## RÉSUMÉ EN UNE PHRASE

> L'architecture de base (Whisper → Qwen QLoRA → enums.py) est **correcte et bien justifiée**. Le gain marginal le plus élevé maintenant est de **fixer les bugs Sprint 0** (1 jour), **réaligner l'annotation app** (2 jours), puis **annoter les 320 appels** avec le bon schéma. Tout le reste (RAG, openSMILE, Outlines) est un amplificateur qui dépend de cette base solide.

---

*Document généré le 7 février 2026 — Session de travail 6-7 février*
*Projet: Gestion des Appels Téléphoniques DGPC Béjaïa*
*Stack: Whisper V3 FT + Qwen 2.5 7B QLoRA + Outlines + openSMILE + ChromaDB*
