# Pipeline de Pretraitement des Donnees Reelles DGPC Bejaia

## Contexte
Pipeline d'alignement force pour extraire des segments (audio, texte) a partir de 622 appels d'urgence enregistres par la DGPC Bejaia. Les appels contiennent du kabyle dialecte Bejaia avec code-switching francais et arabe.

## Probleme resolu
Les transcriptions sont des conversations completes (2 locuteurs) sans timestamps. Il fallait aligner le texte sur l'audio pour obtenir des segments utilisables pour le fine-tuning ASR.

## Methode : MMS Forced Alignment
- **Modele** : `torchaudio.pipelines.MMS_FA` (MMS-300m, 1100+ langues)
- **Principe** : CTC character-level alignment — donne le texte complet + audio complet, trouve OU chaque mot est prononce
- **Pourquoi MMS** : language-agnostic au niveau caractere, gere le kabyle + francais + arabe sans config speciale

## Fichiers

### Scripts
| Fichier | Role |
|---------|------|
| `generate_forced_alignment_colab_notebook.py` | Generateur Python du notebook Colab |
| `forced_alignment_colab.ipynb` | Notebook Colab a executer (genere par le script ci-dessus) |
| `generate_collecte_verify_notebook.py` | Generateur du notebook de verification des anciennes collectes |
| `verify_collecte_colab.ipynb` | Notebook Colab pour verifier les collectes ambigues |

### Donnees source
| Fichier | Contenu |
|---------|---------|
| `Donnee_reel.csv` | 622 appels DGPC avec colonnes File (nom fichier audio) et Transcription (conversation complete) |

### Resultats de l'alignement
| Fichier | Contenu |
|---------|---------|
| `segments_asr_ready.jsonl` | **980 segments** gold+silver, prets pour le fine-tuning (2.65h) |
| `segments_gold.jsonl` | 98 segments haute confiance (score >= 0.3, duree >= 3s) |
| `segments_silver.jsonl` | 882 segments bonne confiance (score >= 0.1, duree >= 1.5s) |
| `segments_reject.jsonl` | 744 segments rejetes (score trop bas ou duree trop courte) |

### Audio aligne (non inclus ici, sur Google Drive)
- `aligned_wavs.zip` : WAV 16kHz mono, un fichier par segment
- Taille : ~626 MB

## Pipeline detaille

### Cell 1 : Installation
- Installe soundfile et librosa
- Utilise numpy 2.x natif de Colab (ne pas downgrader)

### Cell 2 : Upload donnees
- Monte Google Drive
- Upload CSV + dossier audio des appels

### Cell 3 : Parser de tours de parole
- 4 formats detectes : labeled (P:/C:), em_dash, inline_dash, ellipsis
- `detect_first_speaker()` : determine si le premier tour est caller ou operator
- `make_alternating()` : assigne les roles en alternance

### Cell 4 : Normalisation du texte pour l'alignement
- Arabizi digrams : ch->sh, gh->gh, kh->kh
- Arabizi contextuel : 7->h, 3->a, 9->k (seulement si colle a une lettre)
- Chiffres isoles -> mots francais (0->zero, 1->un, etc.)
- Suppression ponctuation et caracteres non-alpha

### Cell 5 : Chargement MMS-FA
- `torchaudio.pipelines.MMS_FA` : modele, tokenizer, aligner
- GPU CUDA, sample rate 16kHz

### Cell 6 : Alignement par chunks
- Fusionne les tours adjacents en chunks de ~12 secondes max
- Aligne le texte normalise sur l'audio complet
- Calcule les timestamps par mot via `fa_aligner(emission, tokenized)`
- Decoupe l'audio aux frontieres des chunks
- Qualite : gold (score>=0.3, dur>=3s), silver (score>=0.1, dur>=1.5s), reject

### Cell 7 : Traitement des 622 appels
- Boucle sur tous les appels du CSV
- Stats intermediaires toutes les 20 appels

### Cell 8 : Export JSONL + WAV
- Sauvegarde segments par qualite en JSONL
- Sauvegarde audio segments en WAV 16kHz

### Cell 9 : Copie vers Google Drive

## Statistiques finales

| Metrique | Valeur |
|----------|--------|
| Appels traites | 531 / 622 |
| Segments gold | 98 |
| Segments silver | 882 |
| Segments reject | 744 |
| **Total utilisable (gold+silver)** | **980** |
| **Duree totale utilisable** | **2.65h** |
| Duree moyenne par segment | 9.7s |
| Appels sans audio | 16 |
| Appels < 2 tours | 74 |
| Erreurs CTC | 12 |

## Execution
1. Ouvrir `forced_alignment_colab.ipynb` dans Google Colab
2. Activer GPU (Runtime > Change runtime type > A100 ou T4)
3. Executer toutes les cellules dans l'ordre
4. Temps d'execution : ~15-20 min sur A100
