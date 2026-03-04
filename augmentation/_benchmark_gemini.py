"""
Phase 1: Deep Linguistic Analysis of Human-Corrected Transcriptions.

Analyzes 103 real human-corrected transcriptions to:
1. Extract linguistic patterns (what correct Kabyle looks like)
2. Identify what Gemini would likely get wrong
3. Build a data-driven corrector from these patterns
"""
import csv
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "dataset" / "annotations_local.csv"

# ── Load data ──
rows = list(csv.DictReader(open(CSV_PATH, "r", encoding="utf-8-sig")))
print(f"Loaded {len(rows)} annotated transcriptions\n")

# ── ANALYSIS 1: Romanization System ──
print("=" * 60)
print("ANALYSIS 1: Romanization Patterns")
print("=" * 60)

arabizi_chars = Counter()
academic_chars = Counter()
for r in rows:
    t = r.get("Transcription", "")
    # Arabizi: 3, 7, 9 used as consonants
    arabizi_chars["3_ayn"] += len(re.findall(r'(?<!\d)3(?!\d)', t))  # 3 not in numbers
    arabizi_chars["7_ha"] += len(re.findall(r'(?<!\d)7(?!\d)', t))
    arabizi_chars["9_qaf"] += len(re.findall(r'(?<!\d)9(?!\d)', t))
    arabizi_chars["gh_ghayn"] += len(re.findall(r'gh', t, re.IGNORECASE))
    arabizi_chars["th_tha"] += len(re.findall(r'th', t, re.IGNORECASE))
    arabizi_chars["ch_shin"] += len(re.findall(r'ch', t, re.IGNORECASE))
    # Academic
    for c in "ɛħɣʃẓḍṭṣɤ":
        n = t.count(c) + t.count(c.upper())
        if n:
            academic_chars[c] += n

print("Arabizi usage (expected in correct transcriptions):")
for k, v in arabizi_chars.most_common():
    print(f"  {k}: {v}")
print(f"\nAcademic chars (should be ZERO in correct transcriptions):")
for k, v in academic_chars.most_common():
    print(f"  '{k}': {v}")
total_academic = sum(academic_chars.values())
print(f"  TOTAL academic chars: {total_academic}")

# ── ANALYSIS 2: Negation Patterns ──
print(f"\n{'='*60}")
print("ANALYSIS 2: Negation Patterns")
print("=" * 60)

neg_stats = Counter()
neg_examples = defaultdict(list)
for r in rows:
    t = r.get("Transcription", "")
    t_lower = t.lower()

    # ur...ara
    ur_matches = list(re.finditer(r'\bur\b', t_lower))
    ara_matches = list(re.finditer(r'\bara\b', t_lower))
    for m in ur_matches:
        # Check if ara follows within 50 chars
        context = t_lower[m.start():m.start()+50]
        if "ara" in context:
            neg_stats["ur...ara (correct)"] += 1
            neg_examples["ur...ara"].append(context[:40])
        else:
            neg_stats["ur WITHOUT ara (orphan)"] += 1
            neg_examples["ur_orphan"].append(context[:40])

    # machi
    for m in re.finditer(r'\bmachi\b', t_lower):
        after = t[m.end():m.end()+25].strip()
        neg_stats["machi"] += 1
        neg_examples["machi_after"].append(after[:30])

    # ulach/wlach
    neg_stats["ulach/wlach"] += len(re.findall(r'\b[wu]lach\b', t_lower))

    # khati/xati
    neg_stats["khati/xati"] += len(re.findall(r'\b[kx]hati\b', t_lower))

    # la la (darija)
    neg_stats["la la"] += len(re.findall(r'\bla la\b', t_lower))

for k, v in neg_stats.most_common():
    print(f"  {k}: {v}")
    examples = neg_examples.get(k.split()[0], [])
    for ex in examples[:2]:
        print(f"    ex: \"{ex}\"")

# ── ANALYSIS 3: Dialogue Format ──
print(f"\n{'='*60}")
print("ANALYSIS 3: Dialogue Format")
print("=" * 60)

format_stats = Counter()
for r in rows:
    t = r.get("Transcription", "")
    has_labels = bool(re.search(r'(Operator|Caller|Opérateur|Appelant)\s*:', t))
    has_dashes = "—" in t or "–" in t or " - " in t
    has_newlines = "\n" in t

    if has_labels:
        format_stats["labels (Operator:/Caller:)"] += 1
    elif has_dashes:
        format_stats["dashes (—)"] += 1
    elif has_newlines:
        format_stats["newlines"] += 1
    else:
        format_stats["continuous flow"] += 1

for k, v in format_stats.most_common():
    pct = v / len(rows) * 100
    print(f"  {k}: {v} ({pct:.0f}%)")

# ── ANALYSIS 4: Greetings ──
print(f"\n{'='*60}")
print("ANALYSIS 4: Greeting Patterns")
print("=" * 60)

greeting_stats = Counter()
for r in rows:
    t = r.get("Transcription", "")
    first100 = t[:100].lower()
    if "allo" in first100:
        greeting_stats["Allo"] += 1
    if "salam" in first100:
        greeting_stats["Salam (alaykoum)"] += 1
    if "azul" in first100:
        greeting_stats["Azul"] += 1
    if "sba7" in first100 or "sbah" in first100:
        greeting_stats["Sba7 lkhir"] += 1
    if "msa" in first100:
        greeting_stats["Msa lkhir"] += 1

for k, v in greeting_stats.most_common():
    pct = v / len(rows) * 100
    print(f"  {k}: {v} ({pct:.0f}%)")

# ── ANALYSIS 5: Construct State Usage ──
print(f"\n{'='*60}")
print("ANALYSIS 5: Construct State Patterns")
print("=" * 60)

construct_examples = []
for r in rows:
    t = r.get("Transcription", "")
    # Look for "n + noun" patterns
    for m in re.finditer(r"\bn\s+([a-zA-Z']+)", t):
        noun = m.group(1).lower()
        if noun.startswith("u") and len(noun) > 2:
            construct_examples.append(f"n {noun}")
        elif noun.startswith("t") and not noun.startswith("th"):
            construct_examples.append(f"n {noun}")

construct_counts = Counter(construct_examples)
print("Top construct state patterns (n + annexed noun):")
for k, v in construct_counts.most_common(15):
    print(f"  {k}: {v}")

# ── ANALYSIS 6: Emergency Verbs ──
print(f"\n{'='*60}")
print("ANALYSIS 6: Emergency Verb Usage")
print("=" * 60)

verb_patterns = {
    "ghli (fall)": r'\b[it]?-?[ye]?ghli\b',
    "che3l (burn)": r'\b[t]?che3l\b|\bch3el\b|\bicha3l\b',
    "doukh (faint)": r'\b[it]?-?doukh\b',
    "yugh (hurt)": r'\b[it]?-?yugh\b|\bthyugh\b',
    "nuffes (breathe)": r'\b[t]?-?nuffes\b|\brespire\b',
    "teddu (go)": r'\b[nt]?-?teddu\b|\bteddud\b',
    "arwa7 (come)": r'\barwa7\b',
    "ttawi (take)": r'\b[nt]?-?awi\b|\btawi\b|\battawi\b',
    "hlek (be bad)": r'\b[i]?hlek\b',
    "che3el (light)": r'\bche3el\b|\btche3el\b',
}

for label, pattern in verb_patterns.items():
    count = sum(1 for r in rows if re.search(pattern, r.get("Transcription", ""), re.IGNORECASE))
    print(f"  {label}: {count} calls")

# ── ANALYSIS 7: French Ratio ──
print(f"\n{'='*60}")
print("ANALYSIS 7: French Word Ratio")
print("=" * 60)

french_common = set([
    "il", "elle", "est", "le", "la", "les", "un", "une", "de", "du",
    "des", "et", "ou", "mais", "donc", "que", "qui", "dans", "sur",
    "avec", "pour", "pas", "ne", "se", "son", "sa", "ses",
    "nous", "vous", "ils", "elles", "ce", "cette",
    "oui", "non", "bien", "très", "aussi", "comme", "plus",
    "an", "ans", "être", "avoir", "faire", "dire",
    "c'est", "qu'est-ce", "parce", "comment", "pourquoi", "quand",
])

ratios = []
for r in rows:
    t = r.get("Transcription", "")
    words = t.lower().split()
    if not words:
        continue
    fr_count = sum(1 for w in words if w in french_common)
    ratio = fr_count / len(words)
    ratios.append(ratio)

if ratios:
    avg = sum(ratios) / len(ratios)
    mn = min(ratios)
    mx = max(ratios)
    print(f"  Average French word ratio: {avg:.1%}")
    print(f"  Min: {mn:.1%}, Max: {mx:.1%}")
    # Distribution
    buckets = Counter()
    for r in ratios:
        if r < 0.05: buckets["< 5%"] += 1
        elif r < 0.10: buckets["5-10%"] += 1
        elif r < 0.15: buckets["10-15%"] += 1
        elif r < 0.20: buckets["15-20%"] += 1
        elif r < 0.30: buckets["20-30%"] += 1
        else: buckets[">30%"] += 1
    for k in ["< 5%", "5-10%", "10-15%", "15-20%", "20-30%", ">30%"]:
        v = buckets.get(k, 0)
        print(f"    {k}: {v} calls")

# ── ANALYSIS 8: Kabyle Markers Density ──
print(f"\n{'='*60}")
print("ANALYSIS 8: Kabyle Markers Density")
print("=" * 60)

MARKERS = [
    "an3am", "ih", "iyeh", "d'accord", "saha", "sahit",
    "dayi", "dagi", "dinna", "tura", "chwiya",
    "anda", "anida", "anwa", "amek", "dachu", "achu",
    "yella", "thella", "nes3a", "ulach", "wlach",
    "agma", "khouya", "a sidi", "ma3lich",
    "khati", "xati", "machi", "bessah",
]

marker_freq = Counter()
calls_per_marker = Counter()
for r in rows:
    t = r.get("Transcription", "").lower()
    for m in MARKERS:
        count = t.count(m)
        if count:
            marker_freq[m] += count
            calls_per_marker[m] += 1

print("Most frequent Kabyle markers across all transcriptions:")
for m, freq in marker_freq.most_common(20):
    calls = calls_per_marker[m]
    print(f"  {m}: {freq} occurrences in {calls} calls")

# ── ANALYSIS 9: Gemini vs Human comparison ──
print(f"\n{'='*60}")
print("ANALYSIS 9: Specific Gemini Error Patterns (from JSON comparison)")
print("=" * 60)

# We found academic notation in the JSON (Gemini raw) vs arabizi in CSV (human corrected)
# Key patterns Gemini gets wrong:
print("""
OBSERVED GEMINI ERRORS (from manual JSON inspection):
1. ROMANIZATION: Uses ɣ (gamma) instead of gh
   - Gemini: "ɣer yiwen" → Human: "gher yiwen"
   - Gemini: "ṭṭbib" → Human: "tbib" or "thbib"
   - Gemini: "ɛassen" → Human: "3assen"

2. OVER-STANDARDIZATION: Gemini uses literary Kabyle forms
   - Gemini: "A: ... O: ..." labels → Human: continuous flow
   - Gemini: "fell-ak" (careful) → Human: "fell-ak" (same, but context)

3. VOCABULARY INVENTION: Gemini translates French → invented Kabyle
   - Gemini: "n d-yefles" → Human: actual Kabyle word used by speaker

4. CONSTRUCT STATE: Gemini sometimes misses construct state
   - Pattern: "n argaz" should be "n urgaz"

5. NEGATION: Gemini may drop the discontinuous "ara"
   - Missing: "ur t-zmir" should be "ur t-zmir ara"
""")

print("\n" + "=" * 60)
print("SUMMARY: Key areas for corrector + prompt improvement")
print("=" * 60)
print("""
PROMPT PRIORITIES (prevent errors at source):
  P1. Explicit arabizi romanization table (3/7/9/gh/th/ch)
  P2. List of emergency verbs with correct conjugations
  P3. Negation rules: ur...ara circumfixe obligatoire
  P4. Code-switching rules: NEVER translate medical/tech FR terms
  P5. Dialogue format: match what human annotators use

CORRECTOR PRIORITIES (catch remaining errors):
  C1. Romanization: replace academic chars → arabizi
  C2. Negation: fix orphan "ur" by adding "ara"
  C3. Construct state: after prepositions n/g
  C4. French article normalization: "la ambulance" → "l'ambulance"
  C5. machi + verb detection (flag only)
""")
