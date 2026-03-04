#!/usr/bin/env python3
"""
build_lexicon.py — Kabyle Memory Core Lexicon Builder
=====================================================
Builds a closed Kabyle vocabulary (kabyle_lexicon.yaml) using the 
Pleias SYNTH "Memory Core" approach:

  Layer 1 (VERIFICATION):  External repos → verified Kabyle lemmes
  Layer 2 (TRANSLITERATION): 400 real Béjaïa calls → Arabizi mapping

Sources:
  - words.csv (5,417 EN↔KAB pairs)
  - flexions_verbales.txt (9,899 conjugated verb forms)
  - corpuspos.txt (19,974 POS-tagged lines)
  - annotations_real_calls.csv (real Béjaïa call transcriptions)
  - corpus-brut/part*.txt (massive Kabyle text corpus, CC0)

Output: augmentation/kabyle_lexicon.yaml
"""

import argparse
import csv
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTERNAL = PROJECT_ROOT / "external_repo_audit"

# Source paths
WORDS_CSV       = EXTERNAL / "FarZ1_Kabyle-Arab-Game" / "resources" / "words.csv"
FLEXIONS_TXT    = EXTERNAL / "MohammedBelkacem_KabyleCorporaGenerator" / "flexions_verbales.txt"
CORPUSPOS_TXT   = EXTERNAL / "MohammedBelkacem_KabyleNLP" / "copus" / "corpuspos.txt"
BRUT_TEXT       = EXTERNAL / "MohammedBelkacem_KabyleNLP" / "POSTAG" / "brut_text.txt"
CORPUS_KAB_DIR  = EXTERNAL / "MohammedBelkacem_corpus-kab" / "corpus-brut"
REAL_CALLS_CSV  = PROJECT_ROOT / "dataset" / "400annotations_local.csv"

OUTPUT_PATH     = Path(__file__).resolve().parent / "kabyle_lexicon.yaml"

# Standard Kabyle → Arabizi transliteration map (Béjaïa conventions)
TRANSLIT_MAP = {
    'ɣ': 'gh', 'Ɣ': 'Gh',
    'ɛ': '3',  'Ɛ': '3',
    'ḥ': '7',  'Ḥ': '7',
    'č': 'ch', 'Č': 'Ch',
    'ṭ': 'tt', 'Ṭ': 'Tt',
    'ṣ': 'ss', 'Ṣ': 'Ss',
    'ḍ': 'dd', 'Ḍ': 'Dd',
    'ṛ': 'r',  'Ṛ': 'R',
    'ẓ': 'zz', 'Ẓ': 'Zz',
    'ǧ': 'dj', 'Ǧ': 'Dj',
}

# POS tags → category mapping (from KabyleNLP tagset)
POS_CATEGORIES = {
    'VAI': 'verb', 'VP': 'verb', 'VAF': 'verb', 'PREAL': 'verb',
    'NMC': 'noun', 'NMP': 'noun', 'NFS': 'noun', 'NFP': 'noun',
    'ADV': 'particle', 'ADJ': 'adjective',
    'PRP': 'preposition', 'CC': 'conjunction', 'CS': 'conjunction',
    'INT': 'interrogative', 'PRD': 'demonstrative',
    'PRI': 'pronoun', 'PDS': 'pronoun', 'PLP': 'particle',
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def to_arabizi(word: str) -> str:
    """Convert standard Kabyle orthography to Béjaïa Arabizi."""
    result = word
    for std, arab in TRANSLIT_MAP.items():
        result = result.replace(std, arab)
    return result


def is_kabyle_like(word: str) -> bool:
    """Heuristic: is this word likely Kabyle (not French/Arabic)?"""
    w = word.lower()
    # Contains Kabyle-specific characters
    kabyle_chars = set('ɣɛḥčṭṣḍṛẓǧ')
    if any(c in kabyle_chars for c in w):
        return True
    # Contains Arabizi markers
    if re.search(r'[37]', w):
        return True
    # Kabyle phonological patterns
    if re.search(r'(gh|dh|th|ch|kh)', w) and len(w) > 2:
        return True
    return False


def normalize_word(word: str) -> str:
    """Lowercase, strip punctuation, normalize whitespace."""
    w = word.strip().lower()
    w = re.sub(r'[.,;:!?"""\'()\[\]{}…«»\-–—/\\]', '', w)
    return w.strip()


def read_file_safe(path: Path, encoding='utf-8') -> str:
    """Read file with fallback encodings."""
    for enc in [encoding, 'utf-8-sig', 'latin-1']:
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    return ""


# ---------------------------------------------------------------------------
# Source Extractors
# ---------------------------------------------------------------------------
def extract_words_csv() -> dict:
    """Extract bilingual pairs from words.csv (EN↔KAB)."""
    pairs = {}
    if not WORDS_CSV.exists():
        print(f"  [SKIP] {WORDS_CSV} not found")
        return pairs
    with open(WORDS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2:
                en, kab = row[0].strip(), row[1].strip()
                if kab and en:
                    kab_norm = normalize_word(kab)
                    if kab_norm:
                        pairs[kab_norm] = en
    print(f"  [OK] words.csv: {len(pairs)} bilingual pairs")
    return pairs


def extract_flexions() -> set:
    """Extract all conjugated verb forms from flexions_verbales.txt."""
    forms = set()
    if not FLEXIONS_TXT.exists():
        print(f"  [SKIP] {FLEXIONS_TXT} not found")
        return forms
    text = read_file_safe(FLEXIONS_TXT)
    for line in text.splitlines():
        line = line.strip().rstrip('.')
        if not line:
            continue
        # Lines are individual verb forms like "Ad afeɣ" or "Ur ufiɣ ara"
        words = line.split()
        for w in words:
            w_clean = normalize_word(w)
            if w_clean and w_clean not in ('ad', 'ur', 'ara', 'yettafen'):
                forms.add(w_clean)
    print(f"  [OK] flexions_verbales.txt: {len(forms)} verb forms")
    return forms


def extract_pos_tagged() -> dict:
    """Extract words by POS category from corpuspos.txt."""
    categories = defaultdict(set)
    if not CORPUSPOS_TXT.exists():
        print(f"  [SKIP] {CORPUSPOS_TXT} not found")
        return categories
    text = read_file_safe(CORPUSPOS_TXT)
    for line in text.splitlines():
        # Format: "word/POS" or "word/POS word2/POS2"
        tokens = line.strip().split()
        for token in tokens:
            if '/' in token:
                parts = token.rsplit('/', 1)
                if len(parts) == 2:
                    word, pos = parts
                    word = normalize_word(word)
                    if word and pos in POS_CATEGORIES:
                        cat = POS_CATEGORIES[pos]
                        categories[cat].add(word)
    total = sum(len(v) for v in categories.values())
    print(f"  [OK] corpuspos.txt: {total} words across {len(categories)} categories")
    for cat, words in sorted(categories.items(), key=lambda x: -len(x[1])):
        print(f"       {cat}: {len(words)} unique")
    return categories


def extract_brut_corpus() -> Counter:
    """Extract word frequencies from brut_text.txt and corpus-brut/."""
    word_freq = Counter()
    
    # brut_text.txt
    if BRUT_TEXT.exists():
        text = read_file_safe(BRUT_TEXT)
        for word in text.split():
            w = normalize_word(word)
            if w and len(w) > 1:
                word_freq[w] += 1
        print(f"  [OK] brut_text.txt: {len(word_freq)} unique tokens")
    
    # corpus-brut/ directory
    if CORPUS_KAB_DIR.exists():
        count = 0
        for txt_file in sorted(CORPUS_KAB_DIR.rglob('*.txt')):
            text = read_file_safe(txt_file)
            for word in text.split():
                w = normalize_word(word)
                if w and len(w) > 1:
                    word_freq[w] += 1
            count += 1
        print(f"  [OK] corpus-brut/: {count} files, {len(word_freq)} total unique tokens")
    
    return word_freq


def extract_real_calls() -> tuple:
    """Extract vocabulary and geography from real Béjaïa calls."""
    arabizi_words = Counter()
    geography = set()
    
    if not REAL_CALLS_CSV.exists():
        print(f"  [SKIP] {REAL_CALLS_CSV} not found")
        return arabizi_words, geography
    
    with open(REAL_CALLS_CSV, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract transcription words
            trans = row.get('Transcription', '')
            if trans:
                for word in trans.split():
                    w = normalize_word(word)
                    if w and len(w) > 1:
                        arabizi_words[w] += 1
            
            # Extract geography (daira, commune, lieu)
            for geo_field in ['daira', 'commune', 'lieu']:
                val = row.get(geo_field, '').strip()
                if val and val.lower() not in ('', 'nan', 'none', 'n/a'):
                    # Clean: remove parentheticals, strip descriptions
                    clean = re.sub(r'\(.*?\)', '', val).strip()
                    clean = re.sub(r'\d{3,}', '', clean).strip()  # remove long numbers
                    clean = re.sub(r'[/,;]', ' ', clean)  # split on separators
                    for part in clean.split():
                        p = part.strip().lower()
                        # Keep only meaningful place names (2+ chars, not pure numbers)
                        if p and len(p) >= 2 and not p.isdigit():
                            geography.add(p)
    
    print(f"  [OK] real_calls: {len(arabizi_words)} unique tokens, {len(geography)} geographic entities")
    return arabizi_words, geography


# ---------------------------------------------------------------------------
# Lexicon Builder
# ---------------------------------------------------------------------------
def build_lexicon():
    """Build the complete kabyle_lexicon.yaml."""
    print("=" * 60)
    print("KABYLE MEMORY CORE LEXICON BUILDER")
    print("=" * 60)
    
    # --- LAYER 1: External Verified Sources ---
    print("\n--- Layer 1: Verified Vocabulary (External Repos) ---")
    
    bilingual_pairs = extract_words_csv()
    verb_forms = extract_flexions()
    pos_categories = extract_pos_tagged()
    corpus_freq = extract_brut_corpus()
    
    # --- LAYER 2: Real Calls Arabizi ---
    print("\n--- Layer 2: Arabizi Vocabulary (Real Béjaïa Calls) ---")
    
    real_words, geography = extract_real_calls()
    
    # --- MERGE & TRANSLITERATE ---
    print("\n--- Merging & Building Lexicon ---")
    
    # 1) Collect all verified Kabyle words (standard orthography)
    verified_standard = set()
    verified_standard.update(bilingual_pairs.keys())
    verified_standard.update(verb_forms)
    for cat_words in pos_categories.values():
        verified_standard.update(cat_words)
    # Add high-frequency corpus words (freq >= 3 = likely real)
    for word, freq in corpus_freq.items():
        if freq >= 3 and len(word) > 1:
            verified_standard.add(word)
    
    print(f"  Total verified (standard orthography): {len(verified_standard)}")
    
    # 2) Generate Arabizi equivalents
    arabizi_set = set()
    standard_to_arabizi = {}
    for word in verified_standard:
        arab = to_arabizi(word)
        arabizi_set.add(arab)
        if arab != word:  # Only store if transliteration changed something
            standard_to_arabizi[word] = arab
    
    # 3) Add real call words directly (already in Arabizi)
    real_arabizi = set()
    for word in real_words:
        if len(word) > 1:
            real_arabizi.add(word)
    
    # Combined whitelist = verified Arabizi + real call words
    full_whitelist = arabizi_set | real_arabizi
    print(f"  Arabizi equivalents generated: {len(arabizi_set)}")
    print(f"  Real call words added: {len(real_arabizi)}")
    print(f"  Total whitelist size: {len(full_whitelist)}")
    
    # --- BUILD YAML STRUCTURE ---
    # Organize by category for the prompt injection
    # STRATEGY: sort by real-call frequency (most used emergency words first),
    # NOT alphabetically. This ensures the prompt contains the most relevant
    # words for our domain (Béjaïa emergency calls).
    def _sort_by_relevance(word_set, freq_counter):
        """Sort words: highest real-call frequency first, then alphabetical."""
        return sorted(word_set, key=lambda w: (-freq_counter.get(w, 0), w))

    # Build a combined frequency index (standard + arabizi forms)
    combined_freq = Counter()
    for w, f in real_words.items():
        combined_freq[w] = f
    for w, f in corpus_freq.items():
        arab = to_arabizi(w)
        combined_freq[arab] = max(combined_freq.get(arab, 0), f)

    lexicon = {
        'version': '1.0',
        'build_info': {
            'sources': {
                'words_csv': len(bilingual_pairs),
                'flexions_verbales': len(verb_forms),
                'corpuspos': sum(len(v) for v in pos_categories.values()),
                'corpus_brut_freq3': sum(1 for f in corpus_freq.values() if f >= 3),
                'real_calls_transcriptions': len(real_words),
            },
            'total_verified_standard': len(verified_standard),
            'total_arabizi': len(arabizi_set),
            'total_real_call_words': len(real_arabizi),
            'total_whitelist': len(full_whitelist),
        },
        'transliteration_map': {k: v for k, v in sorted(TRANSLIT_MAP.items()) if ord(k) > 127},
        'geography_bejaia': sorted(geography),
    }
    
    # Verb forms — sorted by real-call frequency (emergency verbs first)
    verb_arabizi = set(to_arabizi(v) for v in verb_forms)
    lexicon['verbs'] = _sort_by_relevance(verb_arabizi, combined_freq)[:500]
    lexicon['verbs_count'] = len(verb_arabizi)
    
    # POS categories — each sorted by relevance
    for cat, words in sorted(pos_categories.items()):
        cat_arabizi = set(to_arabizi(w) for w in words)
        lexicon[f'pos_{cat}'] = _sort_by_relevance(cat_arabizi, combined_freq)
    
    # Bilingual dictionary — top 200 by real-call frequency
    bilingual_with_freq = []
    for kab, en in bilingual_pairs.items():
        arab = to_arabizi(kab)
        freq = combined_freq.get(arab, 0)
        bilingual_with_freq.append((arab, en, freq))
    bilingual_with_freq.sort(key=lambda x: (-x[2], x[0]))
    bilingual_arabizi = {k: v for k, v, _ in bilingual_with_freq[:200]}
    lexicon['bilingual_kab_en'] = bilingual_arabizi
    
    # High-frequency words from real calls (top 100)
    top_real = [w for w, _ in real_words.most_common(100)]
    lexicon['high_freq_real_calls'] = top_real
    
    # Full flat whitelist for guard rule R7
    lexicon['whitelist_flat'] = sorted(full_whitelist)
    lexicon['whitelist_count'] = len(full_whitelist)
    
    # --- WRITE OUTPUT ---
    print(f"\n--- Writing {OUTPUT_PATH} ---")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(lexicon, f, allow_unicode=True, default_flow_style=False, 
                  width=120, sort_keys=False)
    
    file_size = OUTPUT_PATH.stat().st_size
    print(f"  Written: {file_size:,} bytes")
    
    # --- QUALITY REPORT ---
    print("\n" + "=" * 60)
    print("QUALITY REPORT")
    print("=" * 60)
    
    # Check coverage: how many real call words are in the verified set?
    real_in_verified = sum(1 for w in real_arabizi if w in arabizi_set)
    coverage = real_in_verified / max(len(real_arabizi), 1) * 100
    print(f"  Real call coverage by verified lexicon: {real_in_verified}/{len(real_arabizi)} ({coverage:.1f}%)")
    
    # Words in real calls NOT in verified set (potential gaps)
    gaps = [w for w in real_words.most_common(50) if w[0] not in arabizi_set]
    if gaps:
        print(f"  Top uncovered real-call words (may be French or new Kabyle):")
        for w, freq in gaps[:15]:
            print(f"    '{w}' (freq={freq})")
    
    print(f"\n✅ Lexicon built successfully: {len(full_whitelist)} words")
    return lexicon


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build Kabyle Memory Core Lexicon')
    parser.add_argument('--output', type=str, default=str(OUTPUT_PATH),
                        help='Output YAML path')
    args = parser.parse_args()
    
    if args.output != str(OUTPUT_PATH):
        OUTPUT_PATH = Path(args.output)
    
    build_lexicon()
