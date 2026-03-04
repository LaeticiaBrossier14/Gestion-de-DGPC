"""Kabyle linguistic guardrail for synthetic emergency-call generation.

This module implements:
- machine-readable guard rules loading from YAML
- transcription normalization before scoring
- blocking + quality rules evaluation
- run calibration report generation and persistence
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, Iterable, List, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field


GuardAction = Literal["pass", "borderline", "reject"]


class VariantReplacement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_value: str = Field(alias="from")
    to_value: str = Field(alias="to")


class NormalizationConfig(BaseModel):
    """NormalizationConfig interface (frozen by V2.1 addendum)."""

    model_config = ConfigDict(extra="forbid")

    lowercase: bool = True
    trim: bool = True
    collapse_whitespace: bool = True
    unicode_to_ascii: Dict[str, str] = Field(default_factory=dict)
    variant_replacements: List[VariantReplacement] = Field(default_factory=list)


class GuardThresholds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    min_chars: int = 30
    min_words: int = 8
    min_kabyle_markers: int = 2
    quality_min_words: int = 18
    median_words_target: int = 60
    pass_score: float = 0.80
    borderline_score: float = 0.65
    negation_window_words: int = 10


class BlockingRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    enabled: bool = True


class QualityRule(BaseModel):
    model_config = ConfigDict(extra="forbid")

    description: str
    penalty: float
    enabled: bool = True


class Lexicons(BaseModel):
    model_config = ConfigDict(extra="forbid")

    greetings: List[str] = Field(default_factory=list)
    closure_markers: List[str] = Field(default_factory=list)
    kabyle_particles: List[str] = Field(default_factory=list)
    kabyle_verbs: List[str] = Field(default_factory=list)
    medical_verbs: List[str] = Field(default_factory=list)
    fire_terms: List[str] = Field(default_factory=list)
    french_markers: List[str] = Field(default_factory=list)
    feminine_nouns: List[str] = Field(default_factory=list)
    masculine_nouns: List[str] = Field(default_factory=list)
    arabizi_markers: List[str] = Field(default_factory=list)


class RegexConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    forbidden_unicode: List[str] = Field(default_factory=list)
    forbidden_sequences: List[str] = Field(default_factory=list)
    negation_token: str = r"\bur\b"
    negation_closure: str = r"\bara\b"


class KabyleGuardRules(BaseModel):
    """KabyleGuardRules interface (frozen by V2.1 addendum)."""

    model_config = ConfigDict(extra="forbid")

    version: str
    source: Dict[str, str] = Field(default_factory=dict)
    thresholds: GuardThresholds = Field(default_factory=GuardThresholds)
    normalization: NormalizationConfig = Field(default_factory=NormalizationConfig)
    blocking_rules: Dict[str, BlockingRule] = Field(default_factory=dict)
    quality_rules: Dict[str, QualityRule] = Field(default_factory=dict)
    lexicons: Lexicons = Field(default_factory=Lexicons)
    regex: RegexConfig = Field(default_factory=RegexConfig)


class GuardResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    normalized_transcription: str
    score: float
    action: GuardAction
    blocking_violations: List[str] = Field(default_factory=list)
    quality_violations: List[str] = Field(default_factory=list)
    penalties: Dict[str, float] = Field(default_factory=dict)
    metrics: Dict[str, float] = Field(default_factory=dict)


class GuardCalibrationRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    timestamp_utc: str
    total_checked: int
    pass_count: int
    borderline_count: int
    reject_count: int
    pass_rate: float
    borderline_rate: float
    reject_rate: float
    mean_score: float
    median_score: float
    blocking_rate: float


class GuardStability(BaseModel):
    model_config = ConfigDict(extra="forbid")

    two_run_stable: Optional[bool] = None
    pass_rate_delta: Optional[float] = None
    mean_score_delta: Optional[float] = None


class GuardCalibrationReport(BaseModel):
    """GuardCalibrationReport interface (frozen by V2.1 addendum)."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    rules_version: str
    source_csv_path: str
    thresholds_used: GuardThresholds
    recommended_thresholds: GuardThresholds
    stability: GuardStability = Field(default_factory=GuardStability)
    runs: List[GuardCalibrationRun] = Field(default_factory=list)


def load_guard_rules(path: Path) -> KabyleGuardRules:
    """Load YAML guard rules with strict validation."""
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid YAML at {path}: expected mapping at root")
    return KabyleGuardRules.model_validate(payload)


def normalize_text(text: str, config: NormalizationConfig) -> str:
    """Normalize transcription before guard scoring."""
    normalized = text or ""
    if config.trim:
        normalized = normalized.strip()
    if config.lowercase:
        normalized = normalized.lower()

    for source, target in config.unicode_to_ascii.items():
        normalized = normalized.replace(source, target)

    for replacement in config.variant_replacements:
        normalized = re.sub(
            rf"\b{re.escape(replacement.from_value)}\b",
            replacement.to_value,
            normalized,
            flags=re.IGNORECASE,
        )

    if config.collapse_whitespace:
        normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    """Check if text contains any of the terms (substring match, case-insensitive)."""
    text_lower = text.lower()
    return any(term and term.lower() in text_lower for term in terms)


def _count_terms(text: str, terms: Iterable[str]) -> int:
    text_lower = text.lower()
    return sum(1 for term in terms if term and term.lower() in text_lower)


def _count_french_like_tokens(text: str, french_markers: Iterable[str]) -> int:
    tokens = re.findall(r"[a-z0-9']+", text.lower())
    if not tokens:
        return 0
    marker_tokens = set()
    for marker in french_markers:
        for part in marker.lower().split():
            marker_tokens.add(part)
    return sum(1 for token in tokens if token in marker_tokens)


def _all_ur_have_ara(text: str, negation_window_words: int) -> bool:
    """Check negation consistency for BOTH ur...ara AND ul...ula (Béjaïa EOR)."""
    tokens = re.findall(r"[a-z0-9']+", text.lower())
    if not tokens:
        return True
    # Map negation openers to their required closers
    neg_pairs = {"ur": "ara", "ul": "ula"}
    for idx, token in enumerate(tokens):
        if token not in neg_pairs:
            continue
        required_closer = neg_pairs[token]
        start = max(0, idx - negation_window_words)
        end = min(len(tokens), idx + negation_window_words + 1)
        if required_closer not in tokens[start:end]:
            return False
    return True


def _gender_mismatch(text: str, feminine_nouns: Iterable[str], masculine_nouns: Iterable[str]) -> bool:
    lowered = text.lower()
    fem_set = set(x.lower() for x in feminine_nouns)
    masc_set = set(x.lower() for x in masculine_nouns)

    for match in re.finditer(r"\byiwen\s+([a-z0-9']+)", lowered):
        noun = match.group(1)
        if noun in fem_set:
            return True
    for match in re.finditer(r"\byiweth\s+([a-z0-9']+)", lowered):
        noun = match.group(1)
        if noun in masc_set:
            return True
    return False


def _has_turn_structure(text: str) -> bool:
    """Heuristic for two-speaker structure in call transcripts."""
    lowered = text.lower()
    if re.search(r"\b(?:operator|caller|agent|appelant|s1|s2)\s*:", lowered):
        return True
    if " - " in text or " — " in text:
        return True

    # Fallback: question/answer pattern with typical acknowledgment tokens.
    if lowered.count("?") >= 2 and _contains_any(
        lowered,
        ["an3am", "ih", "iyeh", "khati", "d'accord", "anda", "anwa", "dachu"],
    ):
        return True
    return False


def _action_from_score(score: float, thresholds: GuardThresholds) -> GuardAction:
    if score >= thresholds.pass_score:
        return "pass"
    if score >= thresholds.borderline_score:
        return "borderline"
    return "reject"


def evaluate_kabyle_guard(
    transcription: str,
    labels: Dict[str, Any],
    rules: KabyleGuardRules,
) -> GuardResult:
    """Evaluate one synthetic transcription using V2.1 rules."""
    raw_text = transcription or ""
    normalized = normalize_text(raw_text, rules.normalization)
    thresholds = rules.thresholds
    lexicons = rules.lexicons

    words = re.findall(r"[a-z0-9']+", normalized)
    word_count = len(words)
    char_count = len(normalized)

    blocking_violations: List[str] = []
    quality_violations: List[str] = []
    penalties: Dict[str, float] = {}
    metrics: Dict[str, float] = {
        "char_count": float(char_count),
        "word_count": float(word_count),
    }

    def block(rule_id: str) -> None:
        if rules.blocking_rules.get(rule_id, BlockingRule(description="", enabled=False)).enabled:
            blocking_violations.append(rule_id)

    # R1: minimal length
    if char_count < thresholds.min_chars or word_count < thresholds.min_words:
        block("R1")

    # R2: opening salutation
    lowered_start = normalized[:120]
    lowered_start = re.sub(
        r"^\s*(?:operator|caller|agent|appelant|s1|s2)\s*:\s*",
        "",
        lowered_start,
        flags=re.IGNORECASE,
    )
    lowered_start = re.sub(r"^\s*[-–—:;,.!?]+\s*", "", lowered_start)
    if not any(lowered_start.startswith(g.lower()) for g in lexicons.greetings):
        block("R2")

    # R3 + R5 combined: Percentage-based word recognition
    # Instead of requiring exact verbs/particles, check what % of words
    # are recognized (from glossary + French + Darija + numbers + common).
    # This is robust to Whisper spelling variations.
    recognized_words = set()
    # Build recognized set from all lexicon lists
    for attr in ['greetings', 'closure_markers', 'kabyle_particles', 'kabyle_verbs',
                 'medical_verbs', 'fire_terms', 'french_markers', 'arabizi_markers',
                 'feminine_nouns', 'masculine_nouns']:
        for term in getattr(lexicons, attr, []):
            if term:
                recognized_words.add(term.lower())
    # Common French words in emergency calls (not just technical)
    recognized_words.update({
        "le", "la", "les", "un", "une", "de", "du", "des", "et", "ou",
        "il", "elle", "on", "je", "tu", "nous", "vous", "ils", "ce",
        "est", "pas", "dans", "pour", "sur", "avec", "qui", "que",
        "ne", "se", "en", "au", "aux", "son", "sa", "ses", "par",
        "oui", "non", "allo", "merci", "bonjour", "monsieur", "madame",
        "pompiers", "ambulance", "accident", "urgence", "adresse",
        "bloc", "etage", "rue", "route", "cite", "quartier", "commune",
        "docteur", "tension", "hopital", "protection", "civile",
        "exactement", "daccord", "sil", "svp", "national", "numero",
        "exact", "poste", "blessure", "victime", "conscient",
        "envoyer", "envoyez", "voiture", "maison", "logement",
    })
    # Common Darija words
    recognized_words.update({
        "kayen", "wesh", "rani", "rana", "khouya", "kifach", "bghit",
        "3endna", "win", "hna", "temma", "wa7ed", "wezid", "bezaf",
    })
    # Count recognized words (word must be in set OR be a substring of a lexicon term)
    recognized_count = 0
    for w in words:
        if len(w) <= 2:  # skip very short words (a, d, g, fi, ...)
            recognized_count += 1
            continue
        if w.isdigit():
            recognized_count += 1
            continue
        if w in recognized_words:
            recognized_count += 1
            continue
        # Substring match: check if word contains or is contained by a recognized term
        if any(w in rw or rw in w for rw in recognized_words if len(rw) >= 3):
            recognized_count += 1
            continue
    recognition_ratio = recognized_count / max(word_count, 1)
    metrics["recognition_ratio"] = round(float(recognition_ratio), 4)
    metrics["recognized_count"] = float(recognized_count)

    # R3: Calibrated from real corpus — Min=6%, P5=24%, Median=41%
    # With Whisper degradation margin (-15%), threshold = 10%
    # This catches only complete garbage (100% unrecognized words)
    if recognition_ratio < 0.10:
        block("R3")

    # R5: kept as soft fallback — only block if 0 emergency-related words at all
    all_emergency_words = set()
    for attr in ['kabyle_verbs', 'medical_verbs', 'fire_terms', 'kabyle_particles']:
        for term in getattr(lexicons, attr, []):
            if term:
                all_emergency_words.add(term.lower())
    has_any_emergency = any(
        ew in normalized for ew in all_emergency_words if len(ew) >= 3
    )
    if not has_any_emergency:
        block("R5")

    # R4: forbid unsupported unicode and encoding artifacts (mojibake)
    for seq in rules.regex.forbidden_sequences:
        if seq and seq in raw_text:
            block("R4")
            break
    for ch in rules.regex.forbidden_unicode:
        if ch in raw_text:
            block("R4")
            break

    # R6: negation consistency — ur must have ara, ul must have ula
    if re.search(rules.regex.negation_token, normalized) and not _all_ur_have_ara(
        normalized,
        negation_window_words=thresholds.negation_window_words,
    ):
        block("R6")

    # R7: invented Kabyle words — reject if too many unverified Kabyle-like words
    _r7_rule = rules.blocking_rules.get("R7", BlockingRule(description="", enabled=False))
    if _r7_rule.enabled:
        try:
            from augmentation.build_lexicon import to_arabizi, is_kabyle_like
            from augmentation.generate_synthetic import _load_lexicon
            lex = _load_lexicon()
            whitelist = set(lex.get('whitelist_flat', []))
        except Exception:
            whitelist = set()
        if whitelist:
            # Check each word: if it looks Kabyle but is NOT in whitelist, flag it
            unverified = []
            _common_fr = {
                "le", "la", "les", "un", "une", "de", "du", "des", "et", "ou",
                "il", "elle", "on", "je", "tu", "nous", "vous", "ils", "ce",
                "est", "sont", "pas", "dans", "pour", "sur", "avec", "qui",
                "que", "ne", "se", "en", "au", "aux", "son", "sa", "ses",
                "mon", "ma", "mes", "ton", "ta", "tes", "par", "plus", "mais",
                "oui", "non", "allo", "merci", "bonjour", "monsieur", "madame",
                "pompiers", "ambulance", "accident", "urgence", "adresse",
                "bloc", "etage", "rue", "route", "cite", "quartier",
                "docteur", "tension", "hopital", "blessure", "victime",
                "exactement", "daccord", "sil", "svp", "national",
            }
            for w in words:
                if len(w) < 3:
                    continue
                if w in whitelist or w in _common_fr:
                    continue
                if w.isdigit():
                    continue
                # Heuristic: looks Kabyle-like?
                has_arabizi = any(m in w for m in ('3', '7', '9', 'gh', 'dh', 'th'))
                has_kab_morph = bool(re.match(r'^(ye|te|ne|tt|i[td])', w)) and len(w) > 3
                if has_arabizi or has_kab_morph:
                    unverified.append(w)
            metrics["unverified_kabyle_words"] = float(len(unverified))
            if len(unverified) > 3:
                block("R7")

    if blocking_violations:
        return GuardResult(
            normalized_transcription=normalized,
            score=0.0,
            action="reject",
            blocking_violations=blocking_violations,
            quality_violations=[],
            penalties={},
            metrics=metrics,
        )

    score = 1.0
    incident_type = str(labels.get("incident_type", "unknown")).strip().lower()
    location = str(labels.get("location", "unknown")).strip()

    def penalize(rule_id: str) -> None:
        rule = rules.quality_rules.get(rule_id, QualityRule(description="", penalty=0.0, enabled=False))
        if not rule.enabled:
            return
        penalties[rule_id] = penalties.get(rule_id, 0.0) + rule.penalty
        quality_violations.append(rule_id)

    # Q1: medical urgency verb
    if incident_type == "medical_emergency" and not _contains_any(normalized, lexicons.medical_verbs):
        penalize("Q1")

    # Q2: fire vocabulary
    if incident_type.startswith("fire_") and not _contains_any(normalized, lexicons.fire_terms):
        penalize("Q2")

    # Q3: location mentioned in text
    if location.lower() in {"", "unknown", "inconnu"}:
        penalize("Q3")
    else:
        location_parts = [part.strip().lower() for part in re.split(r"[/,]", location) if part.strip()]
        if location_parts and not any(part in normalized for part in location_parts):
            penalize("Q3")

    # Q4: closure marker (soft)
    if not _contains_any(normalized, lexicons.closure_markers):
        penalize("Q4")

    # Q5: realistic length under corpus median proxy
    if word_count < thresholds.quality_min_words:
        penalize("Q5")

    # Q6: code-switching ratio, plus script dominance tolerance
    french_like = _count_french_like_tokens(normalized, lexicons.french_markers)
    french_ratio = french_like / max(word_count, 1)
    metrics["french_ratio"] = round(float(french_ratio), 4)
    if french_ratio > 0.60:
        penalize("Q6")

    arabizi_hits = sum(1 for marker in lexicons.arabizi_markers if marker and marker in normalized)
    unicode_gh_hits = raw_text.count("ɣ")
    metrics["arabizi_hits"] = float(arabizi_hits)
    metrics["unicode_gh_hits"] = float(unicode_gh_hits)
    # Policy: Arabizi dominant, Unicode tolerated with low penalty.
    if unicode_gh_hits > 0 and arabizi_hits == 0:
        penalties["Q6"] = penalties.get("Q6", 0.0) + 0.05
        if "Q6" not in quality_violations:
            quality_violations.append("Q6")

    # Q7: grammatical gender consistency (light heuristic)
    if _gender_mismatch(normalized, lexicons.feminine_nouns, lexicons.masculine_nouns):
        penalize("Q7")

    # Q8: incomplete utterance fragments often indicate low-quality generations.
    if re.search(r"[,:;/\-–]\s*$", normalized):
        penalize("Q8")

    # Q9: real calls are predominantly two-speaker interactions.
    has_turns = _has_turn_structure(raw_text)
    metrics["has_turn_structure"] = 1.0 if has_turns else 0.0
    if not has_turns:
        penalize("Q9")

    # Q10: scenario coherence — call must have trigger + evidence + location + action
    scenario_elements = 0
    # Trigger: event verbs or emergency words
    trigger_words = [
        "accident", "ghli", "eghli", "ighli", "theghli", "che3l", "ich3el",
        "thech3el", "thmesth", "tombe", "doukh", "idukh", "yugh", "ithyughen",
        "nuffes", "agression", "noyade", "incendie", "feu", "bless", "iblessi",
        "heurte", "renvers", "explosion", "3erd", "t-qleb", "teqleb",
        "iwthit", "thewthit", "irez", "iterteq", "terteq", "tkard",
        "tfit", "crise", "malaise", "drab", "dharb", "ta7", "hallek",
    ]
    if _contains_any(normalized, trigger_words):
        scenario_elements += 1
    # Evidence: symptoms, observations, severity markers
    evidence_words = [
        "sang", "inconscient", "respir", "tension", "douleur", "cassé",
        "brulure", "fumée", "ddaxan", "blesse", "cri", "mal",
        "yettru", "yettxemmim", "ur yezmir ara",
    ]
    if _contains_any(normalized, evidence_words) or re.search(r"\d+\s*(?:bless|victime|personne)", normalized):
        scenario_elements += 1
    # Location: any commune/place/landmark reference
    location_words = [
        "cite", "cité", "quartier", "bloc", "rue", "route", "rn",
        "pres", "près", "devant", "a cote", "a coté",
    ]
    # Also count if the label location appears in text
    loc_lower = str(labels.get("location", "")).strip().lower()
    if loc_lower and loc_lower not in {"", "unknown", "inconnu"} and loc_lower in normalized:
        scenario_elements += 1
    elif _contains_any(normalized, location_words):
        scenario_elements += 1
    # Action: request for help or operator next step
    action_words = [
        "arwa7", "arwah", "envoy", "3edjled", "zerb", "vite",
        "ambulance", "pompier", "7imaya", "l7imaya", "himaya", "aide", "secour",
        "ta3jil", "s zerb", "svp", "d'accord", "on envoie", "n3awen",
        "azlem", "azlemd", "3ajlem", "activiw", "at-tacha", "ntteddu",
        "at-defkegh", "marki", "chey3emd",
    ]
    if _contains_any(normalized, action_words):
        scenario_elements += 1
    metrics["scenario_elements"] = float(scenario_elements)
    if scenario_elements < 2:
        penalize("Q10")

    # Q11: location grounding — label location should be mentioned in text
    if loc_lower and loc_lower not in {"", "unknown", "inconnu"}:
        loc_parts = [part.strip().lower() for part in re.split(r"[/,]", loc_lower) if part.strip()]
        loc_grounded = any(part in normalized for part in loc_parts) if loc_parts else False
        metrics["location_grounded"] = 1.0 if loc_grounded else 0.0
        if not loc_grounded:
            penalize("Q11")

    score -= sum(penalties.values())
    score = max(0.0, min(1.0, round(score, 4)))
    action = _action_from_score(score, thresholds)
    return GuardResult(
        normalized_transcription=normalized,
        score=score,
        action=action,
        blocking_violations=[],
        quality_violations=quality_violations,
        penalties=penalties,
        metrics=metrics,
    )


def summarize_guard_results(results: List[GuardResult], run_id: str) -> GuardCalibrationRun:
    """Create one run calibration summary."""
    total = len(results)
    scores = [r.score for r in results] or [0.0]
    pass_count = sum(1 for r in results if r.action == "pass")
    borderline_count = sum(1 for r in results if r.action == "borderline")
    reject_count = sum(1 for r in results if r.action == "reject")
    blocking_rejects = sum(1 for r in results if r.blocking_violations)
    return GuardCalibrationRun(
        run_id=run_id,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        total_checked=total,
        pass_count=pass_count,
        borderline_count=borderline_count,
        reject_count=reject_count,
        pass_rate=round(pass_count / max(total, 1), 4),
        borderline_rate=round(borderline_count / max(total, 1), 4),
        reject_rate=round(reject_count / max(total, 1), 4),
        mean_score=round(mean(scores), 4),
        median_score=round(median(scores), 4),
        blocking_rate=round(blocking_rejects / max(total, 1), 4),
    )


def _compute_stability(runs: List[GuardCalibrationRun]) -> GuardStability:
    if len(runs) < 2:
        return GuardStability(two_run_stable=None, pass_rate_delta=None, mean_score_delta=None)
    prev, curr = runs[-2], runs[-1]
    pass_delta = round(abs(curr.pass_rate - prev.pass_rate), 4)
    score_delta = round(abs(curr.mean_score - prev.mean_score), 4)
    stable = pass_delta <= 0.10 and score_delta <= 0.08
    return GuardStability(
        two_run_stable=stable,
        pass_rate_delta=pass_delta,
        mean_score_delta=score_delta,
    )


def _recommend_thresholds(
    thresholds_used: GuardThresholds,
    runs: List[GuardCalibrationRun],
    stability: GuardStability,
) -> GuardThresholds:
    recommended = GuardThresholds.model_validate(thresholds_used.model_dump())
    if len(runs) < 2:
        return recommended

    latest = runs[-1]
    if stability.two_run_stable is False and latest.pass_rate < 0.25:
        recommended.pass_score = round(max(0.75, recommended.pass_score - 0.05), 2)
    elif stability.two_run_stable is True and latest.pass_rate > 0.85:
        recommended.pass_score = round(min(0.90, recommended.pass_score + 0.02), 2)

    max_borderline = round(recommended.pass_score - 0.05, 2)
    recommended.borderline_score = min(recommended.borderline_score, max_borderline)
    recommended.borderline_score = round(max(0.50, recommended.borderline_score), 2)
    return recommended


def update_guard_calibration_report(
    report_path: Path,
    rules: KabyleGuardRules,
    run_summary: GuardCalibrationRun,
) -> GuardCalibrationReport:
    """Persist calibration report and keep the last two runs."""
    existing: Optional[GuardCalibrationReport] = None
    if report_path.exists():
        try:
            payload = json.loads(report_path.read_text(encoding="utf-8"))
            existing = GuardCalibrationReport.model_validate(payload)
        except Exception:
            existing = None

    runs = (existing.runs if existing else []) + [run_summary]
    runs = runs[-2:]
    stability = _compute_stability(runs)
    recommended = _recommend_thresholds(rules.thresholds, runs, stability)
    report = GuardCalibrationReport(
        schema_version="1.0",
        rules_version=rules.version,
        source_csv_path=rules.source.get("csv_path", ""),
        thresholds_used=rules.thresholds,
        recommended_thresholds=recommended,
        stability=stability,
        runs=runs,
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return report
