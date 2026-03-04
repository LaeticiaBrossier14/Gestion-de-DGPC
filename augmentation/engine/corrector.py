"""
Kabyle Corrector — Data-driven post-transcription correction engine.

Rules are derived empirically from:
- 100 human-corrected transcriptions (annotations_local.csv)
- Golden data benchmark (metadata.json + v1/v2/v3 results)
- Gemini vs Human comparison (annotations_local.json)
- PROFIL_LINGUISTIQUE_BEJAIA.md (15 guard rules)

Two-tier architecture:
  Tier 1 (auto-fix): High-confidence regex-based fixes applied directly
  Tier 2 (suggest): Medium-confidence flags shown to human annotator
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Literal, Tuple


# ── Data Classes ────────────────────────────────────────────

@dataclass
class Correction:
    """A single correction applied or suggested."""
    rule: str                           # e.g., "ROMANIZE", "NEG_ORPHAN"
    tier: Literal[1, 2]                 # 1=auto-fix, 2=suggestion
    original: str                       # matched span
    replacement: str                    # proposed fix ("" for flags)
    position: int                       # char offset
    explanation: str                    # human-readable

    @property
    def icon(self) -> str:
        return "✅" if self.tier == 1 else "💡"


@dataclass
class CorrectionResult:
    """Result of running the corrector on a transcription."""
    original_text: str
    corrected_text: str
    corrections: List[Correction] = field(default_factory=list)

    @property
    def n_autofixes(self) -> int:
        return sum(1 for c in self.corrections if c.tier == 1)

    @property
    def n_suggestions(self) -> int:
        return sum(1 for c in self.corrections if c.tier == 2)

    @property
    def summary(self) -> str:
        return f"{self.n_autofixes} auto-fix, {self.n_suggestions} suggestions"


# ── Corrector Engine ────────────────────────────────────────

class KabyleCorrector:
    """
    Rule-based corrector for Kabyle transcriptions.

    Rules derived from empirical corpus analysis:
    - Arabizi: 3(386), gh(212), 7(173), ch(323), th(156) in 100 transcriptions
    - Negation: only 4 'ur' total in corpus, 2 with 'ara', 2 orphans
    - French ratio: avg 5.2%, max 24%
    - Top markers: d'accord(97), ih(96), saha(51), an3am(36)
    """

    # ── T1: Romanization ─────────────────────────────────
    # Empirical: 20 academic chars found in 100 human transcriptions (slipped through)
    # Gemini uses ɣ(gamma), ɛ(ayn), ṭ(emphatic t), etc. frequently
    ACADEMIC_TO_ARABIZI = {
        "ɣ": "gh",   # gamma → gh (212 'gh' in corpus)
        "ɛ": "3",    # ayn   → 3  (386 '3' in corpus)
        "ħ": "7",    # ha    → 7  (173 '7' in corpus)
        "ʃ": "ch",   # shin  → ch (323 'ch' in corpus)
        "ẓ": "z",    # emphatic z → z
        "ḍ": "d",    # emphatic d → d
        "ṭ": "t",    # emphatic t → t
        "ṣ": "s",    # emphatic s → s
        "ɤ": "gh",   # variant gamma
        "θ": "th",   # theta → th (156 'th' in corpus)
        "č": "ch",   # variant shin
        "ǧ": "dj",   # variant djim
    }

    # ── T1: Article normalization ────────────────────────
    # Corpus patterns: "l'ambulance"(33), "l'accident"(5), "l'bloc"(4)
    ARTICLE_FIXES = [
        (r'\bla\s+ambulance\b', "l'ambulance"),
        (r'\ble\s+accident\b', "l'accident"),
        (r'\ble\s+bloc\b', "l'bloc"),
        (r'\bla\s+tension\b', "l'tension"),
        (r'\bla\s+crise\b', "l'crise"),
        (r'\ble\s+feu\b', "l'feu"),
        (r'\ble\s+camion\b', "l'camion"),
    ]

    # ── T1: Construct state (after prepositions) ─────────
    # Corpus evidence: "n urgaz"(construct), not "n argaz"(free state)
    CONSTRUCT_MAP = {
        "argaz": "urgaz",     # man
        "aman": "waman",      # water
        "amkan": "umkan",     # place
        "axxam": "uxxam",     # house
        "afus": "ufus",       # hand
        "adrar": "udrar",     # mountain
        "abrid": "ubrid",     # road/path
        "awal": "uwal",       # word
    }
    # Prepositions triggering construct state
    CONSTRUCT_TRIGGERS = {"n", "g", "deg", "seg", "s", "gar"}

    # ── T2: Negation ─────────────────────────────────────
    # Corpus: 4 'ur' total — 2 properly followed by 'ara', 2 orphans
    # Rule R6: ur must have ara within ±10 words

    # ── T2: machi usage ──────────────────────────────────
    # Corpus: 15 'machi' in 8 calls — should be followed by noun, NOT verb
    # Verb patterns: starts with i-/t-/y-/n- prefix
    VERB_PREFIX_PATTERN = re.compile(r'^[ityn]-\w+', re.IGNORECASE)

    # ── T2: French ratio ─────────────────────────────────
    # Corpus avg: 5.2%, max 24%. Threshold: >20% is suspicious
    FRENCH_COMMON = frozenset([
        "il", "elle", "est", "le", "la", "les", "un", "une", "de", "du",
        "des", "et", "ou", "mais", "donc", "que", "qui", "dans", "sur",
        "avec", "pour", "pas", "ne", "se", "son", "sa", "ses",
        "nous", "vous", "ils", "elles", "ce", "cette",
        "oui", "non", "bien", "très", "aussi", "comme", "plus",
        "être", "avoir", "faire", "dire",
    ])
    FR_THRESHOLD = 0.20  # >20% → flag (corpus avg is 5.2%)

    # ── T2: Emergency verbs ──────────────────────────────
    # Corpus evidence: ghli(8 calls), nuffes(3), che3l(2), arwa7(2)
    MEDICAL_VERBS = {"ghli", "eghli", "doukh", "yugh", "thyugh",
                     "nuffes", "hlek", "ihlek", "crise", "tension",
                     "inconscient", "blessé", "malade", "diabétique",
                     "cancéreuse", "l'oxygène", "saturation"}
    FIRE_VERBS = {"che3l", "cha3l", "ch3el", "tche3l", "nar", "n-nar",
                  "thmesth", "tmess", "ddaxan", "incendie", "3aq", "the3req"}

    # ── T2: Gender agreement ─────────────────────────────
    # Corpus: yiwen(masc), yiweth(fem) — must agree with noun gender
    FEM_NOUNS = {"tamettut", "taqchichth", "tamghart", "taddart",
                 "tamezyant", "tarbatst", "taqdimt"}
    MASC_NOUNS = {"argaz", "aqchich", "amghar", "amezyan",
                  "adergas", "awtul"}

    def correct(self, text: str, incident_type: str = "") -> CorrectionResult:
        """
        Apply corrections to a transcription.

        Args:
            text: Raw transcription text from Gemini
            incident_type: Optional incident type for context-specific checks

        Returns:
            CorrectionResult with corrected text and all corrections logged
        """
        corrections: List[Correction] = []
        corrected = text

        # ════════════════════════════════════════════════════
        # TIER 1: Auto-fixes (high confidence)
        # ════════════════════════════════════════════════════

        # T1.1: Romanization — replace academic chars with arabizi
        for academic, arabizi in self.ACADEMIC_TO_ARABIZI.items():
            positions = [m.start() for m in re.finditer(re.escape(academic), corrected)]
            if positions:
                corrections.append(Correction(
                    rule="ROMANIZE",
                    tier=1,
                    original=academic,
                    replacement=arabizi,
                    position=positions[0],
                    explanation=f"Romanisation académique '{academic}' → arabizi '{arabizi}' "
                                f"(corpus: {self._arabizi_count(arabizi)} occurrences)"
                ))
                corrected = corrected.replace(academic, arabizi)

        # T1.2: Article normalization
        for pattern, replacement in self.ARTICLE_FIXES:
            match = re.search(pattern, corrected, re.IGNORECASE)
            if match:
                corrections.append(Correction(
                    rule="ARTICLE",
                    tier=1,
                    original=match.group(0),
                    replacement=replacement,
                    position=match.start(),
                    explanation=f"Article kabylisé: '{match.group(0)}' → '{replacement}'"
                ))
                corrected = re.sub(pattern, replacement, corrected, flags=re.IGNORECASE)

        # T1.3: Construct state after prepositions
        for trigger in self.CONSTRUCT_TRIGGERS:
            pattern = rf'\b{trigger}\s+({")|(".join(self.CONSTRUCT_MAP.keys())})\b'
            for match in re.finditer(pattern, corrected, re.IGNORECASE):
                free = match.group(1) or match.group(2)
                if free and free.lower() in self.CONSTRUCT_MAP:
                    annexed = self.CONSTRUCT_MAP[free.lower()]
                    old_span = match.group(0)
                    new_span = f"{trigger} {annexed}"
                    corrections.append(Correction(
                        rule="CONSTRUCT",
                        tier=1,
                        original=old_span,
                        replacement=new_span,
                        position=match.start(),
                        explanation=f"État construit: '{free}' → '{annexed}' après '{trigger}'"
                    ))
                    corrected = corrected[:match.start()] + new_span + corrected[match.end():]

        # T1.4: Fix Gemini-style dialogue labels → match corpus format
        # Corpus: only 3% use labels. If Gemini outputs "A:" and "O:" labels,
        # convert to dashes which is the 2nd most common format (31%)
        if re.search(r'^[AO]:\s', corrected, re.MULTILINE):
            # Gemini often uses "A:" for Appelant, "O:" for Operateur
            corrected_new = re.sub(r'^A:\s*', '— ', corrected, flags=re.MULTILINE)
            corrected_new = re.sub(r'^O:\s*', '— ', corrected_new, flags=re.MULTILINE)
            if corrected_new != corrected:
                corrections.append(Correction(
                    rule="DIALOGUE_FMT",
                    tier=1,
                    original="A:/O: labels",
                    replacement="— dashes",
                    position=0,
                    explanation="Format dialogue: labels A:/O: → tirets (31% du corpus)"
                ))
                corrected = corrected_new

        # ════════════════════════════════════════════════════
        # TIER 2: Suggestions (medium confidence)
        # ════════════════════════════════════════════════════

        c_lower = corrected.lower()

        # T2.1: Negation — orphan "ur" without "ara"
        for m in re.finditer(r'\bur\b', c_lower):
            # Check ±50 chars for "ara"
            window = c_lower[m.start():min(m.start() + 50, len(c_lower))]
            if "ara" not in window and "ula" not in window:
                corrections.append(Correction(
                    rule="NEG_ORPHAN",
                    tier=2,
                    original=window[:30],
                    replacement="(ajouter 'ara' après le verbe)",
                    position=m.start(),
                    explanation="Négation incomplète: 'ur' sans 'ara' — "
                                "règle R6: ur {verbe} ara"
                ))

        # T2.2: machi + verb (should be machi + noun)
        for m in re.finditer(r'\bmachi\b', c_lower):
            after = corrected[m.end():m.end() + 25].strip()
            if self.VERB_PREFIX_PATTERN.match(after):
                corrections.append(Correction(
                    rule="MACHI_VERB",
                    tier=2,
                    original=f"machi {after[:15]}",
                    replacement="(machi + nom, pas verbe)",
                    position=m.start(),
                    explanation="'machi' s'utilise avec un nom, jamais un verbe conjugué"
                ))

        # T2.3: French ratio check
        words = c_lower.split()
        if words:
            fr_count = sum(1 for w in words if w in self.FRENCH_COMMON)
            fr_ratio = fr_count / len(words)
            if fr_ratio > self.FR_THRESHOLD:
                corrections.append(Correction(
                    rule="FRENCH_HEAVY",
                    tier=2,
                    original=f"{fr_ratio:.0%} mots fr",
                    replacement=f"(corpus avg: 5.2%, max 24%)",
                    position=0,
                    explanation=f"Ratio français {fr_ratio:.0%} — au-dessus du seuil "
                                f"({self.FR_THRESHOLD:.0%}). Corpus avg: 5.2%"
                ))

        # T2.4: Missing medical verbs for medical_emergency
        if incident_type and "medical" in incident_type.lower():
            if not any(v in c_lower for v in self.MEDICAL_VERBS):
                corrections.append(Correction(
                    rule="MED_MISSING",
                    tier=2,
                    original="(aucun verbe médical)",
                    replacement="ghli/doukh/yugh/nuffes",
                    position=0,
                    explanation="Appel médical sans verbe d'urgence "
                                "(corpus: ghli dans 8 appels, nuffes dans 3)"
                ))

        # T2.5: Missing fire verbs for fire incidents
        if incident_type and "fire" in incident_type.lower():
            if not any(v in c_lower for v in self.FIRE_VERBS):
                corrections.append(Correction(
                    rule="FIRE_MISSING",
                    tier=2,
                    original="(aucun verbe feu)",
                    replacement="che3l/thmesth/ddaxan",
                    position=0,
                    explanation="Appel incendie sans vocabulaire feu "
                                "(corpus: che3l dans 2 appels)"
                ))

        # T2.6: No greeting in first line
        first100 = c_lower[:100]
        greetings = ["allo", "salam", "azul", "sba7", "msa", "assalam"]
        if not any(g in first100 for g in greetings):
            corrections.append(Correction(
                rule="NO_GREETING",
                tier=2,
                original="(pas de salutation)",
                replacement="Allo/Salam alaykoum",
                position=0,
                explanation="Salutation absente — corpus: Allo(59%), Salam(39%)"
            ))

        # T2.7: Gender mismatch (yiwen/yiweth)
        for m in re.finditer(r'\byiwen\b', c_lower):
            after_words = c_lower[m.end():m.end() + 30].split()[:2]
            for w in after_words:
                if w in self.FEM_NOUNS:
                    corrections.append(Correction(
                        rule="GENDER",
                        tier=2,
                        original=f"yiwen {w}",
                        replacement=f"yiweth {w}",
                        position=m.start(),
                        explanation=f"Genre: '{w}' est féminin → 'yiweth' au lieu de 'yiwen'"
                    ))
        for m in re.finditer(r'\byiweth\b', c_lower):
            after_words = c_lower[m.end():m.end() + 30].split()[:2]
            for w in after_words:
                if w in self.MASC_NOUNS:
                    corrections.append(Correction(
                        rule="GENDER",
                        tier=2,
                        original=f"yiweth {w}",
                        replacement=f"yiwen {w}",
                        position=m.start(),
                        explanation=f"Genre: '{w}' est masculin → 'yiwen' au lieu de 'yiweth'"
                    ))

        return CorrectionResult(
            original_text=text,
            corrected_text=corrected,
            corrections=corrections,
        )

    @staticmethod
    def _arabizi_count(char: str) -> str:
        """Return corpus frequency for documentation."""
        counts = {"gh": "212", "3": "386", "7": "173", "ch": "323",
                  "th": "156", "z": "~30", "d": "~50", "t": "~80",
                  "s": "~40", "dj": "~10"}
        return counts.get(char, "?")


# ── Quick test ──────────────────────────────────────────────
if __name__ == "__main__":
    corrector = KabyleCorrector()

    # Test cases derived from real Gemini errors
    tests = [
        # T1.1: Romanization (from annotations_local.json comparison)
        ("Azul fell-ak a ṭṭbib, ɣer yiwen n l-mreḍ", ""),
        # T1.2: Article
        ("la ambulance dagi, la tension sighlin", "medical_emergency"),
        # T1.3: Construct state
        ("n argaz yella deg axxam", ""),
        # T1.4: Dialogue labels
        ("A: Allo?\nO: An3am?\nA: Yella l'accident", ""),
        # T2.1: Negation orphan
        ("ur yezmir chwiya, bessah ma3lich", ""),
        # T2.2: machi + verb
        ("machi i-teddu gher sbitar", ""),
        # T2.3: French heavy
        ("il est dans la maison, il est pas bien, elle est malade", "medical_emergency"),
        # Real corpus sample (should pass clean)
        ("Allo? salam alaykoum l'Himayai, d-aqla-gh dagi gher la DGS",  ""),
    ]

    print("=" * 60)
    print("CORRECTOR UNIT TESTS")
    print("=" * 60)

    for i, (text, itype) in enumerate(tests):
        result = corrector.correct(text, itype)
        print(f"\n[Test {i+1}]")
        print(f"  IN:  {text[:70]}...")
        print(f"  OUT: {result.corrected_text[:70]}...")
        print(f"  {result.summary}")
        for c in result.corrections:
            print(f"    {c.icon} {c.rule}: '{c.original}' → '{c.replacement}' — {c.explanation[:60]}")
