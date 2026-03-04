"""Arabizi → TTS normalizer for Béjaïa Kabyle/Darija/French emergency calls.

Converts arabizi digits (3, 7, 9) to IPA-like characters that TTS models can
pronounce, while preserving phone numbers and French text.

Design principles (from 356-call corpus analysis):
- 3 → ɛ  (ʕayn) — most frequent: an3am, ma3lich, ness3a, 3la, ta3
- 7 → ħ  (ḥa)   — most frequent: l7imaya, sa7it, sa7a, wa7ed 
- 9 → q  (qaf)  — rare in real data: yterte9, u9eruy, ta9aryeth
- Phone numbers (034...., 3-4 digit clusters) → preserved as-is
- French words → untouched (TTS handles them natively)
"""

import re
from typing import List, Tuple


# ── Arabizi digit-to-phoneme mapping ──────────────────────────────────
# These characters are chosen because:
# - They exist in Unicode and most TTS tokenizers can handle them
# - They are phonetically correct for the Béjaïa dialect
# - F5-TTS and XTTS-v2 both support IPA-like characters

DIGIT_TO_PHONEME = {
    "3": "ɛ",   # ʕayn  — pharyngeal
    "7": "ħ",   # ḥa    — pharyngeal fricative
    "9": "q",   # qaf   — uvular stop
}


# ── Phone number detection ────────────────────────────────────────────
# Real corpus patterns: "034 86 07 80", "0 5 61 83 19 26", etc.
# Must NOT convert digits inside phone numbers.

_PHONE_PATTERNS = [
    # Standard Algerian phone numbers: 0XX XX XX XX or 0X XX XX XX XX
    re.compile(r"\b0\d{1,2}[\s.-]?\d{2}[\s.-]?\d{2}[\s.-]?\d{2}\b"),
    # Shorter local numbers: 2-4 digit patterns in sequence
    re.compile(r"\b\d{2,4}(?:[\s.-]\d{2,4}){2,}\b"),
]

# Pure numeric tokens (bloc numbers, addresses, counts) — don't convert
_PURE_NUMBER = re.compile(r"^\d+$")

# Tokens that are clearly numeric contexts (not arabizi)
_NUMERIC_CONTEXT = re.compile(
    r"(?:bloc|etage|cite|cité|lot|n°|num|chambre|appartement"
    r"|rn|route\s*nationale)\s*\d",
    re.IGNORECASE,
)


def _is_phone_number(text: str, start: int, end: int) -> bool:
    """Check if a digit at position [start:end] is inside a phone number."""
    # Check each phone pattern against the surrounding text
    context_start = max(0, start - 30)
    context_end = min(len(text), end + 30)
    context = text[context_start:context_end]
    for pattern in _PHONE_PATTERNS:
        for m in pattern.finditer(context):
            # If our digit falls within a phone number match
            abs_start = context_start + m.start()
            abs_end = context_start + m.end()
            if abs_start <= start and end <= abs_end:
                return True
    return False


def _protect_numbers(text: str) -> Tuple[str, List[Tuple[str, str]]]:
    """Replace phone numbers and pure numbers with placeholders."""
    placeholders = []
    
    # Protect phone number patterns
    for pattern in _PHONE_PATTERNS:
        for m in pattern.finditer(text):
            placeholder = f"__PHONE_{len(placeholders)}__"
            placeholders.append((placeholder, m.group()))
            text = text[:m.start()] + placeholder + text[m.end():]
    
    # Protect standalone numbers (bloc 5, cite 200, etc.)
    def replace_standalone(m):
        placeholder = f"__NUM_{len(placeholders)}__"
        placeholders.append((placeholder, m.group()))
        return placeholder
    
    text = re.sub(r"\b\d{1,5}\b", replace_standalone, text)
    
    return text, placeholders


def _restore_numbers(text: str, placeholders: List[Tuple[str, str]]) -> str:
    """Restore protected numbers from placeholders."""
    for placeholder, original in reversed(placeholders):
        text = text.replace(placeholder, original)
    return text


def normalize_arabizi_for_tts(text: str) -> str:
    """Convert arabizi text to TTS-friendly pronunciation.
    
    Rules (calibrated from 356 real calls):
    1. Protect phone numbers and standalone digits
    2. Convert arabizi digits (3, 7, 9) inside words to IPA phonemes
    3. Leave French words and pure Latin text untouched
    
    Examples:
        "an3am"     → "anɛam"
        "l7imaya"   → "lħimaya"
        "034 86 07" → "034 86 07" (phone — preserved)
        "bloc 3"    → "bloc 3" (address number — preserved)
        "sa7a"      → "saħa"
        "yterte9"   → "yterteq"
    """
    if not text:
        return text
    
    # Step 1: protect numbers
    text, placeholders = _protect_numbers(text)
    
    # Step 2: convert arabizi digits inside words
    # Only convert 3/7/9 when they appear INSIDE a word (adjacent to letters)
    for digit, phoneme in DIGIT_TO_PHONEME.items():
        # Pattern: digit preceded or followed by a letter
        # This avoids converting isolated digits
        text = re.sub(
            rf"(?<=[a-zA-Zɛħ]){re.escape(digit)}|{re.escape(digit)}(?=[a-zA-Zɛħ])",
            phoneme,
            text,
        )
    
    # Step 3: restore protected numbers
    text = _restore_numbers(text, placeholders)
    
    return text


def normalize_batch(texts: List[str]) -> List[str]:
    """Normalize a list of transcriptions for TTS."""
    return [normalize_arabizi_for_tts(t) for t in texts]


# ── Self-test ─────────────────────────────────────────────────────────

def _self_test():
    """Verify normalizer against known patterns from real corpus."""
    tests = [
        # (input, expected_output, description)
        ("an3am", "anɛam", "ʕayn in common word"),
        ("l7imaya", "lħimaya", "ḥa in service name"),
        ("sa7it", "saħit", "ḥa in thanks"),
        ("sa7a", "saħa", "ḥa in greeting"),
        ("wa7ed", "waħed", "ḥa in number word"),
        ("ma3lich", "maɛlich", "ʕayn in common expression"),
        ("ness3a", "nessɛa", "ʕayn mid-word"),
        ("3la", "ɛla", "ʕayn word-initial"),
        ("ta3", "taɛ", "ʕayn word-final"),
        ("ya3tik", "yaɛtik", "ʕayn in expression"),
        ("yterte9", "yterteq", "qaf word-final (rare)"),
        ("ta9aryeth", "taqaryeth", "qaf mid-word (rare)"),
        # Phone numbers must be PRESERVED
        ("034 86 07 80", "034 86 07 80", "phone number preserved"),
        ("034 35 31 30", "034 35 31 30", "phone number preserved"),
        # Standalone numbers preserved
        ("bloc 3", "bloc 3", "address number preserved"),
        ("cite 500", "cite 500", "address number preserved"),
        # Full sentences
        (
            "- allo l7imaya? - an3am. - ighli yiwen dagi, sa7it!",
            "- allo lħimaya? - anɛam. - ighli yiwen dagi, saħit!",
            "full sentence with mixed arabizi",
        ),
        (
            "- salam 3likoum, l7imaya? - na3am.",
            "- salam ɛlikoum, lħimaya? - naɛam.",
            "greeting with arabizi",
        ),
        (
            "marki ghorek: 034 86 07 80. sa7it.",
            "marki ghorek: 034 86 07 80. saħit.",
            "phone number + arabizi word",
        ),
        # French text untouched
        (
            "envoyez l'ambulance svp",
            "envoyez l'ambulance svp",
            "pure French preserved",
        ),
        # Edge cases
        ("", "", "empty string"),
        ("3", "3", "isolated digit preserved"),
    ]
    
    passed = 0
    failed = 0
    for input_text, expected, desc in tests:
        result = normalize_arabizi_for_tts(input_text)
        status = "✓" if result == expected else "✗"
        if result != expected:
            print(f"  {status} FAIL: {desc}")
            print(f"    input:    '{input_text}'")
            print(f"    expected: '{expected}'")
            print(f"    got:      '{result}'")
            failed += 1
        else:
            print(f"  {status} {desc}")
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"  {passed}/{passed+failed} tests passed")
    if failed:
        print(f"  {failed} FAILED")
    return failed == 0


if __name__ == "__main__":
    print("=== Arabizi Normalizer Self-Test ===\n")
    success = _self_test()
    
    if success:
        # Run on a synthetic example to show output quality
        print("\n=== Sample Normalization ===\n")
        samples = [
            "- allo 7imaya l'madaniya? - l'7imaya l'madaniya f l'istima3, dachu yellan? - azlemd! yiwen amghar thewthit tomobil di rn12, adekar! ighli, idukh, ul it-respirer-ara!",
            "- salam 3likoum les pompiers? - an3am. - kayen wa7ed drab khouya hna f tichy! - anda exact? - zdat la poste. - d'accord at-tacha l'ambulance. - ya3tik sa7a.",
            "- allo allo arwa7u! tech3el tmes g bolimat! fumée partout, 3ajlem! - anda exact? - bolimat cite 200 bloc 5! marki: 034 35 31 30. - d'accord aqlagh ntteddu-d",
        ]
        for s in samples:
            print(f"IN:  {s[:120]}...")
            print(f"OUT: {normalize_arabizi_for_tts(s)[:120]}...")
            print()
    
    exit(0 if success else 1)
