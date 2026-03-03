"""
Quality Validator — Stage 3: Validate assembled Kabyle transcriptions.

Runs deterministic, rule-based checks on generated transcriptions
to ensure they match real corpus patterns. No LLM calls.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class ValidationResult:
    """Result of validating a single transcription."""
    passed: bool
    score: float  # 0.0–1.0
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def action(self) -> str:
        if self.passed:
            return "accept"
        return "reject"


class QualityValidator:
    """Validate Kabyle emergency call transcriptions against linguistic rules."""

    # ── Blocking Rules (any failure → reject) ──

    def validate(self, transcription: str, incident_type: str = "") -> ValidationResult:
        """Run all validation checks.

        Returns ValidationResult with score and violation details.
        """
        violations: List[str] = []
        warnings: List[str] = []
        checks_passed = 0
        total_checks = 0

        # 1. Minimum length
        total_checks += 1
        if len(transcription.strip()) < 30:
            violations.append(f"TOO_SHORT: {len(transcription)} chars (min 30)")
        else:
            checks_passed += 1

        # 2. Minimum words
        total_checks += 1
        words = transcription.split()
        if len(words) < 8:
            violations.append(f"TOO_FEW_WORDS: {len(words)} words (min 8)")
        else:
            checks_passed += 1

        # 3. Must have dialogue structure (Caller/Operator markers)
        total_checks += 1
        has_caller = bool(re.search(r"Caller:", transcription))
        has_operator = bool(re.search(r"Operator:", transcription))
        if not (has_caller and has_operator):
            violations.append("NO_DIALOGUE_STRUCTURE: missing Caller:/Operator: markers")
        else:
            checks_passed += 1

        # 4. Must have greeting (Allo/Salam/Azul in first 150 chars)
        total_checks += 1
        first150 = transcription[:150].lower()
        greetings = ["allo", "salam", "azul", "sba7", "msa", "assalam", "a n3am"]
        if not any(g in first150 for g in greetings):
            warnings.append("NO_GREETING: no standard greeting in first 150 chars")
        else:
            checks_passed += 1

        # 5. Negation rule: "ur" must have "ara" nearby (±30 chars)
        total_checks += 1
        negation_ok = True
        for m in re.finditer(r"\bur\b", transcription.lower()):
            context = transcription[m.start():min(m.start()+35, len(transcription))].lower()
            if "ara" not in context and "ula" not in context:
                violations.append(
                    f"NEGATION_ORPHAN: 'ur' at pos {m.start()} without 'ara'/'ula' nearby"
                )
                negation_ok = False
                break
        if negation_ok:
            checks_passed += 1

        # 6. "machi" must NOT be followed by a conjugated verb pattern
        total_checks += 1
        machi_ok = True
        for m in re.finditer(r"\bmachi\b", transcription.lower()):
            after = transcription[m.end():m.end()+20].strip().lower()
            # Check for verb patterns (starting with i-, t-, y-, n-)
            if re.match(r"^[ityn]-", after):
                violations.append(
                    f"MACHI_VERB: 'machi' followed by verb pattern at pos {m.start()}"
                )
                machi_ok = False
                break
        if machi_ok:
            checks_passed += 1

        # 7. Not 100% French (must have Kabyle markers)
        total_checks += 1
        kabyle_markers = [
            "an3am", "ih", "iyeh", "dayi", "dagi", "nes3a",
            "athan", "ghli", "che3l", "teddu", "arwa7", "anda",
            "anwa", "anida", "sahit", "saha", "sa7it", "sa7a",
            "ulach", "wlach", "thella", "yella", "agma", "khouya",
            "urgaz", "tamettut", "la3nayak", "s'il vous plaît",
            "pompiers", "ambulance", "himaya", "7imaya", "l'7imaya",
        ]
        found_markers = sum(1 for m in kabyle_markers if m in transcription.lower())
        if found_markers < 2:
            violations.append(
                f"TOO_FEW_KABYLE_MARKERS: only {found_markers} found (min 2)"
            )
        else:
            checks_passed += 1

        # 8. Must not be identical repetition of same phrase
        total_checks += 1
        sentences = [s.strip() for s in re.split(r"[.!?]", transcription) if s.strip()]
        if len(sentences) > 3:
            unique_ratio = len(set(sentences)) / len(sentences)
            if unique_ratio < 0.5:
                violations.append(
                    f"REPETITIVE: {unique_ratio:.0%} unique sentences"
                )
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        # 9. Medical incident must have medical verb
        total_checks += 1
        if incident_type == "medical_emergency":
            med_verbs = ["ghli", "eghli", "doukh", "yugh", "thyugh",
                        "nuffes", "hlek", "ihlek", "crise", "tension",
                        "inconscient", "blessé", "malade"]
            if not any(v in transcription.lower() for v in med_verbs):
                warnings.append("MEDICAL_NO_VERB: no medical verb found")
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        # 10. Fire incident must have fire verb
        total_checks += 1
        if incident_type.startswith("fire_"):
            fire_verbs = ["che3l", "cha3l", "ch3el", "tche3l", "nar",
                         "incendie", "3aq", "the3req"]
            if not any(v in transcription.lower() for v in fire_verbs):
                warnings.append("FIRE_NO_VERB: no fire verb found")
            else:
                checks_passed += 1
        else:
            checks_passed += 1

        # Compute score
        score = checks_passed / max(total_checks, 1)
        passed = len(violations) == 0

        return ValidationResult(
            passed=passed,
            score=score,
            violations=violations,
            warnings=warnings,
        )

    def batch_validate(
        self,
        transcriptions: List[Tuple[str, str]],  # (transcription, incident_type)
    ) -> Tuple[List[int], List[int], float]:
        """Validate a batch and return (accepted_indices, rejected_indices, avg_score).
        """
        accepted = []
        rejected = []
        total_score = 0.0

        for i, (text, itype) in enumerate(transcriptions):
            result = self.validate(text, itype)
            total_score += result.score
            if result.passed:
                accepted.append(i)
            else:
                rejected.append(i)
                print(f"  ✗ Row {i}: {result.violations}")

        avg_score = total_score / max(len(transcriptions), 1)
        return accepted, rejected, avg_score
