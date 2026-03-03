#!/usr/bin/env python3
"""
bpe_corpus_analysis.py — BPE-based linguistic structure analyser for DGPC.

Trains a mini Byte Pair Encoding on real transcriptions from
annotations_local.csv, then optionally compares the BPE vocabulary
against synthetic data.  Outputs:
  1. Top merge operations (most frequent byte-pairs)
  2. Final BPE vocabulary with frequencies
  3. Morphological pattern clusters (arabizi markers, particles, verbs)
  4. [Optional] Real-vs-synthetic divergence report

Usage:
  python augmentation/research/bpe_corpus_analysis.py
  python augmentation/research/bpe_corpus_analysis.py --synth_jsonl path/to/synth.jsonl
  python augmentation/research/bpe_corpus_analysis.py --num_merges 500 --top_k 80
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------------------
# BPE Implementation
# ---------------------------------------------------------------------------

def get_word_freq(corpus: List[str]) -> Dict[Tuple[str, ...], int]:
    """Tokenize each word into character tuples and count frequencies."""
    word_freq: Dict[Tuple[str, ...], int] = collections.Counter()
    for text in corpus:
        # Normalise: lowercase, collapse whitespace
        text = re.sub(r"\s+", " ", text.lower().strip())
        for word in text.split():
            chars = tuple(word) + ("</w>",)  # end-of-word marker
            word_freq[chars] += 1
    return dict(word_freq)


def get_pair_stats(word_freq: Dict[Tuple[str, ...], int]) -> Dict[Tuple[str, str], int]:
    """Count all adjacent symbol pairs across the vocabulary."""
    pairs: Dict[Tuple[str, str], int] = collections.Counter()
    for word, freq in word_freq.items():
        for i in range(len(word) - 1):
            pairs[(word[i], word[i + 1])] += freq
    return dict(pairs)


def merge_pair(
    pair: Tuple[str, str],
    word_freq: Dict[Tuple[str, ...], int],
) -> Dict[Tuple[str, ...], int]:
    """Merge the most frequent pair across the vocabulary."""
    new_word_freq: Dict[Tuple[str, ...], int] = {}
    bigram = pair
    for word, freq in word_freq.items():
        new_word: List[str] = []
        i = 0
        while i < len(word):
            if i < len(word) - 1 and (word[i], word[i + 1]) == bigram:
                new_word.append(word[i] + word[i + 1])
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        new_word_freq[tuple(new_word)] = freq
    return new_word_freq


def train_bpe(
    corpus: List[str],
    num_merges: int = 300,
) -> Tuple[List[Tuple[str, str, int]], Dict[Tuple[str, ...], int]]:
    """Train BPE and return merge log + final vocabulary.

    Returns:
        merges: list of (left, right, frequency) for each merge operation
        word_freq: final segmented vocabulary after all merges
    """
    word_freq = get_word_freq(corpus)
    merges: List[Tuple[str, str, int]] = []

    for step in range(num_merges):
        pair_stats = get_pair_stats(word_freq)
        if not pair_stats:
            break
        best_pair = max(pair_stats, key=pair_stats.get)  # type: ignore[arg-type]
        best_freq = pair_stats[best_pair]
        if best_freq < 2:
            break  # no more useful merges
        merges.append((best_pair[0], best_pair[1], best_freq))
        word_freq = merge_pair(best_pair, word_freq)

    return merges, word_freq


# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------

ARABIZI_MARKERS = {"3", "7", "9", "gh", "ch", "th"}
KABYLE_PARTICLES = {
    "dayi", "dagi", "dinna", "tura", "chwiya", "an3am", "anda",
    "anida", "anwa", "dachu", "achu", "yiwen", "yiweth", "amek",
    "ih", "iyeh", "khati", "xati", "machi", "ulach", "wlach",
}
URGENCY_VERBS = {"ghli", "che3l", "doukh", "yugh", "nuffes", "teddu", "arwa7", "ttawi"}
FRENCH_MARKERS = {
    "ambulance", "accident", "urgence", "bloc", "etage", "docteur",
    "inconscient", "malaise", "tension", "saturation", "oxygene",
    "respire", "hopital", "pompiers", "camion", "blessé", "crise",
}


def classify_token(token: str) -> str:
    """Classify a BPE token into linguistic category."""
    clean = token.replace("</w>", "").lower()
    if clean in ARABIZI_MARKERS:
        return "arabizi_marker"
    if clean in KABYLE_PARTICLES:
        return "kabyle_particle"
    if clean in URGENCY_VERBS:
        return "urgency_verb"
    if clean in FRENCH_MARKERS:
        return "french_technical"
    # Check for arabizi digit patterns
    if any(c in clean for c in "379"):
        return "arabizi_word"
    if clean.startswith("l'") or clean.startswith("l-"):
        return "french_integrated"
    return "other"


def extract_final_vocab(
    word_freq: Dict[Tuple[str, ...], int],
    top_k: int = 100,
) -> List[Dict[str, Any]]:
    """Extract the most frequent tokens from the final BPE vocabulary."""
    token_freq: Dict[str, int] = collections.Counter()
    for word_tuple, freq in word_freq.items():
        for token in word_tuple:
            token_freq[token] += freq

    results = []
    for token, freq in token_freq.most_common(top_k):
        results.append({
            "token": token,
            "frequency": freq,
            "category": classify_token(token),
            "length": len(token.replace("</w>", "")),
        })
    return results


def compute_category_stats(vocab: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """Aggregate stats by linguistic category."""
    stats: Dict[str, Dict[str, int]] = {}
    for entry in vocab:
        cat = entry["category"]
        if cat not in stats:
            stats[cat] = {"count": 0, "total_freq": 0}
        stats[cat]["count"] += 1
        stats[cat]["total_freq"] += entry["frequency"]
    return stats


# ---------------------------------------------------------------------------
# Corpus loading
# ---------------------------------------------------------------------------

def load_real_corpus(csv_path: Path) -> List[str]:
    """Load transcriptions from annotations_local.csv."""
    if not csv_path.exists():
        print(f"Warning: {csv_path} not found.")
        return []
    texts = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            text = (row.get("Transcription") or "").strip()
            if text and len(text) > 20:
                texts.append(text)
    return texts


def load_synth_corpus(jsonl_path: Path) -> List[str]:
    """Load transcriptions from a synthetic JSONL file."""
    if not jsonl_path.exists():
        print(f"Warning: {jsonl_path} not found.")
        return []
    texts = []
    for line in jsonl_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        text = (row.get("transcription") or "").strip()
        if text and len(text) > 20:
            texts.append(text)
    return texts


# ---------------------------------------------------------------------------
# Divergence analysis
# ---------------------------------------------------------------------------

def compute_divergence(
    real_vocab: List[Dict[str, Any]],
    synth_vocab: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Compare real vs synthetic BPE vocabularies."""
    real_tokens = {e["token"]: e["frequency"] for e in real_vocab}
    synth_tokens = {e["token"]: e["frequency"] for e in synth_vocab}

    real_total = sum(real_tokens.values()) or 1
    synth_total = sum(synth_tokens.values()) or 1

    all_tokens = set(real_tokens) | set(synth_tokens)

    divergences = []
    for token in all_tokens:
        r_ratio = real_tokens.get(token, 0) / real_total
        s_ratio = synth_tokens.get(token, 0) / synth_total
        diff = abs(r_ratio - s_ratio)
        divergences.append({
            "token": token,
            "real_freq": real_tokens.get(token, 0),
            "synth_freq": synth_tokens.get(token, 0),
            "real_ratio": round(r_ratio, 6),
            "synth_ratio": round(s_ratio, 6),
            "divergence": round(diff, 6),
            "category": classify_token(token),
        })

    divergences.sort(key=lambda x: x["divergence"], reverse=True)

    # Summary stats
    only_real = [t for t in all_tokens if t not in synth_tokens]
    only_synth = [t for t in all_tokens if t not in real_tokens]
    overlap = all_tokens - set(only_real) - set(only_synth)

    return {
        "total_real_tokens": len(real_tokens),
        "total_synth_tokens": len(synth_tokens),
        "overlap_count": len(overlap),
        "only_in_real": len(only_real),
        "only_in_synth": len(only_synth),
        "overlap_ratio": round(len(overlap) / max(len(all_tokens), 1), 4),
        "top_divergences": divergences[:30],
        "only_real_examples": sorted(only_real)[:20],
        "only_synth_examples": sorted(only_synth)[:20],
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_report(
    merges: List[Tuple[str, str, int]],
    vocab: List[Dict[str, Any]],
    cat_stats: Dict[str, Dict[str, int]],
    corpus_size: int,
    label: str = "REAL",
    divergence: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate a human-readable BPE report."""
    lines = []
    lines.append(f"{'='*70}")
    lines.append(f" BPE CORPUS ANALYSIS — {label}")
    lines.append(f"{'='*70}")
    lines.append(f" Corpus: {corpus_size} transcriptions")
    lines.append(f" Merges performed: {len(merges)}")
    lines.append(f" Final vocab size: {len(vocab)} tokens shown")
    lines.append("")

    # Top merges
    lines.append(f"{'─'*70}")
    lines.append(" TOP 40 BPE MERGES (most frequent byte-pairs)")
    lines.append(f"{'─'*70}")
    lines.append(f" {'#':>3}  {'Left':>10} + {'Right':<10}  {'Freq':>6}  {'Merged':>15}  {'Category'}")
    for i, (left, right, freq) in enumerate(merges[:40], 1):
        merged = left + right
        cat = classify_token(merged)
        lines.append(f" {i:3d}  {left:>10} + {right:<10}  {freq:6d}  {merged:>15}  {cat}")

    # Category summary
    lines.append(f"\n{'─'*70}")
    lines.append(" LINGUISTIC CATEGORY BREAKDOWN")
    lines.append(f"{'─'*70}")
    total_freq = sum(s["total_freq"] for s in cat_stats.values()) or 1
    for cat, stats in sorted(cat_stats.items(), key=lambda x: x[1]["total_freq"], reverse=True):
        pct = stats["total_freq"] / total_freq * 100
        lines.append(f" {cat:25s}  tokens={stats['count']:4d}  freq={stats['total_freq']:6d}  ({pct:5.1f}%)")

    # Top tokens by category
    for category in ["kabyle_particle", "arabizi_word", "french_technical", "french_integrated", "urgency_verb"]:
        cat_tokens = [e for e in vocab if e["category"] == category]
        if cat_tokens:
            lines.append(f"\n {'─'*40}")
            lines.append(f"  {category.upper()} tokens:")
            for e in cat_tokens[:15]:
                lines.append(f"    {e['token']:20s}  freq={e['frequency']:5d}")

    # Divergence report
    if divergence:
        lines.append(f"\n{'='*70}")
        lines.append(" REAL vs SYNTHETIC DIVERGENCE")
        lines.append(f"{'='*70}")
        lines.append(f" Overlap: {divergence['overlap_count']} tokens ({divergence['overlap_ratio']*100:.1f}%)")
        lines.append(f" Only in real: {divergence['only_in_real']} tokens")
        lines.append(f" Only in synth: {divergence['only_in_synth']} tokens")
        lines.append(f"\n Top divergent tokens:")
        lines.append(f" {'Token':>20s}  {'Real%':>8s}  {'Synth%':>8s}  {'Diff':>8s}  {'Cat'}")
        for d in divergence["top_divergences"][:20]:
            lines.append(
                f" {d['token']:>20s}  {d['real_ratio']*100:7.3f}%  {d['synth_ratio']*100:7.3f}%  "
                f"{d['divergence']*100:7.3f}%  {d['category']}"
            )
        if divergence["only_real_examples"]:
            lines.append(f"\n Only in REAL: {', '.join(divergence['only_real_examples'][:15])}")
        if divergence["only_synth_examples"]:
            lines.append(f" Only in SYNTH: {', '.join(divergence['only_synth_examples'][:15])}")

    lines.append(f"\n{'='*70}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="BPE corpus analysis for DGPC")
    parser.add_argument(
        "--corpus_csv",
        default=str(ROOT / "dataset" / "annotations_real_calls.csv"),
        help="Path to real annotations CSV.",
    )
    parser.add_argument(
        "--synth_jsonl",
        default="",
        help="Optional: path to synthetic JSONL for comparison.",
    )
    parser.add_argument("--num_merges", type=int, default=300, help="Number of BPE merges.")
    parser.add_argument("--top_k", type=int, default=100, help="Top-K tokens to display.")
    parser.add_argument(
        "--output",
        default=str(ROOT / "augmentation" / "research" / "bpe_analysis_report.txt"),
        help="Output report path.",
    )
    parser.add_argument(
        "--output_json",
        default=str(ROOT / "augmentation" / "research" / "bpe_analysis_data.json"),
        help="Output structured data path.",
    )
    args = parser.parse_args()

    # Load real corpus
    real_texts = load_real_corpus(Path(args.corpus_csv))
    if not real_texts:
        print("ERROR: No real transcriptions found. Check --corpus_csv path.")
        sys.exit(1)
    print(f"Loaded {len(real_texts)} real transcriptions.")

    # Train BPE on real corpus
    print(f"Training BPE ({args.num_merges} merges)...")
    real_merges, real_word_freq = train_bpe(real_texts, num_merges=args.num_merges)
    real_vocab = extract_final_vocab(real_word_freq, top_k=args.top_k)
    real_cat_stats = compute_category_stats(real_vocab)
    print(f"  {len(real_merges)} merges completed, {len(real_vocab)} tokens extracted.")

    # Optional synthetic comparison
    divergence = None
    if args.synth_jsonl:
        synth_texts = load_synth_corpus(Path(args.synth_jsonl))
        if synth_texts:
            print(f"Loaded {len(synth_texts)} synthetic transcriptions.")
            print(f"Training BPE on synthetic corpus...")
            _, synth_word_freq = train_bpe(synth_texts, num_merges=args.num_merges)
            synth_vocab = extract_final_vocab(synth_word_freq, top_k=args.top_k)
            divergence = compute_divergence(real_vocab, synth_vocab)
            print(f"  Overlap: {divergence['overlap_ratio']*100:.1f}%")

    # Generate report
    report = print_report(
        merges=real_merges,
        vocab=real_vocab,
        cat_stats=real_cat_stats,
        corpus_size=len(real_texts),
        label="REAL CORPUS" + (" vs SYNTHETIC" if divergence else ""),
        divergence=divergence,
    )

    # Save report
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved: {out_path}")

    # Save structured data
    json_out = Path(args.output_json)
    json_data = {
        "corpus_size": len(real_texts),
        "num_merges": len(real_merges),
        "top_merges": [
            {"left": l, "right": r, "frequency": f, "merged": l + r}
            for l, r, f in real_merges[:60]
        ],
        "vocabulary": real_vocab,
        "category_stats": real_cat_stats,
    }
    if divergence:
        json_data["divergence"] = divergence
    json_out.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Data saved: {json_out}")

    # Print to stdout
    print(report)


if __name__ == "__main__":
    main()
