# 🚀 CHEAT SHEET - Commandes Rapides Pipeline 506+

## ⚡ Une Seule Ligne (Copy-Paste)

### Démarrage Menu Interactif
```bash
python pipeline_menu.py
```

### Transcrire 506-809 (Whisper)
```bash
python transcribe_from_506.py --start 506
```

### Transcrire 506-520 (test rapide)
```bash
python transcribe_from_506.py --start 506 --end 520
```

### Transcrire avec Qwen3-ASR (Kabyle optimisé)
```bash
python transcribe_qwen3_from_506.py --start 506
```

### Transcrire + Auto-lancer annotation
```bash
python transcribe_from_506.py --start 506 --auto-launch
```

### Lancer Annotation seule
```bash
cd annotation_app && streamlit run dgpc_annotation_local.py
```

### Vérifier Health Check
```bash
python check_health.py
```

### Voir Architecture Visuelle
```bash
python ARCHITECTURE_VISUELLE.py
```

---

## 📊 Voir Résultats

### Compter appels dans dataset
```bash
python -c "import pandas as pd; df = pd.read_csv('dataset/506_onwards_transcriptions.csv'); print(f'Appels: {len(df)}')"
```

### Afficher premières lignes
```bash
python -c "import pandas as pd; print(pd.read_csv('dataset/506_onwards_transcriptions.csv').head())"
```

### Exporter en JSON
```bash
python -c "import pandas as pd; pd.read_csv('dataset/506_onwards_transcriptions.csv').to_json('data.json', orient='records', indent=2)"
```

### Exporter en Excel
```bash
python -c "import pandas as pd; pd.read_csv('dataset/506_onwards_transcriptions.csv').to_excel('data.xlsx')"
```

---

## 🔧 Installation

### Installer tout d'un coup
```bash
pip install openai-whisper qwen-asr google-generativeai streamlit pandas pydub python-dotenv
```

### Juste Whisper
```bash
pip install openai-whisper
```

### Juste Qwen3-ASR
```bash
pip install qwen-asr
```

### Juste annotation
```bash
pip install streamlit google-generativeai pandas pydub
```

---

## 🖱️ Double-Cliquer (Sans Terminal)

```
LancerMenu.bat                    ← Menu complet ✅
run_transcription_506.bat         ← Whisper
run_qwen3_transcription_506.bat   ← Qwen3-ASR
check_health.bat                  ← Vérification
```

---

## 🐛 Dépannage Rapide

### Erreur: Module not found
```bash
pip install -r requirements.txt  # Installation ALL
python check_health.py           # Voir ce qui manque
```

### Whisper hors mémoire
```bash
python transcribe_from_506.py --start 506 --end 520  # Batch plus petit
```

### Qwen3 hors mémoire
```bash
python transcribe_qwen3_from_506.py --use-cpu  # Mode CPU
```

### Transcription trop lente
```bash
python check_health.py  # Vérifier GPU
nvidia-smi              # Voir GPU stats
```

---

## 📊 Workflow Typique (Copy-Paste)

### 1. Vérifier Setup
```bash
python check_health.py
```

### 2. Tester sur 5 appels
```bash
python transcribe_from_506.py --start 506 --end 510
```

### 3. Voir résultats
```bash
python -c "import pandas as pd; print(pd.read_csv('dataset/506_onwards_transcriptions.csv').head())"
```

### 4. Si OK → Lancer complet
```bash
python transcribe_from_506.py --start 506
```

### 5. Après transcription → Annotation
```bash
python pipeline_menu.py  # Option 3
```

---

## 🎯 Options Avancées

### Whisper avec spécification GPU
```bash
# Force GPU 0
CUDA_VISIBLE_DEVICES=0 python transcribe_from_506.py --start 506

# Force CPU
python transcribe_from_506.py --start 506 --use-cpu
```

### Qwen3 verbose output
```bash
python transcribe_qwen3_from_506.py --start 506 -v  # Mode verbose
```

### Pipeline avec logging
```bash
python transcribe_from_506.py --start 506 2>&1 | tee transcription.log
```

---

## 📁 Fichiers Importants

| Chemin | Contenu |
|--------|---------|
| `audio_processed/appelle 506.wav` | Audioà transcrire |
| `dataset/506_onwards_transcriptions.csv` | Résultat |
| `annotation_app/.env` | API keys (Gemini) |
| `augmentation/` | Correcteur Kabyle |

---

## 🔗 Ressources

- **Whisper docs:** https://github.com/openai/whisper
- **Qwen3-ASR:** https://huggingface.co/Qwen/Qwen3-ASR-1.7B
- **Pandas docs:** https://pandas.pydata.org/docs/
- **Streamlit docs:** https://docs.streamlit.io/

---

## ✨ Tips & Tricks

```bash
# Kill Streamlit (si bloqué)
pkill -f streamlit

# Vider cache Streamlit
streamlit cache clear

# Voir tout fichiers audio
ls audio_processed/appelle *.wav | wc -l

# Voir taille dataset
wc -l dataset/506_onwards_transcriptions.csv

# Benchmark GPU
python -c "import torch; print(torch.cuda.get_device_properties(0))"
```

---

## 🚀 Production Deploy (Avancé)

### Batch nocturne (Windows Task Scheduler)
```
Tâche: C:\Python\python.exe
Args: C:\path\transcribe_from_506.py --start 506
Horaire: 22:00 (tous les jours)
```

### Cron (Linux)
```bash
# Ajouter à crontab -e
0 22 * * * cd /path && python transcribe_from_506.py --start 506
```

### Docker
```bash
# Dockerfile à créer
FROM python:3.10
RUN pip install -r requirements.txt
CMD ["python", "transcribe_from_506.py", "--start", "506"]
```

---

## 📞 Quick Support

**Q: Je veux juste tester?**
```bash
python transcribe_from_506.py --start 506 --end 510
```

**Q: Combien de temps?**
- Whisper: 5s/appel (GPU) = 25 min pour 304 appels
- Qwen3: 10s/appel (GPU) = 50 min pour 304 appels
- CPU: +10x plus lent

**Q: Puis-je arrêter et reprendre?**
Oui! Le script est safe, vous pouvez relancer sans risque

**Q: Doublonnage de données?**
Non! Safe merge automatique par ID

---

**Version:** 1.0.0  
**Last Updated:** 4 Mars 2026  
**Status:** ✅ Production Ready 🚀
