"""
Generate synthetic emergency-call rows from augmentation tasks.

Input:
- ml_pipeline/dataset/synthetic_generation/generation_tasks.jsonl

Output:
- ml_pipeline/dataset/annotations_synthetic.jsonl

Rules:
- facts only in labels (no urgency/dispatch/assets/staffing)
- schema aligned with ml_pipeline/dataset/enums.py
- row format aligned with final/train_real_seed.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    # Allow direct script execution without package installation.
    sys.path.insert(0, str(ROOT))

from ml_pipeline.dataset.enums import IncidentType, InjurySeverity, TriState
from augmentation.kabyle_guard import (
    GuardResult,
    evaluate_kabyle_guard,
    load_guard_rules,
    summarize_guard_results,
    update_guard_calibration_report,
)
from pydantic import BaseModel, ConfigDict


FACT_FIELDS = [
    "incident_type",
    "location",
    "victims_count",
    "injury_severity",
    "fire_present",
    "trapped_persons",
    "weapons_involved",
    "hazmat_involved",
]
FORBIDDEN_FIELDS = {"urgency", "dispatch", "assets", "staffing"}
MOJIBAKE_MARKERS = ("Ã", "â€™", "â€œ", "â€", "â€“", "â€”", "�")

# --- KABYLE LEXICON (Memory Core) ----------------------------------------
_LEXICON_PATH = Path(__file__).resolve().parent / "kabyle_lexicon.yaml"
_KABYLE_LEXICON: Optional[Dict[str, Any]] = None


def _load_lexicon() -> Dict[str, Any]:
    """Load the kabyle lexicon (cached after first call)."""
    global _KABYLE_LEXICON
    if _KABYLE_LEXICON is not None:
        return _KABYLE_LEXICON
    if not _LEXICON_PATH.exists():
        print(f"[WARN] Lexicon not found at {_LEXICON_PATH}, skipping whitelist.")
        _KABYLE_LEXICON = {}
        return _KABYLE_LEXICON
    with open(_LEXICON_PATH, 'r', encoding='utf-8') as f:
        _KABYLE_LEXICON = yaml.safe_load(f) or {}
    wl_count = _KABYLE_LEXICON.get('whitelist_count', 0)
    print(f"[OK] Lexicon loaded: {wl_count} whitelist words")
    return _KABYLE_LEXICON


def _build_vocab_whitelist_block() -> str:
    """Legacy flat whitelist — kept as fallback."""
    return ""


# --- SCENARIO GLOSSARY (LexC-Gen inspired) --------------------------------
_GLOSSARY_PATH = Path(__file__).resolve().parent / "scenario_glossary.yaml"
_SCENARIO_GLOSSARY: Optional[Dict[str, Any]] = None


def _load_glossary() -> Dict[str, Any]:
    """Load scenario glossary (cached)."""
    global _SCENARIO_GLOSSARY
    if _SCENARIO_GLOSSARY is not None:
        return _SCENARIO_GLOSSARY
    if not _GLOSSARY_PATH.exists():
        print(f"[WARN] Glossary not found at {_GLOSSARY_PATH}")
        _SCENARIO_GLOSSARY = {}
        return _SCENARIO_GLOSSARY
    with open(_GLOSSARY_PATH, 'r', encoding='utf-8') as f:
        _SCENARIO_GLOSSARY = yaml.safe_load(f) or {}
    scenarios = [k for k in _SCENARIO_GLOSSARY if k != '_common']
    print(f"[OK] Scenario glossary loaded: {len(scenarios)} incident types")
    return _SCENARIO_GLOSSARY


def _build_scenario_glossary(incident_type: str) -> str:
    """Build a targeted bilingual glossary block for one incident type.

    Instead of dumping 500 random words, this injects ONLY the 15-20 Kabyle
    words semantically relevant to the scenario, with their French meaning.
    Follows LexC-Gen (ACL 2024) approach: bilingual lexicon conditioning.
    """
    glossary = _load_glossary()
    if not glossary:
        return _build_vocab_whitelist_block()  # fallback

    common = glossary.get('_common', {})
    scenario = glossary.get(incident_type, glossary.get('unknown', {}))

    sections = []
    sections.append(f"--- SCENARIO GLOSSARY: {incident_type} ---")
    sections.append("For this call, use ONLY these verified Kabyle words with their French meaning.")
    sections.append("If you need a word not listed, use French (natural code-switching).")
    sections.append("DO NOT invent Kabyle words.")
    sections.append("")

    # Greetings & closings (shared)
    greetings = common.get('greetings', [])
    closings = common.get('closings', [])
    if greetings:
        sections.append(f"GREETINGS: {', '.join(greetings)}")
    if closings:
        sections.append(f"CLOSINGS: {', '.join(closings)}")
    sections.append("")

    # Discourse markers (shared)
    discourse = common.get('discourse', {})
    if discourse:
        sections.append("DISCOURSE MARKERS:")
        for concept_fr, kab_forms in discourse.items():
            sections.append(f"  {concept_fr.replace('_', ' ')} → {', '.join(kab_forms)}")
        sections.append("")

    # Negation (shared)
    negation = common.get('negation', {})
    if negation:
        sections.append("NEGATION:")
        for concept_fr, kab_forms in negation.items():
            sections.append(f"  {concept_fr.replace('_', ' ')} → {', '.join(kab_forms)}")
        sections.append("")

    # Scenario-specific verbs
    verbs = scenario.get('verbs', {})
    if verbs:
        sections.append(f"VERBS ({incident_type}):")
        for concept_fr, kab_forms in verbs.items():
            sections.append(f"  {concept_fr.replace('_', ' ')} → {', '.join(kab_forms)}")
        sections.append("")

    # Scenario-specific nouns
    nouns = scenario.get('nouns', {})
    if nouns:
        sections.append(f"NOUNS ({incident_type}):")
        for concept_fr, kab_forms in nouns.items():
            sections.append(f"  {concept_fr.replace('_', ' ')} → {', '.join(kab_forms)}")
        sections.append("")

    # Example expressions
    expressions = scenario.get('expressions', [])
    if expressions:
        sections.append("EXAMPLE EXPRESSIONS:")
        for expr in expressions[:6]:  # max 6 to save context
            sections.append(f"  {expr}")
        sections.append("")

    # French loanwords (natural code-switching)
    loanwords = scenario.get('french_loanwords', [])
    if loanwords:
        sections.append(f"FRENCH LOANWORDS (natural): {', '.join(loanwords)}")
        sections.append("")

    sections.append("--- END GLOSSARY ---")
    return "\n".join(sections)


# --- SYNTH exercise types (inspired by Pleias SYNTH methodology) ----------
# Weights sum to 100 and reflect Béjaïa linguistic profile priorities.
# Négation (20%) and Géo (25%) are highest because they are the weakest
# signals and the primary competitive advantage, respectively.
SYNTH_EXERCISE_TYPES = {
    "ex1_urgency_verbs": 15,       # ighli/idukh/it-respirer-ara + hybrid expressions
    "ex2_kabyle_negation": 15,     # ul…ula (Béjaïa), ur…ara, khati, machi, ulach
    "ex3_geographic_anchor": 15,   # commune + quartier + landmark (zdat/en face)
    "ex4_code_switching": 10,      # KAB/FR/Darija trilingual mix
    "ex5_open_close": 10,          # Allo/Salam/panic opening + saha/sahit closing
    "ex6_full_flow_negative": 10,  # non-emergency / false alarm / wrong number
    "ex7_redirect": 15,            # caller outside zone → operator gives local post number
    "ex8_panic": 10,               # panic: no greeting, repeated words, cries, chaotic
}
_EXERCISE_NAMES = list(SYNTH_EXERCISE_TYPES.keys())
_EXERCISE_WEIGHTS = [SYNTH_EXERCISE_TYPES[k] for k in _EXERCISE_NAMES]


def pick_exercise_type(rng: random.Random | None = None) -> str:
    """Select an exercise type using weighted random sampling."""
    chooser = rng or random
    return chooser.choices(_EXERCISE_NAMES, weights=_EXERCISE_WEIGHTS, k=1)[0]

VALID_INCIDENT_TYPES = {e.value for e in IncidentType}
VALID_INJURY_SEVERITY = {e.value for e in InjurySeverity}
VALID_TRISTATE = {e.value for e in TriState}


class SyntheticLabels(BaseModel):
    model_config = ConfigDict(extra="forbid")
    incident_type: str
    location: str
    victims_count: Optional[int]
    injury_severity: str
    fire_present: str
    trapped_persons: str
    weapons_involved: str
    hazmat_involved: str


class SyntheticExample(BaseModel):
    model_config = ConfigDict(extra="forbid")
    transcription: str
    chain_of_thought: str
    labels: SyntheticLabels


class GenerationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    examples: List[SyntheticExample]


GENERATION_SYSTEM_PROMPT = """You generate synthetic emergency call transcriptions for model training.
These calls simulate real calls to the Bejaia (Algeria) emergency dispatch center (7imaya l'madaniya).

ROMANISATION ARABIZI (OBLIGATOIRE — violations = rejet automatique):
  | Son    | Écris | JAMAIS | Correct example      |
  | 3ayn   | 3     | ɛ      | an3am, ma3lich       |
  | 7a     | 7     | ħ      | l7uma, sa7a, 7imaya  |
  | qaf    | 9     | q      | 9abel                |
  | ghayn  | gh    | ɣ      | ghli, eghli, gher    |
  | tha    | th    | θ      | thella, thmesth      |
  | shin   | ch    | ʃ      | chwiya, che3l, dachu |
  Emphatics ẓ ḍ ṭ ṣ → z d t s (no diacritics).
  CRITICAL: NEVER use ɣ, ɛ, ḥ, ʃ, θ. Write gh, 3, 7, ch, th instead.
  Example: write "yezdagh" NOT "yezdaɣ"; write "ur yezmir ara" NOT "ur yeẓmir ara".

BÉJAÏA DIALECT (EOR — Eastern Kabyle, NOT standard Kabyle):
  Preverbal future: di {verb} (dominant, 13/19 parlers) NOT ad {verb}.
    Example: "di yeghli" = he will fall (NOT "ad yeghli").
  Negation: ul {verb} ula (dominant 13/19) > ur {verb} ara (6/19 western).
    Example: "ul yezmir ula" = he can't (dominant Béjaïa form).
  Pronouns: cekk (you masc, 14/19), cemm (you fem, 12/19) NOT kečč/kemm.
  Copula 'd': d acu? (what is it?), d tametut (it's a woman), d urgent (it's urgent).

LINGUISTIC STYLE (trilingual Béjaïa calls):
  Real calls are Kabyle-French-Darija trilingual. The dominant pattern:
  - KABYLE provides: verbs, particles, negation, construct state 'n', questions
  - FRENCH provides: infrastructure (bloc, étage, ambulance, accident, tension, docteur)
  - DARIJA (Arabic) appears in ~15% of calls: kayen (there is), wesh (what),
    rani (I am), khouya (brother), bghit (I want), kifach (how), win (where)

  KABYLE DISCOURSE MARKERS:
  dayi/dagi (here), tura (now), chwiya (a little), an3am (yes), anda (where),
  dachu/dachou (what), la3nayak/lu3aghawend (please help), meskin/meskint (poor thing),
  ma3lich (please/it's ok), dakur/dakour (d'accord in Kabyle pronunciation).

  KABYLE VERBS by scenario:
  Medical: ighli/theghli (fell), idukh (fainted), ithyughen (what hurts him),
           tfit la crise (had a crisis), it-respirer-ara (can't breathe)
  Fire: thech3el/ich3el tmess (caught fire), iterteq (exploded), tkard tmess (fire took)
  Accident: t-qleb (flipped), iwthitt tomobil (car hit her), idhem (crushed),
            iblessi (injured), irez (broke)
  Urgency: azlem/azlemd (hurry!), arwa7u (come!), activiw (activate!), 3ajlem (hurry!)

NEGATION FORMS:
  - Circumfixe: ul {verbe} ula (Béjaïa dominant), ur {verbe} ara (standard)
  - Nominal: ulach / wlach (there is none)
  - Identity: machi + NOM (ex: 'machi enceinte')
  - Refusal: khati / xati (no)

OPERATOR STANDARD FORMULAS (use these exact phrases for the operator):
  Opening: "l'7imaya l'madaniya f l'istima3" or "m3akoum l'7imaya l'madaniya"
  Questions: "anda exact?", "dachu yellan?", "anwa l'bloc?", "wach la commune?"
           "est-ce qu'il est conscient?", "sh7al n l'blessés?"
  Dispatch: "d'accord, at-tacha l'ambulance", "aqlagh ntteddu-d" (we're coming)
  Redirect: "at-defkegh numéro n [poste], marki ghorek" (I'll give you the number)
  Close: "d'accord a {gma/madame/sidi}", "sa7it", "ya3tik sa7a"

STRESS-DEPENDENT BEHAVIOUR:
  When stress=calm: Normal greeting (Salam/Allo) → structured exchange.
  When stress=hurried: Short greeting → fast incident report → urgent tone.
  When stress=panic: NO greeting! Caller launches directly into crisis.
    - Repeated/elongated words: "allo allo allo!", "azlemd azlemd!", "s'il vous plaît!"
    - Incomplete sentences, cries: "arwa7u! tech3el! aqlin hesslegh g kham!"
    - Interjections of distress: "yaddi!", "ya rebbi!", "ahhhh"
    - Operator tries to calm: "Madame! s'te plaît!", "asber a madame"

SCENARIO COHERENCE (CRITICAL — violations = rejet):
  RULE: Each call has EXACTLY ONE incident with ONE causal chain.
  NEVER combine two unrelated events. The caller describes ONE thing, the operator
  asks about THAT thing. No "he fell sick AND a car hit him" — pick ONE.

  CAUSAL CHAIN TEMPLATES (pick one, instantiate with variables):
  medical_fall: someone fell → symptoms (idukh/iblessi/irez) → need ambulance
  medical_crisis: had a crisis (cardiac/epileptic/tension) → can't move/breathe → urgent transport
  medical_other: someone sick → vague symptoms → transport to sbitar
  accident_vehicle: car/moto accident (t-qleb/derapage) → blessés → ambulance
  accident_pedestrian: car hit person (iwthitt tomobil) → blessé → ambulance
  fire: something caught fire (thech3el tmess) → smoke/danger → pompiers
  assault: someone attacked (dharbou/iwthes) → blessé → urgence
  hazmat: gas leak (fuite lgaz) or explosion (iterteq) → danger → pompiers + Sonelgaz
  structural: wall/ceiling fell (yeghli sour/plafond) → trapped/injured → rescue

DIALOGUE PHASES (MANDATORY — follow this order):
  1) OPENING: Caller greets + identifies service (1-2 lines).
     OR if panic: Caller launches directly "Allo allo! arwa7u! tech3el!"
  2) INCIDENT: Caller states ONE incident (1-2 lines). Use "ness3a/illa/thella + [event]".
  3) LOCATION: Operator asks "anda?" — Caller gives landmarks (3-6 exchanges).
     Location uses: cité+bloc+étage, "zdat/en face [repère]", village name, route+repère.
     Operator may ask: "anwa l'bloc?", "wach la commune?", "wach la famille?"
  4) CLARIFICATION: Operator asks about condition (1-2 exchanges).
     "dachu yellan?", "est-ce qu'il est conscient?", "iblessi?"
  5) CLOSING: Dispatch or redirect + farewell (1-2 lines).
     Dispatch: "d'accord, at-tacha l'ambulance" / "aqlagh ntteddu-d"
     Redirect: "at-defkegh numéro n [poste local]: 034..."
     Farewell: "sa7a", "sahit", "barak Allahu fik"

CHAIN OF THOUGHT (MANDATORY):
  You MUST include a `chain_of_thought` field explaining step-by-step how you go from
  the transcription to the final structured labels. Map Kabyle/Arabizi terms to English
  schema fields (e.g. "ighli → fell → medical_emergency, idukh → fainted → severe").

QUALITY PRIORITY:
  Naturalness and semantic coherence > mechanical checklist.
  NEVER insert particles/verbs just to pass rules.
  ONE incident per call. ONE causal chain. No contradictions.

Forbidden in labels: urgency, dispatch, assets, staffing.
Use only Bejaia geography provided in prompt context.
"""


def load_tasks(plan_path: Path) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []
    if not plan_path.exists():
        return tasks
    with plan_path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            raw = raw.strip()
            if not raw:
                continue
            tasks.append(json.loads(raw))
    return tasks


def load_real_calls(csv_path: Path) -> List[Dict[str, str]]:
    """Load real annotated calls used for style guidance."""
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [dict(row) for row in csv.DictReader(handle)]
    return rows


def load_real_style_profile(profile_path: Path) -> Dict[str, Any]:
    if not profile_path.exists():
        return {}
    try:
        return json.loads(profile_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _safe_ratio(profile: Dict[str, Any], key: str) -> float:
    markers = profile.get("dialect_markers", {})
    marker = markers.get(key, {})
    ratio = marker.get("ratio", 0.0)
    if isinstance(ratio, (int, float)):
        return float(ratio)
    return 0.0


def build_real_dna_block(profile: Dict[str, Any]) -> str:
    """Summarize real-corpus DNA as prompt guidance."""
    if not profile:
        return ""

    two_speaker = profile.get("two_speaker_like", {})
    two_speaker_ratio = two_speaker.get("ratio", 0.0)
    if not isinstance(two_speaker_ratio, (int, float)):
        two_speaker_ratio = 0.0

    allor = _safe_ratio(profile, "allo")
    salamr = _safe_ratio(profile, "salam")
    an3amr = _safe_ratio(profile, "an3am")
    dayir = _safe_ratio(profile, "dayi")
    khatir = _safe_ratio(profile, "khati")
    pompiersr = _safe_ratio(profile, "l_pompiers")
    ambur = _safe_ratio(profile, "l_ambulance")

    return (
        "\n--- REAL CALL DNA (from real corpus) ---\n"
        f"- Two-speaker turn-taking: ~{two_speaker_ratio * 100:.1f}% of calls\n"
        f"- Frequent opening tokens: Allo ~{allor * 100:.1f}%, Salam ~{salamr * 100:.1f}%\n"
        f"- Frequent interaction markers: an3am ~{an3amr * 100:.1f}%, dayi ~{dayir * 100:.1f}%, khati ~{khatir * 100:.1f}%\n"
        f"- Service lexical anchors: l'pompiers ~{pompiersr * 100:.1f}%, l'ambulance ~{ambur * 100:.1f}%\n"
        "- Real calls are not monologues: they include clarifications, hesitation, corrections, and routing.\n"
        "- Keep chronology coherent: incident -> clarification -> dispatch/routing decision.\n"
        "--- END REAL CALL DNA ---\n"
    )


def _sanitize_real_text(text: str, max_chars: int = 650) -> str:
    cleaned = (text or "").strip()
    cleaned = re.sub(r"\b0\d(?:[\s.\-]?\d){7,}\b", "<PHONE>", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:max_chars]


def _looks_mojibake(text: str) -> bool:
    return any(marker in text for marker in MOJIBAKE_MARKERS)


def select_real_fewshots(
    real_calls: List[Dict[str, str]],
    incident_type: str,
    rng: random.Random,
    count: int,
) -> List[Dict[str, str]]:
    if not real_calls or count <= 0:
        return []

    def has_text(row: Dict[str, str]) -> bool:
        text = (row.get("Transcription") or "").strip()
        if not text:
            return False
        # Avoid feeding encoding-noisy examples into the prompt.
        if _looks_mojibake(text):
            return False
        return True

    incident_type = (incident_type or "unknown").strip().lower()
    same_type = [
        row
        for row in real_calls
        if has_text(row) and (row.get("incident_type") or "").strip().lower() == incident_type
    ]
    pool = same_type if len(same_type) >= count else [row for row in real_calls if has_text(row)]
    if not pool:
        return []

    # Deduplicate by normalized transcription.
    unique: Dict[str, Dict[str, str]] = {}
    for row in pool:
        key = (row.get("Transcription") or "").strip().lower()
        if key and key not in unique:
            unique[key] = row
    unique_rows = list(unique.values())
    if len(unique_rows) <= count:
        return unique_rows

    # Keep incident-specific examples when available, then fill from global pool.
    unique_same = [
        row for row in unique_rows if (row.get("incident_type") or "").strip().lower() == incident_type
    ]
    if len(unique_same) >= count:
        return rng.sample(unique_same, k=count)
    if unique_same:
        by_id = {id(row) for row in unique_same}
        rest = [row for row in unique_rows if id(row) not in by_id]
        needed = max(0, count - len(unique_same))
        return unique_same + (rng.sample(rest, k=needed) if len(rest) >= needed else rest)

    return rng.sample(unique_rows, k=count)


def build_real_fewshot_block(fewshots: List[Dict[str, str]]) -> str:
    if not fewshots:
        return ""

    lines = [
        "\n--- FEW-SHOT REAL CALL STYLES (ANONYMIZED, STYLE ONLY) ---",
        "Do NOT copy text verbatim. Reuse discourse structure and realism only.",
    ]
    for idx, row in enumerate(fewshots, start=1):
        transcription = _sanitize_real_text(str(row.get("Transcription", "")))
        incident = str(row.get("incident_type", "unknown")).strip() or "unknown"
        location_hint = (
            str(row.get("location_description", "")).strip()
            or str(row.get("lieu", "")).strip()
            or str(row.get("commune", "")).strip()
            or "unknown"
        )
        intent = str(row.get("intent", "unknown")).strip() or "unknown"
        lines.append(
            f"[Example {idx}] incident={incident}; intent={intent}; location_hint={location_hint}\n"
            f"Transcript: {transcription}"
        )
    lines.append("--- END FEW-SHOT ---\n")
    return "\n".join(lines)


def parse_json_response(text: str) -> List[Dict[str, Any]]:
    content = (text or "").strip()
    if not content:
        return []

    parsed: Any
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"```json\s*(.*?)\s*```", content, flags=re.DOTALL | re.IGNORECASE)
        if not match:
            return []
        parsed = json.loads(match.group(1))

    if isinstance(parsed, list):
        return [x for x in parsed if isinstance(x, dict)]

    if isinstance(parsed, dict):
        examples = parsed.get("examples")
        if isinstance(examples, list):
            return [x for x in examples if isinstance(x, dict)]
        if "transcription" in parsed and ("labels" in parsed or "extraction" in parsed):
            return [parsed]

    return []


def parse_generation_response(response: Any) -> List[Dict[str, Any]]:
    """Parse Gemini response, preferring structured payload when available."""
    parsed_obj = getattr(response, "parsed", None)
    if parsed_obj is not None:
        if isinstance(parsed_obj, BaseModel):
            payload = parsed_obj.model_dump()
        else:
            payload = parsed_obj

        if isinstance(payload, dict):
            examples = payload.get("examples")
            if isinstance(examples, list):
                return [x for x in examples if isinstance(x, dict)]
        if isinstance(payload, list):
            return [x for x in payload if isinstance(x, dict)]

    return parse_json_response(getattr(response, "text", ""))


def clean_tristate(value: Any) -> str:
    v = str(value).strip().lower()
    if v in {"yes", "oui", "true", "1"}:
        return "yes"
    if v in {"no", "non", "false", "0"}:
        return "no"
    return "unknown"


def clean_severity(value: Any) -> str:
    v = str(value).strip().lower()
    if v in VALID_INJURY_SEVERITY:
        return v
    return "unknown"


def clean_incident(value: Any, fallback: str) -> str:
    v = str(value).strip().lower()
    if v in VALID_INCIDENT_TYPES:
        return v
    return fallback if fallback in VALID_INCIDENT_TYPES else "unknown"


def clean_victims_count(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    if number < 0:
        return None
    return number


def pick_first(source: Dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in source and source.get(key) is not None:
            return source.get(key)
    return default


def normalize_labels(raw_labels: Dict[str, Any], fallback_incident: str) -> Dict[str, Any]:
    incident = clean_incident(raw_labels.get("incident_type"), fallback=fallback_incident)
    location = str(raw_labels.get("location", "unknown")).strip() or "unknown"

    injury_value = pick_first(raw_labels, ["injury_severity", "injuries_severity"], "unknown")
    labels = {
        "incident_type": incident,
        "location": location,
        "victims_count": clean_victims_count(raw_labels.get("victims_count")),
        "injury_severity": clean_severity(injury_value),
        "fire_present": clean_tristate(raw_labels.get("fire_present")),
        "trapped_persons": clean_tristate(raw_labels.get("trapped_persons")),
        "weapons_involved": clean_tristate(raw_labels.get("weapons_involved")),
        "hazmat_involved": clean_tristate(raw_labels.get("hazmat_involved")),
    }
    return labels


def normalize_example(
    item: Dict[str, Any],
    fallback_incident: str,
    *,
    synth_meta: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Normalize a single example and optionally attach SYNTH metadata.

    The *synth_meta* dict is carried through to ``to_training_row`` where it
    ends up in the ``meta`` block of the output JSONL.  This keeps the Gemini
    schema (``SyntheticExample``) untouched while enriching the pipeline.
    """
    transcription = str(item.get("transcription", "")).strip()
    if not transcription:
        return None

    raw_labels = item.get("labels")
    if not isinstance(raw_labels, dict):
        raw_labels = item.get("extraction")
    if not isinstance(raw_labels, dict):
        raw_labels = item
    if not isinstance(raw_labels, dict):
        return None

    labels = normalize_labels(raw_labels=raw_labels, fallback_incident=fallback_incident)
    for forbidden in FORBIDDEN_FIELDS:
        labels.pop(forbidden, None)

    result: Dict[str, Any] = {"transcription": transcription, "labels": labels}

    cot = str(item.get("chain_of_thought", "")).strip()
    if not cot and isinstance(item.get("synth_meta"), dict):
        cot = str(item["synth_meta"].get("chain_of_thought", "")).strip()

    meta_out = dict(synth_meta) if synth_meta is not None else dict(item.get("synth_meta", {}))
    if cot:
        meta_out["chain_of_thought"] = cot

    if meta_out:
        result["synth_meta"] = meta_out

    return result


# ---- SYNTH constraint builder -----------------------------------------------

# Linguistic profiles matching real corpus: ~50% kabyle-dom, ~35% mixed, ~15% darija
_LANG_PROFILES = [
    ("kabyle_dominant", 50),   # Kabyle grammar + max 15% French technical vocab
    ("mixed_kabyle_fr", 35),   # Bilingual, 30-50% French
    ("darija_dominant", 15),   # Arabic Algerian dominant (kayen, wesh, rani, khouya)
]
_LANG_NAMES = [p[0] for p in _LANG_PROFILES]
_LANG_WEIGHTS = [p[1] for p in _LANG_PROFILES]

# Stress weighted to match real corpus: most are calm/hurried, ~15-25% panic
_STRESS_PROFILES = [
    ("calm", 40),      # Normal greeting, structured exchange
    ("hurried", 35),   # Short greeting, fast report, urgent tone
    ("panic", 25),     # NO greeting, repeated words, cries, incomplete sentences
]
_STRESS_NAMES = [s[0] for s in _STRESS_PROFILES]
_STRESS_WEIGHTS = [s[1] for s in _STRESS_PROFILES]
_INFO_QUANTITIES = ["minimal", "normal", "verbose"]
_TIME_PERIODS = ["day", "night", "rush_hour"]
_DIALOGUE_STYLES = [
    ("dash_turns", 70),    # "- ... - ..." style
    ("labeled_turns", 20), # "Operator:/Caller:" or "S1:/S2:"
    ("mixed_turns", 10),   # mixed markers
]
_DIALOGUE_NAMES = [x[0] for x in _DIALOGUE_STYLES]
_DIALOGUE_WEIGHTS = [x[1] for x in _DIALOGUE_STYLES]


def build_synth_constraints(
    exercise_type: str,
    incident_type: str,
    rng: random.Random,
) -> Dict[str, str]:
    """Build randomized SYNTH constraints for one example.

    Returns a dict with human-readable constraint descriptions that are
    injected into the generation prompt. The guard rules are already baked
    into GENERATION_SYSTEM_PROMPT; these constraints add *variation*.
    """
    lang = rng.choices(_LANG_NAMES, weights=_LANG_WEIGHTS, k=1)[0]
    stress = rng.choices(_STRESS_NAMES, weights=_STRESS_WEIGHTS, k=1)[0]
    info_qty = rng.choice(_INFO_QUANTITIES)
    time_period = rng.choice(_TIME_PERIODS)
    dialogue_style = rng.choices(_DIALOGUE_NAMES, weights=_DIALOGUE_WEIGHTS, k=1)[0]

    # Exercise-specific stress overrides
    if exercise_type == "ex8_panic":
        stress = "panic"
    elif exercise_type == "ex7_redirect":
        stress = rng.choice(["calm", "hurried"])  # redirects are never panic
    dialogue_instruction = {
        "dash_turns": "Use '-' turn markers for each exchange.",
        "labeled_turns": "Use explicit labels: Operator:/Caller: or S1:/S2:.",
        "mixed_turns": "Mix '-' and labeled turns naturally.",
    }.get(dialogue_style, "")

    is_negative = exercise_type == "ex6_full_flow_negative"

    # Exercise-specific focus instructions
    exercise_focus = {
        "ex1_urgency_verbs": (
            "FOCUS: Use at least 2 Kabyle urgency verbs (ighli/theghli, idukh, ithyughen, "
            "it-respirer-ara, tfit la crise). "
            "Combine with hybrid expressions like 'crise n-wul', 'tension tela3'."
        ),
        "ex2_kabyle_negation": (
            "FOCUS: Include at least 2 negation forms. Béjaïa dominant: ul+VERB+ula "
            "(13/19 parlers), also use: ur+VERB+ara (western minority), "
            "khati (informal no), machi (it's not), ulach (there is none). "
            "Example: 'ul yezmir ula', 'machi enceinte', 'khati ma3lich'."
        ),
        "ex3_geographic_anchor": (
            "FOCUS: Give a precise location with commune + quartier/cite/bloc + landmark. "
            "Use real Béjaïa patterns: 'zdat la poste', 'en face l'école', 'wa7id l'jame3'. "
            "Operator asks: 'anda exact?', 'anwa l'bloc?', 'wach la commune?'. "
            "Example: 'Ighzer Ouzarif, cite 2550 logements, bloc 20, zdat l-poste'."
        ),
        "ex4_code_switching": (
            "FOCUS: Natural code-switching between Kabyle structure and French technical "
            "vocabulary. Kabyle provides grammar (verbs, particles, construct state 'n'). "
            "French provides: ambulance, accident, tension, bloc, etage, docteur. "
            "~15% of calls may be Darija-dominant (kayen, wesh, rani, khouya, kifach)."
        ),
        "ex5_open_close": (
            "FOCUS: Realistic opening and closing. Opening variants by stress level: "
            "calm='Salam alaykoum, les pompiers?', hurried='Allo l'7imaya!', "
            "panic='Allo allo allo! arwa7u!' (no greeting, repeated words, cries). "
            "Closing: 'sa7a', 'sahit', 'ya3tik sa7a', 'barak Allahu fik'."
        ),
        "ex6_full_flow_negative": (
            "FOCUS: This is NOT a real emergency. Generate a non-urgent call: "
            "information request, wrong number ('rani ghalet'), noise complaint, "
            "electricity/water problem, or silent false alarm ('Protection Civile Allo? [Silence]'). "
            "Labels: incident_type='unknown', injury_severity='unknown'."
        ),
        "ex7_redirect": (
            "FOCUS: Caller is OUTSIDE Béjaïa zone. Operator redirects to local post. "
            "Pattern: Caller says location → Operator says 'n Bgayet, at-defkegh numéro n [poste]' "
            "→ dictates phone number → Caller repeats → 'saha'. "
            "Use real posts: Oued Ghir (030 16 92 92), El Kseur (034 82 35 65), "
            "Sidi Aïch (034 86 07 80), Souk El Tenine (034 09 36 13), Kherrata (034 18 51 21)."
        ),
        "ex8_panic": (
            "FOCUS: Generate a PANIC call. The caller is extremely stressed. "
            "NO greeting — launch directly: 'Allo allo! arwa7u!', 'azlemd! tech3el!'. "
            "Use repeated/elongated words, incomplete sentences, cries (yaddi! ya rebbi!). "
            "Operator must calm: 'asber a madame!', 'Madame! s'te plaît!'. "
            "Keep ONE incident chain, but delivery is chaotic and emotional."
        ),
    }.get(exercise_type, "")

    # Darija-specific behaviour note
    lang_note = ""
    if lang == "darija_dominant":
        lang_note = (
            "This caller speaks mostly Darija (Algerian Arabic), not Kabyle. "
            "Use: kayen (there is), wesh (what), rani (I am), khouya (brother), "
            "win (where), kifach (how), bghit (I want), 3endna (we have). "
            "Mix with French technical terms as usual.\n"
        )
    # Panic-specific note
    panic_note = ""
    if stress == "panic":
        panic_note = (
            "PANIC MODE: Caller skips greeting, launches directly into crisis. "
            "Use repeated words (allo allo!, azlemd azlemd!), cries (yaddi!, ya rebbi!), "
            "incomplete sentences. Operator tries to calm them down.\n"
        )

    constraint_text = (
        f"Linguistic profile: {lang.replace('_', ' ')}\n"
        f"{lang_note}"
        f"Caller stress: {stress}\n"
        f"{panic_note}"
        f"Info quantity: {info_qty} (target {'18-35' if info_qty == 'minimal' else '30-55' if info_qty == 'normal' else '45-80'} words)\n"
        f"Time of call: {time_period}\n"
        f"Dialogue style: {dialogue_style}\n"
        f"Dialogue instruction: {dialogue_instruction}\n"
    )
    if exercise_focus:
        constraint_text += f"\n{exercise_focus}\n"
    if is_negative:
        constraint_text += "This call is NOT an emergency.\n"

    return {
        "lang_profile": lang,
        "stress_level": stress,
        "info_quantity": info_qty,
        "time_period": time_period,
        "exercise_type": exercise_type,
        "is_negative": is_negative,
        "dialogue_style": dialogue_style,
        "constraint_text": constraint_text,
    }


def build_generation_prompt(
    task: Dict[str, Any],
    constraints: Optional[Dict[str, str]] = None,
    *,
    real_style_profile: Optional[Dict[str, Any]] = None,
    fewshot_examples: Optional[List[Dict[str, str]]] = None,
) -> str:
    """Build the full generation prompt, optionally enriched with SYNTH constraints."""
    base_prompt = str(task.get("prompt_template", "")).strip()
    incident = str(task.get("incident_type", "unknown")).strip().lower() or "unknown"
    requested = int(task.get("requested_examples", 1))

    # Constraint block (injected between system prompt and task specifics)
    constraint_block = ""
    if constraints:
        constraint_block = (
            "\n--- CONSTRAINTS FOR THIS BATCH ---\n"
            f"{constraints.get('constraint_text', '')}\n"
            "--- END CONSTRAINTS ---\n\n"
        )

    real_dna_block = build_real_dna_block(real_style_profile or {})
    fewshot_block = build_real_fewshot_block(fewshot_examples or [])
    glossary_block = _build_scenario_glossary(incident)

    if base_prompt:
        return (
            f"{GENERATION_SYSTEM_PROMPT}\n{real_dna_block}\n{fewshot_block}\n"
            f"{glossary_block}\n{constraint_block}"
            f"{base_prompt}\n\n"
            f"Reminder: return exactly {requested} examples for incident_type={incident}.\n"
            "Each example must be coherent and realistic: no random token stuffing, no broken fragments."
        )

    context = task.get("knowledge_context", {})
    communes = ", ".join((context.get("priority_communes") or [])[:12])
    routes = ", ".join((context.get("routes") or [])[:10])
    plages = ", ".join((context.get("plages") or [])[:10])
    return (
        f"{GENERATION_SYSTEM_PROMPT}\n{real_dna_block}\n{fewshot_block}\n"
        f"{glossary_block}\n{constraint_block}"
        f"Generate {requested} emergency call examples for incident_type={incident}.\n"
        f"Use only Bejaia context:\n- communes: {communes}\n- routes: {routes}\n- beaches: {plages}\n"
        "Each example must be coherent and realistic: no random token stuffing, no broken fragments.\n"
    )


def _extract_lexical_anchors(task: Dict[str, Any]) -> List[str]:
    prompt = str(task.get("prompt_template", ""))
    match = re.search(r"Lexical anchors to vary:\s*(.+?)\.", prompt, flags=re.IGNORECASE)
    if not match:
        return []
    return [x.strip() for x in match.group(1).split(",") if x.strip()]


def _incident_defaults(incident: str) -> Dict[str, Any]:
    fire_types = {"fire_building", "fire_forest", "fire_vehicle"}
    defaults: Dict[str, Any] = {
        "victims": [None, 1, 2],
        "injury": ["unknown", "minor", "severe"],
        "fire_present": "yes" if incident in fire_types else "no",
        "trapped": ["unknown", "no"],
        "weapons": ["unknown", "no"],
        "hazmat": ["unknown", "no"],
    }
    if incident == "hazmat":
        defaults["hazmat"] = ["yes", "unknown"]
    if incident == "assault_violence":
        defaults["weapons"] = ["yes", "no", "unknown"]
        defaults["injury"] = ["minor", "severe", "unknown"]
    if incident == "drowning":
        defaults["injury"] = ["severe", "fatal", "unknown"]
        defaults["victims"] = [1, 1, 2, None]
    if incident == "medical_emergency":
        defaults["injury"] = ["unknown", "severe", "minor"]
    if incident == "unknown":
        defaults["fire_present"] = "unknown"
        defaults["trapped"] = ["unknown"]
        defaults["weapons"] = ["unknown"]
        defaults["hazmat"] = ["unknown"]
    return defaults


def generate_local_examples(task: Dict[str, Any], seed: int) -> List[Dict[str, Any]]:
    incident = str(task.get("incident_type", "unknown")).strip().lower() or "unknown"
    n = int(task.get("requested_examples", 1))
    context = task.get("knowledge_context", {})
    communes = list(context.get("priority_communes") or []) or ["Bejaia"]
    routes = list(context.get("routes") or [])
    plages = list(context.get("plages") or [])
    anchors = _extract_lexical_anchors(task)
    defaults = _incident_defaults(incident)

    seed_key = f"{seed}:{task.get('task_id', 'task')}"
    rnd = random.Random(seed_key)
    style_templates = [
        "Allo himaya, yella {kw} deg {loc}, arwah-d s zerb.",
        "Salam, kayen {kw} fi {loc}, ma3lich 3edjled.",
        "A lhimaya, sra {kw} g {loc}, rahoum yesta3fou.",
        "Pompiers? yella {kw} hna {loc}, ne7taj l'aide daba.",
        "Urgence, {kw} deg {loc}, ta3jil svp.",
    ]

    def pick_location() -> str:
        if incident == "drowning" and plages:
            return rnd.choice(plages)
        if incident in {"accident_vehicular", "accident_pedestrian", "fire_vehicle"} and routes:
            return f"{rnd.choice(communes)} / {rnd.choice(routes)}"
        return rnd.choice(communes)

    examples: List[Dict[str, Any]] = []
    for _ in range(max(0, n)):
        kw = rnd.choice(anchors) if anchors else incident.replace("_", " ")
        loc = pick_location()
        transcription = rnd.choice(style_templates).format(kw=kw, loc=loc)
        labels = {
            "location": loc,
            "incident_type": incident,
            "victims_count": rnd.choice(defaults["victims"]),
            "injury_severity": rnd.choice(defaults["injury"]),
            "fire_present": defaults["fire_present"],
            "trapped_persons": rnd.choice(defaults["trapped"]),
            "weapons_involved": rnd.choice(defaults["weapons"]),
            "hazmat_involved": rnd.choice(defaults["hazmat"]),
        }
        examples.append({"transcription": transcription, "chain_of_thought": "Local fallback.", "labels": labels})
    return examples


def generate_task_calls(
    model: Any,
    task: Dict[str, Any],
    retries: int = 2,
    constraints: Optional[Dict[str, str]] = None,
    *,
    real_style_profile: Optional[Dict[str, Any]] = None,
    fewshot_examples: Optional[List[Dict[str, str]]] = None,
) -> List[Dict[str, Any]]:
    prompt = build_generation_prompt(
        task,
        constraints=constraints,
        real_style_profile=real_style_profile,
        fewshot_examples=fewshot_examples,
    )
    generation_cfg = {
        "temperature": 0.8,
        "response_mime_type": "application/json",
        "response_schema": GenerationResponse,
    }
    fallback_incident = str(task.get("incident_type", "unknown")).strip().lower() or "unknown"

    for attempt in range(retries + 1):
        try:
            response = model.generate_content(prompt, generation_config=generation_cfg)
            parsed_items = parse_generation_response(response)
            normalized = [
                ex
                for ex in (normalize_example(item, fallback_incident=fallback_incident) for item in parsed_items)
                if ex is not None
            ]
            if normalized:
                return normalized
        except Exception as exc:
            print(f"[{task.get('task_id', 'task')}] generation error: {exc}")
            if attempt == retries:
                return []
            time.sleep(1.5)
    return []


def to_training_row(
    example: Dict[str, Any],
    task_id: str,
    row_index: int,
    generator_name: str,
    guard_result: Optional[GuardResult] = None,
    guard_rules_version: str = "",
) -> Dict[str, Any]:
    labels = example["labels"]
    location = str(labels.get("location", "unknown")).strip() or "unknown"
    commune_guess = location.split("/")[0].strip() if "/" in location else location

    meta: Dict[str, Any] = {
        "commune": commune_guess or "Inconnu",
        "daira": "Inconnu",
        "intent": "report_incident",
        "urgency_human": "unknown",
        "source": "synthetic",
        "task_id": task_id,
        "generator": generator_name,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    if guard_result is not None:
        meta.update(
            {
                "guard_rules_version": guard_rules_version,
                "guard_action": guard_result.action,
                "guard_score": guard_result.score,
                "guard_blocking_violations": guard_result.blocking_violations,
                "guard_quality_violations": guard_result.quality_violations,
            }
        )

    # ---- SYNTH provenance & exercise metadata ----------------------------
    synth = example.get("synth_meta")
    if isinstance(synth, dict):
        meta["exercise_type"] = synth.get("exercise_type", "")
        meta["seed_id"] = synth.get("seed_id", "")
        meta["is_negative"] = synth.get("is_negative", False)
        meta["source_type"] = synth.get("source_type", "synthetic")
        cot = synth.get("chain_of_thought", "")
        if cot:
            meta["chain_of_thought"] = cot
        ca = synth.get("constraints_applied")
        if isinstance(ca, dict):
            meta["constraints_applied"] = ca

    return {
        "id": f"SYN_{task_id}__{row_index:05d}",
        "call_group": f"SYN_{task_id}",
        "audio_file": "",
        "transcription": example["transcription"],
        "labels": labels,
        "meta": meta,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plan_path",
        default=str(ROOT / "ml_pipeline" / "dataset" / "synthetic_generation" / "generation_tasks.jsonl"),
    )
    parser.add_argument(
        "--output_jsonl",
        default=str(ROOT / "ml_pipeline" / "dataset" / "annotations_synthetic.jsonl"),
    )
    parser.add_argument("--limit", type=int, default=0, help="Number of tasks to process. 0 means all tasks.")
    parser.add_argument("--model", default="models/gemini-2.5-flash")
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--local_fallback", action="store_true")
    parser.add_argument(
        "--force_local_fallback",
        action="store_true",
        help="Explicitly allow low-quality offline fallback generation.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--allow_empty_overwrite",
        action="store_true",
        help="Allow overwriting output file when generation produced zero rows.",
    )
    parser.add_argument(
        "--guard_rules_path",
        default=str(ROOT / "augmentation" / "kabyle_guard_rules.yaml"),
        help="Path to machine-readable Kabyle guard rules (YAML).",
    )
    parser.add_argument(
        "--guard_calibration_report",
        default=str(ROOT / "ml_pipeline" / "dataset" / "synthetic_generation" / "guard_calibration_report.json"),
        help="Path to guard calibration report JSON.",
    )
    parser.add_argument(
        "--guard_run_id",
        default="",
        help="Optional run id for calibration report. Auto-generated when empty.",
    )
    parser.add_argument(
        "--disable_kabyle_guard",
        action="store_true",
        help="Disable linguistic guard evaluation (not recommended).",
    )
    parser.add_argument(
        "--real_corpus_csv",
        default=str(ROOT / "dataset" / "annotations_local.csv"),
        help="CSV of real calls used to extract style DNA and few-shot examples.",
    )
    parser.add_argument(
        "--real_profile_json",
        default=str(ROOT / "dataset" / "annotations_real_profile.json"),
        help="Optional real-corpus profile JSON produced by merge_real_annotations.py.",
    )
    parser.add_argument(
        "--fewshot_count",
        type=int,
        default=2,
        help="Number of anonymized real-call few-shot examples injected per task.",
    )
    parser.add_argument(
        "--disable_real_dna",
        action="store_true",
        help="Disable real-corpus DNA guidance and few-shot injection.",
    )
    args = parser.parse_args()

    tasks = load_tasks(Path(args.plan_path))
    if args.limit and args.limit > 0:
        tasks = tasks[: args.limit]
    print(f"Loaded {len(tasks)} tasks.")

    if args.dry_run:
        for task in tasks:
            print(f"- {task.get('task_id')} | incident={task.get('incident_type')} | n={task.get('requested_examples')}")
        print("Dry run complete.")
        return

    if args.local_fallback and not args.force_local_fallback:
        print(
            "Refusing local fallback by default. "
            "Use Gemini API, or pass --force_local_fallback if you intentionally accept low-quality synthetic data."
        )
        return

    guard_rules = None
    if not args.disable_kabyle_guard:
        try:
            guard_rules = load_guard_rules(Path(args.guard_rules_path))
            print(f"Loaded guard rules: {args.guard_rules_path} (version={guard_rules.version})")
        except Exception as exc:
            print(f"Error: failed to load guard rules from {args.guard_rules_path}: {exc}")
            return

    model = None
    generator_name = "local_fallback"
    if not args.local_fallback:
        try:
            from dotenv import load_dotenv
            import google.generativeai as genai
        except Exception as exc:  # pragma: no cover
            print(f"Error: missing Gemini dependencies ({exc}). Use --local_fallback.")
            return

        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY not found. Use --local_fallback for offline generation.")
            return
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(args.model)
        generator_name = f"gemini:{args.model}"

    real_calls: List[Dict[str, str]] = []
    real_style_profile: Dict[str, Any] = {}
    if not args.disable_real_dna:
        real_calls = load_real_calls(Path(args.real_corpus_csv))
        real_style_profile = load_real_style_profile(Path(args.real_profile_json))
        print(
            f"Loaded real DNA corpus: {len(real_calls)} rows "
            f"(csv={args.real_corpus_csv}, profile={'yes' if real_style_profile else 'no'})."
        )

    all_rows: List[Dict[str, Any]] = []
    guard_results: List[GuardResult] = []
    global_index = 1
    rejected_by_guard = 0
    borderline_by_guard = 0
    task_rng = random.Random(args.seed)

    for index, task in enumerate(tasks, start=1):
        task_id = str(task.get("task_id", f"task_{index:03d}"))
        incident_type = str(task.get("incident_type", "unknown")).strip().lower() or "unknown"
        print(f"Processing Task {index}/{len(tasks)}: {task_id}")

        # Build SYNTH constraints for this task
        exercise = pick_exercise_type(task_rng)
        constraints = build_synth_constraints(
            exercise_type=exercise,
            incident_type=incident_type,
            rng=task_rng,
        )
        synth_meta = {
            "exercise_type": constraints["exercise_type"],
            "is_negative": constraints["is_negative"],
            "seed_id": task_id,
            "source_type": "synthetic",
            "constraints_applied": {
                "lang_profile": constraints["lang_profile"],
                "stress_level": constraints["stress_level"],
                "info_quantity": constraints["info_quantity"],
                "time_period": constraints["time_period"],
                "dialogue_style": constraints["dialogue_style"],
                "real_dna_enabled": not args.disable_real_dna,
                "fewshot_count": 0,
            },
        }

        if args.local_fallback:
            examples = generate_local_examples(task=task, seed=args.seed)
        else:
            fewshots = select_real_fewshots(
                real_calls=real_calls,
                incident_type=incident_type,
                rng=task_rng,
                count=args.fewshot_count,
            ) if not args.disable_real_dna else []
            synth_meta["constraints_applied"]["fewshot_count"] = len(fewshots)
            examples = generate_task_calls(
                model=model,
                task=task,
                constraints=constraints,
                real_style_profile=real_style_profile,
                fewshot_examples=fewshots,
            )

        valid = 0
        fallback_incident = incident_type
        for ex in examples:
            normalized = normalize_example(
                ex,
                fallback_incident=fallback_incident,
                synth_meta=synth_meta,
            )
            if normalized is None:
                continue

            guard_result: Optional[GuardResult] = None
            if guard_rules is not None:
                guard_result = evaluate_kabyle_guard(
                    transcription=normalized["transcription"],
                    labels=normalized["labels"],
                    rules=guard_rules,
                )
                guard_results.append(guard_result)
                if guard_result.action == "reject":
                    rejected_by_guard += 1
                    continue
                if guard_result.action == "borderline":
                    borderline_by_guard += 1
                normalized["transcription"] = guard_result.normalized_transcription

            row = to_training_row(
                example=normalized,
                task_id=task_id,
                row_index=global_index,
                generator_name=generator_name,
                guard_result=guard_result,
                guard_rules_version=guard_rules.version if guard_rules is not None else "",
            )
            all_rows.append(row)
            global_index += 1
            valid += 1

        print(f"  -> Generated {valid} valid examples (exercise={exercise}, lang={constraints['lang_profile']}).")
        if not args.local_fallback:
            time.sleep(0.5)

    output_path = Path(args.output_jsonl)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not all_rows and output_path.exists() and not args.allow_empty_overwrite:
        print(
            "\nNo rows generated. Existing output preserved. "
            "Use --allow_empty_overwrite if you want to overwrite with an empty file."
        )
    else:
        with output_path.open("w", encoding="utf-8") as handle:
            for row in all_rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    incident_counter = Counter(row["labels"]["incident_type"] for row in all_rows)
    print("\n=== SYNTHETIC GENERATION SUMMARY ===")
    print(f"rows_written: {len(all_rows)}")
    print(f"output_path: {output_path}")
    print(f"incident_distribution: {dict(sorted(incident_counter.items()))}")
    if guard_rules is not None:
        run_id = args.guard_run_id or datetime.now(timezone.utc).strftime("guard_%Y%m%dT%H%M%SZ")
        report = update_guard_calibration_report(
            report_path=Path(args.guard_calibration_report),
            rules=guard_rules,
            run_summary=summarize_guard_results(guard_results, run_id=run_id),
        )
        print(f"guard_checked: {len(guard_results)}")
        print(f"guard_rejected: {rejected_by_guard}")
        print(f"guard_borderline: {borderline_by_guard}")
        print(
            "guard_thresholds: "
            f"pass={report.thresholds_used.pass_score} "
            f"borderline={report.thresholds_used.borderline_score}"
        )
        print(f"guard_calibration_report: {args.guard_calibration_report}")


if __name__ == "__main__":
    main()
