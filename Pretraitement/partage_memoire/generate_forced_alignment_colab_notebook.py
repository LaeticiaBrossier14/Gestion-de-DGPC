"""
generate_forced_alignment_colab_notebook.py
============================================
Genere forced_alignment_colab.ipynb
Pipeline : MMS forced alignment (facebook/mms-300m) sur les appels DGPC.

Logique :
  1. Parser ameliore : labels (P/C/F/M/S1/S2/B/A/Op/Cal...) + split sur ... alternatif
  2. Normalisation arabizi -> latin pour MMS FA
  3. ctc-forced-aligner avec facebook/mms-300m (supporte kab)
  4. Timestamps mot par mot -> frontiere de tour -> decoupage audio
  5. Export gold/silver/reject JSONL + WAV -> Drive
"""

import json, os

NOTEBOOK_PATH = "forced_alignment_colab.ipynb"
cells = []

def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [text]})

def code(src):
    lines = src.split('\n')
    source = [l + '\n' for l in lines[:-1]] + [lines[-1]]
    cells.append({
        "cell_type": "code", "execution_count": None,
        "metadata": {}, "outputs": [], "source": source
    })

# ---------------------------------------------------------------------------
md("""# Forced Alignment DGPC — MMS (facebook/mms-300m)

**Objectif** : aligner mot-par-mot les transcriptions DGPC sur l\'audio complet
pour obtenir des segments audio/texte parfaitement alignes.

**Pipeline** :
1. Parser de tours ameliore (tous formats labels + `...` alternatif)
2. Normalisation arabizi -> latin pour MMS FA
3. `ctc-forced-aligner` + `facebook/mms-300m` (Kabyle supporte)
4. Timestamps par mot -> frontieres de tours -> extraction WAV
5. Export vers Google Drive

**GPU requis** : T4 minimum, A100/H100 recommande pour vitesse.
""")

# ---------------------------------------------------------------------------
code("""# Cell 1 : Installations
import subprocess, sys

import subprocess, sys
# Ne pas toucher numpy - utiliser la version Colab (2.x)
for pkg in ['soundfile', 'librosa']:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg], check=False)

import torch, torchaudio, numpy as np
gpu  = torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE'
vram = torch.cuda.get_device_properties(0).total_memory / 1e9 if torch.cuda.is_available() else 0
print(f'GPU        : {gpu}')
print(f'VRAM       : {vram:.1f} GB')
print(f'numpy      : {np.__version__}')
print(f'torchaudio : {torchaudio.__version__}')
print('OK')
""")

# ---------------------------------------------------------------------------
code("""# Cell 2 : Monter Drive + localiser les donnees
from google.colab import drive
import os, zipfile
from pathlib import Path

drive.mount('/content/drive')

drive_base = Path('/content/drive/MyDrive')
zip_candidates = list(drive_base.rglob('segmentation_data.zip'))
print(f'ZIP trouves : {zip_candidates}')

DATA_DIR = Path('/content/seg_data')
DATA_DIR.mkdir(exist_ok=True)

if zip_candidates:
    zip_path = zip_candidates[0]
    print(f'Extraction de {zip_path} ...')
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(DATA_DIR)
    print('Extrait.')
else:
    print('ATTENTION : segmentation_data.zip non trouve dans Drive.')

wav_list = list(DATA_DIR.rglob('*.wav'))
csv_list = list(DATA_DIR.rglob('*.csv'))
print(f'WAV trouves : {len(wav_list)}')
print(f'CSV trouves : {[c.name for c in csv_list]}')

AUDIO_DIR = wav_list[0].parent if wav_list else DATA_DIR
CSV_PATH  = csv_list[0] if csv_list else None
print(f'AUDIO_DIR = {AUDIO_DIR}')
print(f'CSV_PATH  = {CSV_PATH}')
""")

# ---------------------------------------------------------------------------
code("""# Cell 3 : Parser de tours ameliore (tous formats, v3)
import re
from dataclasses import dataclass
from typing import List

@dataclass
class TextTurn:
    role: str   # 'caller' | 'operator' | 'unknown'
    text: str
    index: int = 0

# Labels : single letters only match with ':', multi-char with ':' or '.'
_OP_LABELS = {'operator', 'op', 'repondant', 'r', 'b', 'p', 's1', '7imaya'}
_CAL_LABELS = {'caller', 'cal', 'appelant', 'c', 'a', 'f', 'm', 's2'}
RE_LABEL = re.compile(
    r'(?:^|(?<=[^a-zA-Z0-9]))'
    r'(?:(?:Operator|Caller|Appelant|Repondant|Op|Cal)\\s*[:\\.]'
    r'|(?:S1|S2)\\s*:'
    r'|(?:R|B|P|C|A|F|M)\\s*:)',
    re.IGNORECASE
)

def detect_first_speaker(first_text):
    'Determine si le premier locuteur est caller ou operator.'
    t = first_text.lower().strip()
    # Operateur : formules institutionnelles en debut
    op_pats = [
        r'^(an3am|himaya|7imaya|l.?7imaya|les?\\s+pompiers|protection)',
        r'^oui\\s+(an3am|les?\\s+pompiers|himaya)',
    ]
    cal_pats = [
        r'^allo', r'^salam', r'^azul', r'^sbakhir',
        r'^(ya|a)\\s+(khouya|khoya|gma|agma)',
    ]
    for pat in op_pats:
        if re.search(pat, t): return 'operator'
    for pat in cal_pats:
        if re.search(pat, t): return 'caller'
    return 'caller'

def make_alternating(parts, first_role):
    'Cree des tours alternants.'
    r1, r2 = first_role, ('operator' if first_role == 'caller' else 'caller')
    return [TextTurn(role=r1 if i%2==0 else r2, text=p, index=i) for i, p in enumerate(parts)]

def parse_turns(text):
    'Parse les tours depuis tous les formats DGPC.'
    text = text.strip()
    if not text:
        return []

    # 1. Labels explicites
    if RE_LABEL.search(text):
        matches = list(RE_LABEL.finditer(text))
        if matches:
            turns = []
            before = text[:matches[0].start()].strip()
            if before and len(before) >= 2:
                turns.append(TextTurn(role='unknown', text=before, index=len(turns)))
            for mi, m in enumerate(matches):
                label = m.group().rstrip(':. ').strip().lower()
                if label in _OP_LABELS: role = 'operator'
                elif label in _CAL_LABELS: role = 'caller'
                else: role = 'unknown'
                start = m.end()
                end = matches[mi+1].start() if mi+1 < len(matches) else len(text)
                t = text[start:end].strip()
                if t and len(t) >= 2:
                    turns.append(TextTurn(role=role, text=t, index=len(turns)))
            if turns:
                return turns

    # 2. Em-dash
    if '\\u2014' in text:
        parts = [p.strip() for p in text.split('\\u2014') if p.strip()]
        if len(parts) >= 2:
            first = detect_first_speaker(parts[0])
            return make_alternating(parts, first)

    # 3. Inline dash
    if re.search(r'[\\s\\.\\?,!]\\s*-\\s*(?=[A-Za-z0-9])', text):
        parts = [p.strip() for p in re.split(r'[\\s\\.\\?,!]\\s*-\\s*(?=[A-Za-z0-9])', text) if p.strip()]
        if len(parts) >= 2:
            first = detect_first_speaker(parts[0])
            return make_alternating(parts, first)

    # 4. Ellipsis (2+ points) -> alternance
    dot_parts = [p.strip() for p in re.split(r'\\.{2,}', text) if p.strip()]
    if len(dot_parts) >= 3:
        first = detect_first_speaker(dot_parts[0])
        return make_alternating(dot_parts, first)

    # 5. Fallback
    return [TextTurn(role='unknown', text=text, index=0)]

# Test rapide
tests = [
    ('P: Allo 7imaya C: Salam 3likoum P: Dachou yellan?', 'P/C labels'),
    ('Allo...7imaya oui?... Salam 3likoum... Anda?', 'ellipsis'),
    ('B: 7imaya? A: Salam 3likoum', 'B/A labels'),
    ('S1: Zdakhel? S2: imsawen S1: D accord', 'S1/S2 labels'),
]
for text, fmt in tests:
    turns = parse_turns(text)
    print(f'[{fmt}] {len(turns)} tours')
    for t in turns:
        print(f'  [{t.role}] {t.text[:60]}')
    print()
""")

# ---------------------------------------------------------------------------
code("""# Cell 4 : Normalisation arabizi -> latin pour MMS FA
import re

# Arabizi contextuel : chiffre ENTOURE de lettres = arabizi
# Chiffre SEUL ou en groupe = vrai nombre -> converti en mot francais
# (prononces chiffre par chiffre en contexte urgence algerien)

ARABIZI_DIGRAM = [('ch', 'sh'), ('gh', 'gh'), ('kh', 'kh'), ('th', 'th')]
ARABIZI_SINGLE = {'3': 'a', '7': 'h', '9': 'k', '5': 'kh'}

# Chiffres prononces en francais digit-par-digit
DIGIT_WORDS = {
    '0': 'zero', '1': 'un', '2': 'deux', '3': 'trois',
    '4': 'quatre', '5': 'cinq', '6': 'six', '7': 'sept',
    '8': 'huit', '9': 'neuf',
}

RE_CLEAN = re.compile(r'[,;:!?()\\[\\]{}\\u00ab\\u00bb"\\'\\u2026\\u2014\\_*#@&%$^~`]')

def is_arabizi(text, pos):
    'Un chiffre est arabizi ssi il touche une lettre (7imaya, sa7a, 3likoum).'
    before = text[pos-1] if pos > 0 else ' '
    after  = text[pos+1] if pos+1 < len(text) else ' '
    return before.isalpha() or after.isalpha()

def normalize_for_fa(text):
    'Normalise pour MMS forced aligner.'
    t = text.lower()

    # 1. Digrams arabizi
    for src, dst in ARABIZI_DIGRAM:
        t = t.replace(src, dst)

    # 2. Chiffres: arabizi -> lettre, vrais chiffres -> mots (prononciation locale)
    result = []
    for i, c in enumerate(t):
        if c in ARABIZI_SINGLE and is_arabizi(t, i):
            result.append(ARABIZI_SINGLE[c])
        elif c.isdigit():
            result.append(' ' + DIGIT_WORDS.get(c, '') + ' ')
        else:
            result.append(c)
    t = ''.join(result)

    # 3. Nettoyage
    t = RE_CLEAN.sub(' ', t)
    t = t.replace('-', ' ').replace('.', ' ')
    t = re.sub(r'[^a-z\\s]', '', t)
    t = re.sub(r'\\s+', ' ', t).strip()
    return t

# Test
samples = [
    ("Allo, 7imaya l'madaniya?", '7=arabizi -> h'),
    ('salam 3likoum les pompiers?', '3=arabizi -> a'),
    ('034 82 92', 'chiffres -> mots prononces'),
    ('rwa7em 9bala idhukh!', '7,9=arabizi'),
    ('Marki: 034- kemel - 08 77 14.', 'numero + mots'),
    ('g 2550 logements, le bloc 20.', 'adresse'),
    ("L'bloc 93 dachou yellan?", 'chiffres seuls'),
    ('sa7a merci', 'arabizi simple'),
]
for s, desc in samples:
    print(f'[{desc}]')
    print(f'  IN : {s}')
    print(f'  OUT: {normalize_for_fa(s)}')
    print()
""")

# ---------------------------------------------------------------------------
code("""# Cell 5 : Charger MMS_FA via torchaudio (API officielle, pas de package externe)
import torch, torchaudio
from torchaudio.pipelines import MMS_FA as bundle

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
SR = bundle.sample_rate  # 16000
print(f'Device    : {DEVICE}')
print(f'SR        : {SR}')

print('Chargement MMS_FA (facebook/mms-300m multilingual)...')
fa_model     = bundle.get_model().to(DEVICE)
fa_tokenizer = bundle.get_tokenizer()
fa_aligner   = bundle.get_aligner()
fa_model.eval()

print(f'Modele charge.')
if torch.cuda.is_available():
    print(f'VRAM utilisee: {torch.cuda.memory_allocated()/1e9:.1f} GB')
""")

# ---------------------------------------------------------------------------
code("""# Cell 6 : Fonctions alignement + extraction par chunks ~12s (torchaudio MMS_FA)
from pathlib import Path
import torchaudio, soundfile as sf
import numpy as np

TARGET_CHUNK = 12.0   # duree cible par chunk (secondes)
MIN_CHUNK    = 1.0    # minimum 1s
MAX_CHUNK    = 25.0   # max 25s (marge sous le 30s architectural)

OUT_DIR = Path('/content/aligned_segments')
OUT_DIR.mkdir(exist_ok=True)
(OUT_DIR / 'wavs').mkdir(exist_ok=True)

def load_audio(path):
    wav, orig_sr = torchaudio.load(str(path))
    if orig_sr != SR:
        wav = torchaudio.functional.resample(wav, orig_sr, SR)
    if wav.shape[0] > 1:
        wav = wav.mean(0, keepdim=True)
    return wav.squeeze(0)  # [T]

def align_call(audio_path, turns, call_name):
    wav = load_audio(audio_path)

    # Construire la liste de mots par tour
    fa_texts   = [normalize_for_fa(t.text) for t in turns]
    words_turn = [ft.split() for ft in fa_texts]
    all_words  = [w for ws in words_turn for w in ws]

    if len(all_words) < 3:
        return []

    try:
        with torch.inference_mode():
            emission, _ = fa_model(wav.unsqueeze(0).to(DEVICE))
    except Exception as e:
        print(f'  emissions error: {e}')
        return []

    try:
        tokenized = fa_tokenizer(all_words)
        word_spans = fa_aligner(emission[0], tokenized)
    except Exception as e:
        print(f'  alignment error: {e}')
        return []

    # ratio : echantillons par frame
    ratio = wav.shape[0] / emission.shape[1]

    def span_to_time(word_spans_list):
        t_start = word_spans_list[0].start * ratio / SR
        t_end   = word_spans_list[-1].end  * ratio / SR
        score   = float(np.mean([s.score for s in word_spans_list]))
        return t_start, t_end, score

    # --- Etape 1 : timestamps par tour ---
    turn_info = []
    word_off  = 0
    for turn, words in zip(turns, words_turn):
        n = len(words)
        if n == 0:
            turn_info.append(None)
            continue
        t_spans = word_spans[word_off : word_off + n]
        word_off += n
        if not t_spans:
            turn_info.append(None)
            continue
        t_start, _, _ = span_to_time(t_spans[0])
        _, t_end, _   = span_to_time(t_spans[-1])
        scores = [span_to_time(s)[2] for s in t_spans]
        turn_info.append({
            'turn': turn, 't_start': t_start, 't_end': t_end,
            'avg_score': float(np.mean(scores)),
        })

    valid = [ti for ti in turn_info if ti is not None]
    if not valid:
        return []

    # --- Etape 2 : fusionner en chunks de ~12s ---
    chunks  = []
    current = {'turns': [], 't_start': None, 't_end': None, 'scores': []}

    for ti in valid:
        dur_if_added = ti['t_end'] - (current['t_start'] or ti['t_start'])

        if current['turns'] and dur_if_added > TARGET_CHUNK:
            chunks.append(current)
            current = {'turns': [], 't_start': None, 't_end': None, 'scores': []}

        if current['t_start'] is None:
            current['t_start'] = ti['t_start']
        current['t_end'] = ti['t_end']
        current['turns'].append(ti['turn'])
        current['scores'].append(ti['avg_score'])

    if current['turns']:
        chunks.append(current)

    # --- Etape 3 : extraire audio et creer les resultats ---
    results = []
    for ci, chunk in enumerate(chunks):
        dur = chunk['t_end'] - chunk['t_start']
        if dur < MIN_CHUNK or dur > MAX_CHUNK:
            continue

        avg_score = float(np.mean(chunk['scores']))
        text = ' '.join(t.text for t in chunk['turns'])

        s0 = int(chunk['t_start'] * SR)
        s1 = min(int(chunk['t_end'] * SR), wav.shape[0])
        wav_name = f'{call_name}_c{ci:03d}.wav'
        sf.write(str(OUT_DIR / 'wavs' / wav_name), wav[s0:s1].numpy(), SR)

        quality = ('gold'   if avg_score >= 0.3 and dur >= 3.0 else
                   'silver' if avg_score >= 0.1 and dur >= 1.5 else 'reject')

        results.append({
            'text': text,
            'start': round(chunk['t_start'], 3),
            'end': round(chunk['t_end'], 3),
            'duration': round(dur, 3),
            'confidence': round(avg_score, 3),
            'quality': quality,
            'call_file': call_name,
            'chunk_index': ci,
            'n_turns': len(chunk['turns']),
            'audio': str(OUT_DIR / 'wavs' / wav_name),
        })

    return results

print('Fonctions alignement pretes (chunks ~12s, torchaudio MMS_FA).')
""")

# ---------------------------------------------------------------------------
code("""# Cell 7 : Traitement de tous les appels
import csv
from pathlib import Path
from collections import defaultdict

all_results = []
stats = defaultdict(int)

rows = []
with open(CSV_PATH, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f'Total appels dans CSV : {len(rows)}')

# Detecter les colonnes
col_file = next((k for k in rows[0].keys() if 'file' in k.lower()), 'File')
col_text = next((k for k in rows[0].keys() if 'transcript' in k.lower()), 'Transcription')
print(f'Colonnes : fichier={col_file!r}, texte={col_text!r}')
print()

for i, row in enumerate(rows):
    fname = row.get(col_file, '').strip()
    text  = row.get(col_text, '').strip()

    if not fname or not text:
        stats['skipped_empty'] += 1
        continue

    audio_path = Path(AUDIO_DIR) / fname
    if not audio_path.exists():
        found = list(Path(AUDIO_DIR).rglob(fname))
        if not found:
            found = list(Path(AUDIO_DIR).rglob(Path(fname).stem + '.wav'))
        audio_path = found[0] if found else None

    if not audio_path:
        stats['skipped_no_audio'] += 1
        continue

    turns = parse_turns(text)
    if len(turns) < 2:
        stats['skipped_few_turns'] += 1
        continue

    call_name = Path(fname).stem
    print(f'[{i+1}/{len(rows)}] {call_name} | {len(turns)} tours')

    try:
        results = align_call(audio_path, turns, call_name)
    except Exception as e:
        print(f'  ERREUR : {e}')
        stats['errors'] += 1
        continue

    for r in results:
        stats[f"quality_{r['quality']}"] += 1

    all_results.extend(results)
    stats['processed'] += 1

    if (i+1) % 20 == 0:
        g = stats['quality_gold']
        s = stats['quality_silver']
        r = stats['quality_reject']
        print(f'\\n  >> {i+1} traites | gold={g} silver={s} reject={r}\\n')

print()
print('=' * 50)
for k, v in sorted(stats.items()):
    print(f'  {k:30s}: {v}')
print(f'  Total segments : {len(all_results)}')
""")

# ---------------------------------------------------------------------------
code("""# Cell 8 : Export JSONL
from pathlib import Path
import json

OUT_DIR_P = Path('/content/aligned_segments')

gold   = [r for r in all_results if r['quality'] == 'gold']
silver = [r for r in all_results if r['quality'] == 'silver']
reject = [r for r in all_results if r['quality'] == 'reject']

for name, subset in [('gold', gold), ('silver', silver), ('reject', reject)]:
    path = OUT_DIR_P / f'segments_{name}.jsonl'
    with open(path, 'w', encoding='utf-8') as f:
        for r in subset:
            f.write(json.dumps(r, ensure_ascii=False) + '\\n')
    dur = sum(r['duration'] for r in subset) / 3600
    print(f'{name:8s}: {len(subset):5d} segments | {dur:.2f}h -> {path.name}')

asr_ready = gold + silver
asr_path = OUT_DIR_P / 'segments_asr_ready.jsonl'
with open(asr_path, 'w', encoding='utf-8') as f:
    for r in asr_ready:
        entry = {
            'audio': r['audio'],
            'text': r['text'],
            'duration': r['duration'],
            'quality': r['quality'],
            'call_file': r['call_file'],
        }
        f.write(json.dumps(entry, ensure_ascii=False) + '\\n')
print(f'ASR-ready: {len(asr_ready)} chunks -> {asr_path.name}')

g_dur = sum(r['duration'] for r in gold) / 3600
s_dur = sum(r['duration'] for r in silver) / 3600
print(f'\\nGold  : {len(gold)} ({g_dur:.2f}h)')
print(f'Silver: {len(silver)} ({s_dur:.2f}h)')
print(f'Total : {(g_dur+s_dur):.2f}h utilisable')
""")

# ---------------------------------------------------------------------------
code("""# Cell 9 : Sauvegarde vers Drive
import shutil, zipfile
from pathlib import Path

out_dir = Path('/content/aligned_segments')
drive_out = Path('/content/drive/MyDrive/aligned_segments_output')
drive_out.mkdir(parents=True, exist_ok=True)

for jsonl in out_dir.glob('*.jsonl'):
    shutil.copy2(jsonl, drive_out / jsonl.name)
    print(f'Copie : {jsonl.name}')

wav_dir = out_dir / 'wavs'
wav_files = list(wav_dir.glob('*.wav'))
zip_path = drive_out / 'aligned_wavs.zip'
print(f'Compression de {len(wav_files)} WAVs...')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for wav in wav_files:
        zf.write(wav, wav.name)
print(f'ZIP : {zip_path}')
print('Sauvegarde terminee dans Drive : aligned_segments_output/')
""")

# ---------------------------------------------------------------------------
code("""# Cell 10 : Verification ancien collecte - Upload ZIP
# Uploader le fichier 'collecte_ambiguous.zip' contenant :
#   - collecte_verify.csv (metadata)
#   - audios/*.webm (fichiers audio)
from google.colab import files
import zipfile
from pathlib import Path

print("Uploadez 'collecte_ambiguous.zip'...")
uploaded = files.upload()

zip_name = list(uploaded.keys())[0]
extract_dir = Path('/content/collecte_verify')
extract_dir.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_name, 'r') as zf:
    zf.extractall(extract_dir)

# Trouver le CSV
csv_files = list(extract_dir.rglob('*.csv'))
print(f'Extrait dans {extract_dir}')
print(f'CSV trouve: {[str(c) for c in csv_files]}')

# Compter les audios
webm_files = list(extract_dir.rglob('*.webm'))
print(f'Fichiers audio: {len(webm_files)}')
""")

# ---------------------------------------------------------------------------
code("""# Cell 11 : Verification par alignement force MMS (1 clip = 1 transcription)
import csv, json
import torchaudio, soundfile as sf
import numpy as np
from pathlib import Path
from collections import defaultdict

VERIFY_DIR = Path('/content/collecte_verify')
OUT_VERIFY = Path('/content/collecte_verified')
OUT_VERIFY.mkdir(exist_ok=True)
(OUT_VERIFY / 'wavs').mkdir(exist_ok=True)

# Trouver le CSV
csv_path = list(VERIFY_DIR.rglob('*.csv'))[0]
print(f'CSV: {csv_path}')

with open(csv_path, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))
print(f'Total entrees: {len(rows)}')

results = []
stats = defaultdict(int)

for i, row in enumerate(rows):
    audio_rel = row.get('audio_path', '').strip()
    text = row.get('transcription', '').strip()

    if not audio_rel or not text:
        stats['skip_empty'] += 1
        continue

    # Resoudre le chemin audio
    audio_path = None
    for candidate in [
        VERIFY_DIR / audio_rel,
        VERIFY_DIR / Path(audio_rel).name,
        VERIFY_DIR / 'audios' / Path(audio_rel).name,
    ]:
        if candidate.exists():
            audio_path = candidate
            break

    # Chercher par glob si pas trouve
    if not audio_path:
        found = list(VERIFY_DIR.rglob(Path(audio_rel).name))
        if found:
            audio_path = found[0]

    if not audio_path:
        stats['skip_no_audio'] += 1
        continue

    # Charger et resampler (webm/opus -> wav via ffmpeg)
    try:
        import subprocess, tempfile
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        subprocess.run(
            ['ffmpeg', '-y', '-i', str(audio_path), '-ar', str(SR), '-ac', '1', '-f', 'wav', tmp_path],
            capture_output=True, check=True
        )
        wav, _ = torchaudio.load(tmp_path)
        wav = wav.squeeze(0)
        import os; os.unlink(tmp_path)
    except Exception as e:
        stats['skip_load_error'] += 1
        continue

    dur = wav.shape[0] / SR
    if dur < 0.5 or dur > 30.0:
        stats['skip_duration'] += 1
        continue

    # Normaliser le texte
    fa_text = normalize_for_fa(text)
    words = fa_text.split()
    if len(words) < 1:
        stats['skip_no_words'] += 1
        continue

    # Alignement
    try:
        with torch.inference_mode():
            emission, _ = fa_model(wav.unsqueeze(0).to(DEVICE))
        tokenized = fa_tokenizer(words)
        word_spans = fa_aligner(emission[0], tokenized)
    except Exception as e:
        stats['skip_align_error'] += 1
        continue

    # Calculer le score moyen
    all_scores = []
    for ws in word_spans:
        for s in ws:
            all_scores.append(float(s.score))
    avg_score = float(np.mean(all_scores)) if all_scores else 0

    quality = 'verified' if avg_score >= 0.1 else 'rejected'
    stats[quality] += 1

    # Sauver le WAV 16kHz
    wav_name = Path(audio_rel).stem + '.wav'
    wav_out = OUT_VERIFY / 'wavs' / wav_name
    sf.write(str(wav_out), wav.numpy(), SR)

    results.append({
        'audio': str(wav_out),
        'text': text,
        'duration': round(dur, 3),
        'confidence': round(avg_score, 3),
        'quality': quality,
        'original_file': audio_rel,
    })

    if (i + 1) % 100 == 0:
        v = stats.get('verified', 0)
        r = stats.get('rejected', 0)
        print(f'  [{i+1}/{len(rows)}] verified={v} rejected={r}')

print()
print('=' * 50)
for k, v in sorted(stats.items()):
    print(f'  {k:25s}: {v}')

verified = [r for r in results if r['quality'] == 'verified']
rejected = [r for r in results if r['quality'] == 'rejected']
v_dur = sum(r['duration'] for r in verified) / 3600
r_dur = sum(r['duration'] for r in rejected) / 3600
print(f'\\nVerified : {len(verified)} clips ({v_dur:.2f}h)')
print(f'Rejected : {len(rejected)} clips ({r_dur:.2f}h)')
""")

# ---------------------------------------------------------------------------
code("""# Cell 12 : Export collecte verifiee + sauvegarde Drive
import json, shutil, zipfile
from pathlib import Path

OUT_VERIFY = Path('/content/collecte_verified')

# Export JSONL
verified = [r for r in results if r['quality'] == 'verified']
jsonl_path = OUT_VERIFY / 'collecte_verified.jsonl'
with open(jsonl_path, 'w', encoding='utf-8') as f:
    for r in verified:
        f.write(json.dumps(r, ensure_ascii=False) + '\\n')
print(f'Export: {len(verified)} clips -> {jsonl_path.name}')

# Copier vers Drive
drive_out = Path('/content/drive/MyDrive/aligned_segments_output')
drive_out.mkdir(parents=True, exist_ok=True)
shutil.copy2(jsonl_path, drive_out / jsonl_path.name)

# ZIP des WAVs verifies
verified_wavs = [Path(r['audio']) for r in verified if Path(r['audio']).exists()]
zip_path = drive_out / 'collecte_verified_wavs.zip'
print(f'Compression de {len(verified_wavs)} WAVs verifies...')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for wav in verified_wavs:
        zf.write(wav, wav.name)
print(f'ZIP : {zip_path}')
print('Sauvegarde terminee!')

v_dur = sum(r['duration'] for r in verified) / 3600
print(f'\\nTotal collecte verifiee: {len(verified)} clips ({v_dur:.2f}h)')
""")

# ---------------------------------------------------------------------------
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py", "mimetype": "text/x-python",
            "name": "python", "nbformat_exporter": "python",
            "pygments_lexer": "ipython3", "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

os.makedirs(os.path.dirname(os.path.abspath(NOTEBOOK_PATH)), exist_ok=True)
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print(f"Notebook genere : {NOTEBOOK_PATH}")
