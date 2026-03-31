# Pipeline ML — DGPC Béjaïa (PFE Master Data Science)

## Architecture

Ce pipeline traite des appels d'urgence de la Protection Civile de Béjaïa
(kabyle avec code-switching français/arabe, en écriture Arabizi).

## Scripts (ordre d'exécution)

### Partie 1 : ASR (Whisper)
| Script | Rôle | Exécution |
|--------|------|-----------|
| `00_prepare_asr_manifest.py` | Charge les segments, nettoie le texte, split train/val/test | Local ✅ |
| `01_build_hf_asr_dataset.py` | Construit le Dataset HuggingFace (Mel + Tokens) | Colab recommandé |
| `02_train_whisper.py` | Fine-tune Whisper-small avec Seq2SeqTrainer | Colab GPU requis |

### Partie 2 : Extraction structurée (Qwen 2.5)
| Script | Rôle | Exécution |
|--------|------|-----------|
| `03_prepare_qwen_extraction_dataset.py` | Transforme le CSV annoté en instruction-tuning ChatML | Local ✅ |
| `04_train_qwen_qlora.py` | Fine-tune Qwen 2.5-7B avec QLoRA 4-bit | Colab GPU T4+ |

### Partie 3 : Baseline BERT
| Script | Rôle | Exécution |
|--------|------|-----------|
| `05_prepare_bert_dataset.py` | Prépare classification incident_type + urgency_human | Local ✅ |
| `06_train_bert_classifier.py` | Fine-tune BERT multilingual avec poids de classe | Colab GPU |

## Utilisation sur Google Colab

1. Uploader le dossier `Training/` sur Google Drive
2. Ouvrir un notebook Colab
3. Copier-coller les cellules (`# %%`) de chaque script
4. Les chemins s'adaptent automatiquement (détection Colab)

## Fichiers obsolètes (à ignorer)
- `01_forced_alignment_pro.py` — ancien brouillon
- `02_dataset_builder_hf.py` — ancien brouillon
