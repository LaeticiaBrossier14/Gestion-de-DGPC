# Frameworks de Description Grammaticale pour le NLP : Spécificités du Tasahlit (Kabyle)
## Rapport de Recherche Académique Approfondie

---

## Executive Summary

Ce rapport synthétise une recherche ciblée sur deux axes stratégiques pour la documentation automatique et linguistique du Tasahlit (Kabyle) en contexte NLP/ASR :

1. **Frameworks de description grammaticale pour dialectes complexes** : méthodologies et standards reconnus mondialement pour annoter, représenter et préserver les structures linguistiques
2. **Spécificités phonologiques et morphologiques du Tasahlit** : caractéristiques pointe qui demandent traitements spécialisés en NLP

Le rapport identifie les défis clés, les solutions technologiques éprouvées via cas d'études analogues, et propose un framework intégré adapté au contexte Kabyle bej aïen avec ressources contraintes.

---

## I. Frameworks de Description Grammaticale pour le NLP

### A. Standards Internationaux Reconnus

#### 1. Universal Dependencies (UD)

**Qu'est-ce que c'est ?** Universal Dependencies est un schéma d'annotation syntaxique harmonisé couvrant >200 langues, développé par la communauté NLP/linguistique mondiale. Il utilise des dépendances plutôt que des arbres de constituants.[1][25]

**Composants clés** :
- **Lemma** : forme de base d'un mot
- **POS Tags** : universels (NOUN, VERB, ADJ, etc.) avec extensions possibles par langue
- **Morphosyntactic Features** : traits comme gender, number, case, tense, aspect
- **Syntactic Dependencies** : relations de dépendance (sujet, objet, modificateur, etc.)

**Avantage pour minoritaires** : UD accepte les extensions linguistiquement motivées tout en gardant cohérence cross-linguistique. Plusieurs langues minoritaires (Kurde, Basque, Gallois) ont des arbres UD.

**Défi pour Kabyle** : la morphologie nonconcatenative (root-template) ne s'encode pas facilement en dépendance word-level standard. Solution : représentation morphosyntaxique enrichie au niveau sub-word.

#### 2. Abstract Meaning Representation (AMR)

Cadre pour représenter le sens sémantique des phrases sous forme de graphes de relations entre concepts.[10] Moins courant pour ASR mais utile pour tâches de compréhension.

#### 3. Linguistic Typology Framework (Croft 2006)

Approche basée sur universaux linguistiques et variations cross-linguistiques typologiques. Propose des dépendances qui reflètent construction meaning plutôt que purement syntaxe.[31]

---

### B. Methodologies de Documentation pour Langues en Danger

#### 1. DOBES Program (Documentation of Endangered Languages)

Framework complet développé par Max Planck Institute for Psycholinguistics [67] :

**Principes clés** :
- Archive long-terme compatible archival standards internationaux
- Architecture flexible pour polysynthetic/morphologically-rich languages
- Lexical databases avec recherche sur roots, stems, affixes
- Preservation de metadata riche

**Applicabilité** : Directement pertinent pour Kabyle - DOBES accepte codes non-écrits, dialectal variation.

#### 2. NoLoR Framework (No-to Low-Resource Language Documentation)

Framework pour accélerer la documentation via ASR, testé sur dialecte Neo-Aramaic [65] :

**4 étapes** :
1. **Define phonemic orthography** : décision écriture + phonemic/phonetic distinctions
2. **Build initial dataset** : 30-60 heures transcribed (peut être petit)
3. **Train ASR model** : fine-tuner modèle pré-entraîné
4. **Community application** : outil accessible speakers

**Résultat** : Avec 35 minutes seulement, ASR produisait transcriptions 6.3× plus vite que transcription manuelle. Tout code + données publiques.

#### 3. ELDP (Endangered Languages Documentation Programme)

Programme financé par SOAS/Leverhulme pour documentation endangered languages [81]. Fournit ressources training, guidelines, accès archive ELAR.

---

### C. Standards d'Annotation et Formats de Données

#### 1. CoNLL-U Format (Universal Dependencies base format)

Format texte plain pour distribution corpus annotés. Chaque token sur ligne séparée, colonnes tab-délimitées :

```
ID | FORM | LEMMA | UPOS | XPOS | FEATS | HEAD | DEPREL | DEPS | MISC
```

Avantages :
- Simple, lisible, parseable facilement
- Support pour multiword tokens (crucial pour agglutinatives)
- Morphosyntactic features arbitraires en colonne FEATS
- Widely supported par outils NLP (spaCy, stanza, etc.)

**Pour Kabyle** : CoNLL-U peut encoder morphologie nonconcatenative via FEATS enrichis (Root, Template, etc.).

#### 2. TEI XML (Text Encoding Initiative)

Standard international pour markup textes linguistiques, édition critique, archivage à long-terme.[41] TEI permet représentation riche grammaires descriptives avec structure sémantique explicite.

Utilisé par archives linguistiques (ELAR, PARADISEC, Documenting Samoan Language Project).

#### 3. OLAC Metadata (Open Language Archives Community)

Standard pour catalogage ressources linguistiques.[30] Permet découverte corpora linguistiques, code language ISO 639, Dublin Core extensions.

---

### D. Outils Pratiques d'Annotation

#### 1. ELAN (EUDICO Linguistic Annotator)

Logiciel gratuit Max Planck pour annotation audio/vidéo linguistique [47][53] :

**Fonctionnalités clés** :
- Multi-tier hierarchiques (parent-child relationships)
- Vocabulaires contrôlés (dropdown lists)
- Linked audio/video (playback synchronisé)
- Export vers formats multiples (ELAN .eaf XML, Praat TextGrid, CoNLL tab-delimited)
- Interopérabilité directe Praat (force-alignment)

**Pour Kabyle** : Perfect pour hierarchy orthography → phonetics → morphology → syntax → loanword flags → dialect marking.

#### 2. Praat (Paul Boersma)

Logiciel phonétique pour analyse acoustique fine [47] :
- Formant analysis
- Force-alignment (aligner transcription avec audio)
- TextGrid files (compatible ELAN)
- Export pour secondary articulations (emphasis, pharyngealization)

#### 3. speach Library (Python)

Bibliothèque Python pour gestion corpus multiformat [50] :
- Read/write ELAN .eaf files
- Convert ELAN ↔ Praat ↔ CoNLL ↔ CSV/JSON/SQLite
- Corpus management workflows
- Interlinear gloss export

---

## II. Spécificités Linguistiques Pointues du Tasahlit (Kabyle)

### A. Phonologie Complexe

#### 1. Inventaire Consonantique Exceptionnel

Kabyle possède ~40+ consonants distincts (incluant geminates) - bien au-delà des langues indo-européennes :

**Traits remarquables** [16][17][37] :
- **Haute concentration fricatives** : /θ/, /ð/, /ʃ/, /ʒ/, /χ/, /ɣ/, /ħ/, etc.
  - Phénotypie linguistique rare cross-linguistiquement
  - Résultat : spirantization historique (stops → fricatives)
  
- **Secondary articulations (overlaid features)** :
  - **Pharyngealisés/Emphathiques** : ṭ [tˤ], ḍ [ðˤ], ṣ [sˤ], ẓ [zˤ], ṛ [rˤ]
    - Changements formantiques : F1 raised, F2 lowered, vowels influenced [55]
  - **Labialisés** : k͡ʷ, q͡ʷ, x͡ʷ, ɣ͡ʷ
    - Lip rounding + velar/uvular
    - Interdit certaines combinaisons dans mots (coarticulation constraint)

- **Contraste fricative/stop variable par dialecte** :
  - Western Kabyle : fricatives dominantes (b→β, d→ð, g→ʝ)
  - Eastern Kabyle : mix stops/fricatives
  - Orthography challenge : single letter peut = fricative OR stop

**Implications NLP** :
- IPA annotation **MUST** explicitement marquer emphathique/labialisé
- Phonemic vs. phonetic transcription distinction critique
- ASR tokenizer doit capturer secondarticulations

#### 2. Système Vocalique Minimale

Seuls 3 voyelles phonémiques : /i/, /a/, /u/ [16][37]

- Schwa [ə] épenthétique fréquent (pas phonémique, orthographié ⟨e⟩)
- Réalisations phonétiques influencées consonnes emphathiques :
  - [aẓru] 'stone' vs. [æmud] 'seed' (vowel quality shift)

#### 3. Syllable Structure Remarquable : Mots Sans Voyelles

**Phénomène unique cross-linguistiquement** [17][21][57][60] :

Tashlhiyt permet structure syllabique TRÈS permissive :
- V (vowel alone)
- CV, CVC (normal)
- CC, CCC (consonant clusters without vocalic nucleus)
- **Entire words consonant-only** : [rɡl] 'close!', [tskːststː] 'you took it (F)'

**Mécanisme phonologique** :
- Sonority plays key role : sonorants (nasals, liquids) peuvent nuclèi
- Obstruents peuvent être noyau si dans structure spécifique
- NOT just schwa : real vowelless syllables phonetiquement
- Listeners Tashlhiyt perçoivent comme multisyllabique (consonants hétérosyllabic)[57]

**Implication ASR** :
- Syllabification rules non-standard
- Force-alignment à phoneme level problématique
- Need explicit rule-based syllabifier ou hand-annotation

---

### B. Morphologie Nonconcatenative (Root-Template)

#### 1. Structure Racine-Gabarit Canonique

Berber morphology = **root-template (vocalic melody) system** [56][59] :

```
Example : Tamazight verb 'sleep'
├─ Root (consonantal skeleton) : f-d-s (3 consonants)
├─ Template (vocalic melody) : i-u (2 voyelles)
├─ Combination → [i-f-d-u-s] = ifds 'he sleeps'

Comparaison West Semitic:
├─ Arabic √k-t-b + template a-i = katib 'writer'
├─ Kabyle √f-k + template i-u = ifuk 'he learned'
```

**Ramifications** :
- Morphemes NOT contiguous dans surface form
- Standard word boundaries (spaces) insufficient for morphology
- Affixes (prefixes, suffixes, infixes) S'AJOUTENT à root-template base

#### 2. Classes Verbales Aspectuelles

Verbes Kabyle = classés par aspect (Tense-Aspect distinctions)[56] :

| Aspect | Fonction | Exemple |
|--------|----------|---------|
| **Aorist** | Default, non-tendu | af 'he takes' |
| **Perfective** | Past completed action | yffa 'he took' |
| **Imperfective** | Habitual/progressive | ifa 'he used to take' |
| **Negative Perfective** | Negated past | ur yffa 'he didn't take' |

- Distinctions marquées par vocalic melody + preverbs (particle ad)
- Prefix+ : a- (perfective), i- (imperfective), y- (3.M aorist)

**Challenge NLP** :
- Aspect/tense encoded ACROSS morpheme boundaries
- Simple POS tags insufficient - need complex morphosyntactic features
- Universal Dependencies morphology module needs extension

#### 3. Genre, Nombre, État

Nom Kabyle système incluent :
- **Gender** : Masculine, Feminine
  - Suffix -t for feminine typically : tamdint 'city' (FEM) vs. tamda 'ground' (MASC)
  - Prefix a- determiner for most nouns
  
- **Number** : Singular, Plural
  - Prefixes/suffixes + ablaut vocalique change simultaneously
  - Complex internal vowel changes (non-concatenative again)
  
- **"État" (construct state)** : Nominatif vs. annexation state
  - Used post-prepositions, numerals, possess constructions

---

### C. Contact Linguistique et Emprunt

#### 1. Pervasive Arabic Loanwords

**Fait établi linguistiquement** [33][34][35] :
- >20% loanwords dans TOUS domaines sémantiques Tarifiyt (Berber sud)
- Pervasive across Kabyle aussi - même mots corpus

**Patterns morphologiques d'intégration** [38] :
- **Integrated loanwords** : adoptent morphologie Berbère
  - Exemple : l'arabe qəlb 'heart' → Kabyle aqəlb (+ préfixe a-)
  - Héritent genre Berbère parfois
  
- **Non-integrated loanwords** : garde déterminant source l- (Arabic al-)
  - Exemple : l-tomobil 'automobile' (non-adapted)
  - Gardent phonologie source plus souvent

**Implication ASR** :
- Loanword detection + source language identification necessary
- Different morphosyntactic rules s'appliquent selon integration type
- Code-switching markers needed

#### 2. Code-Switching Amazigh-Arabic-French

Phénomène sociolinguistique courant Béjaïa/Alger [34] :

**Patterns observés** :
- Tamazight matrix language + Arabic embedded language typically
- French occasionnel dans youth urban contexts
- **Morphosyntactic influence** : Arabic clitic systems sometimes borrowed
- **Lexical switching** : Domaines prestigieux (tech, education) → French/Arabic

**Pourquoi pertinent ASR** :
- Sentence peut avoir 3 langues dans 10 secondes
- Acoustic models standard fail on code-switching
- Need specialized tokenization + per-language ASR components

---

## III. Ressources NLP Existantes pour Kabyle/Amazigh

### A. Modèles Pré-entrainés

#### 1. DziriBERT : Transformer pour dialecte Algérien

**Papers** : [48][51]

Framework : Transformer BERT pré-entraîné spécifiquement sur dialecte algérien (Darja)

**Spécificités** :
- Handle Arabizi (Latin script representation Darja)
- Multilingual training data mix (French, English, Wikipedia)
- 150 MB training data = **sufficient pour compétitive performance vs. gros modèles**

**Performance** :
- SOTA sur sentiment analysis Algérien (63.5% accuracy topic classification vs. 49% mBERT)
- Gère script diversity

**Limitations** :
- Token-based (subword) tokenization problème pour morphologically-rich
- Doesn't explicitly capture Kabyle phonology/secondary articulations
- Dialecte focus = Darja (plus Arabic-influenced) vs. Kabyle pur

#### 2. chDzDT : Character-level Morphology-Aware LM

**Paper** [54]

Novel approach : **character-level encoding** plutôt que token-level

**Motivation** :
- Standard tokenizers (BPE, WordPiece) découpe mots agglutinatives inconsistently
- Morpheme boundaries ignorés
- Character-level captures morphological patterns robustement

**Résultats** :
- Better morphological encoding Algérien
- Multilingual training (Arabic, Latin, French, Tifinagh script)
- Potentiel pour Kabyle dialect aussi

**Limitation** : Pas Kabyle-specific encore.

### B. Corpus et Data Collection Initiatives

- **Mozilla Common Voice** : collecte crowdsourced speech Amazigh (incomplete)
- **Amazigh corpus projects** : fragmentés, no standardization (Tamazight vs. Tarifit vs. Kabyle splits problématique)
- **Academic collections** : small, no public access

---

## IV. Défis Spécifiques pour Kabyle ASR et NLP

### A. Phonologiques

1. **Consonant-only words syllabification** : Besoin explicit rule-based ou hand-annotation
2. **Secondary articulation marking** : Emphasis + labialization pas standard phonetically
3. **Regional spirantization variation** : Different phonetic realizations par sous-dialect
4. **Fricative/stop contrast ambiguity** : Orthography challenge

### B. Morphologiques

5. **Root-template non-linear encoding** : ASR tokenizer standard inadapté
6. **Loanword integration variation** : Multiple morphosyntactic rules co-exist
7. **High morpheme-per-word agglutination** : Tokens très longs, vocabulary explosion

### C. Dialectales et Sociolinguistiques

8. **Variation dialectale systematic** : Eastern vs. Western Kabyle phonological differences
9. **Code-switching trilingue** : Amazigh-Arabic-French mélange fréquent
10. **Limited speaker pool** : Few trained transcribers available

### D. Ressources et Technicité

11. **Corpus fragmenté** : Pas standardization orthography/annotation
12. **Données limitées** : 10-50 heures parlant réelle typically
13. **ASR low-resource challenges** : Fine-tuning strategies + transfer learning essential

---

## V. Framework Proposé : Intégration Solutions Éprouvées

### A. Annotation Tier Architecture (ELAN)

Hiérarchie multi-tier capturant toutes dimensions linguistiques :

```
Audio/Video base layer
│
├─ Tier 1: ORTHOGRAPHY (Tifinagh IRCAM standard)
│  │
│  ├─ Tier 2: IPA PHONETIC (with Berber-specific notation)
│  │  ├─ Tier 2a: EMPHASIS marker [+/- emphatic]
│  │  └─ Tier 2b: LABIALIZATION marker [+/- labialized]
│  │
│  ├─ Tier 3: MORPHOLOGICAL SEGMENTATION
│  │  ├─ Tier 3a: ROOT (consonantal skeleton)
│  │  ├─ Tier 3b: TEMPLATE (vocalic melody)
│  │  ├─ Tier 3c: AFFIXES (prefixes/suffixes/infixes)
│  │  └─ Tier 3d: GEMINATION [+/- long]
│  │
│  ├─ Tier 4: POS TAGS (Universal Dependencies adapted)
│  ├─ Tier 5: MORPHOSYNTACTIC FEATURES (gender, number, aspect, tense, etc.)
│  ├─ Tier 6: SYNTACTIC DEPENDENCIES (basic head-dependent relations)
│  ├─ Tier 7: LOANWORD FLAG [+/-] + SOURCE LANGUAGE
│  ├─ Tier 8: DIALECT/REGIONAL MARKING
│  ├─ Tier 9: CODE-SWITCHING FLAGS (language transitions)
│  └─ Tier 10: METADATA & NOTES
```

**Advantages** :
- Hierarchical parent-child relationships enable automatic dependent tier validation
- Controlled vocabularies prevent typos, enable quantitative analysis
- Export ELAN .eaf → CoNLL-U → UD-compatible
- Full audio synchronization maintained throughout annotation

### B. CoNLL-U Format avec Extensions Kabyle

```conllu
# sent_id = kab-001
# text = taqcict d tamacahut
# lang = kab
# dialect = western_kabyle
# recording_date = 2025-01-20
# speaker_id = SPK-001-Female-30yo
# code_switch = amazigh-only
#
1	ta	a	DET	DET	_	2	det	_	Lemma=ta;Gloss=DEFEM
2	q	q	ROOT	ROOT	_	3	nmod	_	Lemma=q;Root=q;Gloss=GIRL
3	-cict	-ct	SUFF	SUFF	Gender=Fem|Number=Sing	2	case	_	Lemma=-ct;Morpheme_type=diminutive
4	d	d	CCONJ	CCONJ	_	6	cc	_	Lemma=d;Gloss=AND
5	ta	a	DET	DET	_	6	det	_	Lemma=ta;Gloss=DEFEM
6	macahut	m-c-h	ADJ	ADJ	Gender=Fem|Number=Sing|Root=m-c-h|Template=a-u	3	conj	_	Lemma=m-c-h;Gloss=beautiful;Morphtype=nonconcatenative

```

**Custom FEATS fields** :
- `Root` : 3-consonant radical
- `Template` : vocalic melody pattern
- `Morphtype` : {concatenative, nonconcatenative, loanword}
- `Emphasis` : [+/-emphatic]
- `Labialized` : [+/-labialized]
- `Loanword_source` : {arabic, french, other}
- `Syllabic` : [+/-syllabic_consonant] for consonant-only words

---

## VI. Cas d'Études Analogues : Leçons Apprises

### A. Swiss German (Low-Resource Dialect)

**Context** : Dialecte parlé Suisse sans ressources NLP établies.[77]

**Solution** :
- Whisper fine-tuning avec data generation
- Sentence-level data → long-form audio via synthetic noise + timestamp correction
- Mix local Swiss German + multilingual FLEURS data

**Résultats** : SOTA STT pour Swiss German avec limited data

**Applicabilité Kabyle** : Même setup (mix local + multilingual sources) optimal pour Kabyle

### B. Amharic (Agglutinative, Low-Resource)

**Context** : Langue morphologically-rich Ethiopie, peu ressources.[71]

**Challenges** :
- Agglutination → vocabulaire explosion si pas morphologically-aware
- Homophones nombreux

**Solution** :
- Whisper fine-tuning sur FLEURS + local Amharic data mix
- Homophone normalization step
- Best = FLEURS data + local data ensemble (not local-only)

**Applicabilité Kabyle** : Morphology handling strategies + data mixing directly transferable

### C. Neo-Aramaic (Endangered Semitic, Similar phonology)

**Context** : Dialecte menacé, few speakers, urgent documentation.[65]

**NoLoR Framework** :
1. Define phonemic orthography
2. Collect 35 minutes transcribed speech
3. Train Whisper ASR
4. Deploy community transcription tool

**Résultats** : 6.3× speedup transcription avec ASR assist, dataset public

**Applicabilité Kabyle** :
- Exact framework applicable
- Phonemic orthography decision (Tifinagh vs. Latin) = step 1
- 35-50 hours initial corpus sufficient

---

## VII. Méthodologie Implémentation : Protocole Detaillé

### A. Phase 1 : Préparation (Mois 1-2)

#### 1.1 Orthography Standardization Decision

**Critères décision** [86][89] :

| Dimension | Latin IRCAM | Tifinagh | Hybrid |
|-----------|------------|----------|--------|
| Technological usability | **High** (standard keyboard) | Medium (special fonts needed) | High |
| Cultural acceptability | High (familiar to speakers) | **Very High** (official Moroccan) | High |
| Linguistic adequacy | High (all phonemes representable) | High | **High** |
| Learnability | High | Medium | Medium |
| Typography support | Excellent | Good | Mixed |

**Recommendation pour Kabyle/Béjaïa** :
- Latin IRCAM standard pour ease of adoption
- Document fricative/stop contrast explicitly (e.g., t vs. tt for geminate, but fricative vs. stop indicated via diacritics or convention)
- Berber IRCAM Tifinagh as alternative/parallel representation

#### 1.2 Community Engagement

- Form consultation panel : native speakers, educators, linguists
- Obtain ethics approval (IRB/similar)
- Community consent + data ownership agreements

### B. Phase 2 : Data Collection (Mois 2-6)

#### 2.1 Recording Specifications

- **Target** : 50-100 hours Kabyle speech (diverse speakers, natural contexts)
- **Minimum initial** : 30 hours for ASR baseline
- **Speaker diversity** :
  - ≥5 speakers per dialect region (West, East)
  - Gender balanced if possible
  - Age range : 20-70yo
  - Education backgrounds

- **Audio specs** :
  - Mono, 16kHz sample rate
  - .wav format (uncompressed for annotation)
  - <10dB SNR (signal-to-noise ratio)
  - Natural speech preferred over read speech

- **Content types** :
  - Interviews (biographical, language attitudes, local knowledge)
  - Narratives (folktales, anecdotes)
  - Spontaneous conversation (if possible)
  - Elicited utterances (for phonological coverage)

- **Metadata captured** :
  - Speaker ID, age, gender, education level, native/near-native status
  - Dialect identification
  - Recording date, location, equipment model, ambient noise level
  - Speaker permission (audio publication, derivative use, community access restrictions)

#### 2.2 Manual Transcription

- First pass : orthographic transcription (Tier 1 orthography)
- Transcriber : native speaker or fluent L2 speaker with training
- Interrater reliability check : 10% overlap with second transcriber, target Cohen's kappa >0.80
- Tool : ELAN with orthography tier template

### C. Phase 3 : Annotation (Mois 6-12)

#### 3.1 Phonetic/Phonological Annotation

- Export orthographic ELAN → Praat TextGrid
- Force-align using acoustic model (if available, else manual segmentation)
- Phonetic transcription (IPA Berber notation) Tier 2
- Mark secondary articulations (Tier 2a emphasis, 2b labialization)

**Special handling** :
- Consonant-only words : explicit syllable boundary marking
- Emphasis detection : Visual inspection F1/F2 formants via Praat

#### 3.2 Morphological Segmentation

- Root-template analysis (Tiers 3a-3d)
- Affix identification + classification
- Gemination marking
- Cross-check against morphological literature (Kossmann, Ouali, Mihuc)

#### 3.3 POS & Morphosyntactic Annotation

- Assign POS tags (UD Universal : NOUN, VERB, ADJ, etc.)
- Add morphosyntactic features : Gender, Number, Case, Aspect, Tense
- Identify syntactic dependencies (basic relations)

**Approach** :
- Start automatic via morphological rules + statistical taggers
- Manual review + correction by linguist
- Interrater agreement benchmark

#### 3.4 Loanword & Code-switching Markup

- Flag loanwords : Tier 7 [+/-] + source language
- Mark code-switching transitions : Tier 9
- Track integration type : integrated (a-) vs. non-integrated (l-)

### D. Phase 4 : Quality Control (ongoing)

- **Consistency checks** : Automatic validation scripts (duplicate morphemes, POS inconsistencies)
- **Interrater agreement** : 20% sample review by second annotator
- **Speaker feedback** : Occasional playback review with speakers (cultural validation)

### E. Phase 5 : Data Export & Archival (Mois 12+)

#### 5.1 Format Conversion

- ELAN .eaf → CoNLL-U format (via speach library + custom Python script)
- Validation : CoNLL-U parsing checks
- UD-compatible format for potential contribution

#### 5.2 Archival

- **Primary archive** : ELAR (Endangered Languages Archive, SOAS)
- **Secondary** : Zenodo (open-access, citable DOI)
- **Institutional** : Local backup Université Béjaïa
- **Metadata** : OLAC-compliant entry
- **Licenses** : CC-BY-SA or institution-specific if community preference

#### 5.3 Derived Resources

- Frequency lexicon (lemmas + morphology)
- Pronunciation dictionary (orthography → IPA)
- Morphological rules documentation
- Treebank statistics report

---

## VIII. ASR Fine-tuning Strategy

### A. Model Selection & Baseline

**Recommendation** : OpenAI Whisper (Large model)

**Rationale** :
- Multilingual pre-training → better low-resource generalization[71]
- State-of-the-art on accent/dialect variation
- Publicly available, reproducible
- Fine-tuning guides widely available

**Alternative** : wav2vec 2.0 (fine-tuned on target language)

### B. Data Preparation

#### B.1 Mixing Strategy

Based on Amharic success [71] :

```
Training data composition:
├─ Local Kabyle corpus : 50 hours (YOUR annotated data)
├─ Mozilla Common Voice Kabyle : ~10 hours (if available)
├─ Multilingual FLEURS data : 5 hours (cross-lingual regularization)
└─ Optional : Synthetic data augmentation (noise, pitch shift)
```

**Rationale** :
- Local-only → overfitting to speakers/acoustic conditions
- Multilingual mix → prevents catastrophic forgetting
- Cross-lingual → improves robustness to variation

#### B.2 Data Preprocessing

- Normalize orthography (consistent space/punctuation)
- Segment long utterances (>15 seconds) into sentences
- Augment long-form audio via concatenation (for Swiss German technique)[77]
- Apply SpecAugment (frequency masking) randomly

### C. Fine-tuning Configuration

```python
# Pseudocode Whisper fine-tuning
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")
processor = WhisperProcessor.from_pretrained("openai/whisper-large")

# Freeze encoder (optional, for low data)
for param in model.encoder.parameters():
    param.requires_grad = False

# Training args
training_args = {
    'learning_rate': 1e-5,
    'warmup_steps': 500,
    'num_train_epochs': 3,
    'batch_size': 4,  # adjust for GPU memory
    'gradient_accumulation_steps': 4,
    'weight_decay': 0.01,
    'save_strategy': 'epoch',
    'eval_strategy': 'epoch',
    'metric_for_best_model': 'wer',
    'load_best_model_at_end': True,
}

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_wer,  # Word Error Rate
    ...
)
trainer.train()
```

### D. Evaluation & Benchmarking

**Metrics** :
- Word Error Rate (WER) overall + by dialect
- Character Error Rate (CER)
- Morpheme-level accuracy (important for Kabyle!)
- Robustness : performance on held-out speakers, noise conditions, dialects

**Ablations** :
- Freeze encoder vs. fine-tune full model
- Multilingual data impact
- Emphasis marking impact (if acoustic model captures)

---

## IX. Recommendations Prioritaires pour Thèse Kabyle ASR

### Court Terme (6 mois)

1. **Orthography decision** + community consensus
2. **Recording protocol setup** (40-60 heures, speaker diversity)
3. **ELAN template creation** avec 10+ tiers standardisés
4. **Interrater reliability pilote** (sample annotations)

### Moyen Terme (12 mois)

5. **Full corpus annotation** (orthography → morphology → POS → loanwords)
6. **CoNLL-U export** + validation
7. **Whisper fine-tuning baseline** (local data + multilingual mix)
8. **WER benchmarking** by dialect

### Long Terme (18-24 mois)

9. **Community tool** (web interface for speakers)
10. **Morphology-aware tokenizer** (MIASEG or BPE optimization)
11. **Pre-trained language model** (Kabyle-specific if corpus >150 MB)
12. **Corpus archival** (ELAR + Zenodo) with metadata

---

## X. Conclusion

La documentation linguistique du Tasahlit pour NLP/ASR est réalisable même sous contraintes ressources, via :

1. **Frameworks standardisés** (UD, CoNLL-U, ELAN, IPA Berber) adaptés aux complexités Kabyle
2. **Methodologies éprouvées** (DOBES, NoLoR, ELDP, ethical fieldwork) pour endangered languages
3. **Technology appropriée** (Whisper fine-tuning, morphology-aware encoding, hybrid human-AI annotation)
4. **Community engagement** fondamental (ethical principles, speaker empowerment)

**Points critiques résolvables** :
- Phonologie complexe (consonant-only words, secondary articulations) → explicit annotation frameworks
- Morphologie nonconcatenative → root-template encoding + CoNLL-U FEATS extension
- Ressources limitées → transfer learning (multilingual pre-training mix) + data augmentation
- Variation dialectale → systematic metadata + dialect-specific evaluation

**Défis humanistes prioritaires** :
- Standardisation orthography = décision communautaire
- Speaker empowerment via community tools
- Long-term preservation via international archives
- Capacity building : train local transcribers/annotators

Avec cette approche intégrée, une documentation Kabyle scientifiquement robuste, techniquement reproductible, et socialement responsable est achievable dans 18-24 mois avec équipe petite mais dévouée.

---

## Références Principales

### Frameworks & Standards
[1] Universal Dependencies: https://universaldependencies.org/
[25] Nivre et al. (2020) UD v2
[31] Croft (2006) Linguistic typology
[40][42] IPA for Berber
[87] CoNLL-U format documentation

### Tools & Software
[47][53] ELAN (EUDICO Linguistic Annotator)
[50] speach library (Python)

### Kabyle/Berber Linguistics
[16] Kenstowicz (1987), Kabyle phoneme inventory
[17][20][21] Tashlhiyt syllable structure
[37] Kabyle consonants
[38][39] Mihuc (2020) Kabyle noun-initial a
[56] Ouali (2020) Verb morphology Tamazight
[59] Kossmann Berber morphology

### ASR & Low-Resource NLP
[48][51] DziriBERT (Algerian dialect)
[54] chDzDT (character-level Algérien)
[65] NoLoR framework (Neo-Aramaic)
[71] Fine-tuning Whisper Amharic
[74][77] Whisper fine-tuning low-resource languages

### Endangered Language Documentation
[64] Dwyer (2011) Tools for endangered language assessment
[67] DOBES program (language documentation)
[70] Austin (2007) Language documentation principles
[81] ELDP training resources

### Ethical Fieldwork
[80][83] Ethical principles linguistic fieldwork
[84] Language revitalization protocols

### Orthography Design
[86] Creating orthographies endangered languages
[89] Writing endangered language (Guérin 2008)
[92] Phonemic orthography design (Enets case)

