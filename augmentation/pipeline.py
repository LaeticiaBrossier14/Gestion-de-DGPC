"""
Rule-Guided Kabyle Generation Pipeline — CLI Entry Point.

3-Stage Architecture:
  1. SCENARIO GEN  → Gemini generates rich French scenarios (structured output)
  2. ASSEMBLY      → Python assembles Kabyle from templates + grammar rules
  3. VALIDATION    → Deterministic checks ensure quality

Usage:
  # Generate 50 scenarios across all missing types
  python -m augmentation.pipeline --count 50

  # Generate for a specific incident type
  python -m augmentation.pipeline --type drowning --count 10

  # Dry run (no LLM calls, use local fallback)
  python -m augmentation.pipeline --dry-run --count 5

  # Output to custom file
  python -m augmentation.pipeline --output dataset/synthetic_v2.csv --count 100
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from augmentation.engine.kabyle_assembler import (
    KabyleAssembler,
    ScenarioInput,
    load_geography,
    sample_location,
)
from augmentation.engine.scenario_gen import (
    ScenarioGenerator,
    generate_geography_context,
)
from augmentation.engine.validator import QualityValidator, ValidationResult


# ── Constants ───────────────────────────────────────────────

# Incident types we need to generate (underrepresented in real data)
MISSING_TYPES = {
    "drowning": 15,
    "assault_violence": 15,
    "hazmat": 8,
    "lost_person": 8,
    "structural_collapse": 10,
    "fire_forest": 10,
    "fire_building": 10,
}

# Types that need augmentation (exist but underrepresented)
AUGMENT_TYPES = {
    "medical_emergency": 10,
    "accident_vehicular": 8,
    "fire_vehicle": 8,
    "accident_pedestrian": 8,
}

ALL_TYPES_WITH_COUNTS = {**MISSING_TYPES, **AUGMENT_TYPES}

DEFAULT_OUTPUT = PROJECT_ROOT / "dataset" / "synthetic_v2.csv"

CSV_COLUMNS = [
    "ID", "File", "Transcription",
    "incident_type", "injury_severity", "victims_count",
    "fire_present", "trapped_persons", "weapons_involved",
    "hazmat_involved", "intent", "urgency_human",
    "daira", "commune", "lieu", "location_description",
    "summary", "notes_cot",
]


# ── Scenario → ScenarioInput Conversion ────────────────────

def scenario_to_input(scenario: Dict[str, Any]) -> ScenarioInput:
    """Convert a Gemini scenario dict to a ScenarioInput for the assembler."""
    loc = scenario.get("location", {})
    caller = scenario.get("caller", {})
    victim = scenario.get("victim", {})
    details = scenario.get("details", {})

    # Map victim gender
    gender_map = {"homme": "masc", "femme": "fem", "mixte": "masc"}
    v_gender = gender_map.get(victim.get("genre", ""), "masc")

    # Map victim age
    age_map = {"enfant": "child", "adulte": "adult", "agé": "aged", "âgé": "aged"}
    v_age = age_map.get(victim.get("age_approx", ""), "adult")

    # Map victim state
    state_map = {
        "conscient": "conscious",
        "inconscient": "unconscious",
        "blessé": "bleeding",
        "critique": "severe",
        "décédé": "severe",
    }
    v_state = state_map.get(victim.get("etat", ""), "conscious")

    # Map caller emotion
    emo_map = {
        "paniqué": "paniqué",
        "calme": "calm",
        "en_colère": "urgent",
        "confus": "calm",
        "pleurs": "paniqué",
    }
    c_emotion = emo_map.get(caller.get("etat_emotionnel", ""), "calm")

    return ScenarioInput(
        incident_type=scenario.get("incident_type", "unknown"),
        urgency=scenario.get("urgency", "high"),
        daira=loc.get("daira", ""),
        commune=loc.get("commune", ""),
        lieu=loc.get("lieu_dit", ""),
        repere=loc.get("repere", ""),
        victim_gender=v_gender,
        victim_age=v_age,
        victim_count=victim.get("nombre", 1),
        victim_state=v_state,
        medical_detail=victim.get("details_medicaux", ""),
        fire_source=details.get("fire_source", ""),
        vehicle_type=details.get("vehicle_type", ""),
        accident_detail="",
        water_body=details.get("water_body", ""),
        caller_emotion=c_emotion,
        caller_relation=caller.get("relation_victime", "témoin"),
        dialogue_turns=scenario.get("dialogue", []),
    )


# ── Row Formatting ──────────────────────────────────────────

def to_csv_row(
    transcription: str,
    scenario: Dict[str, Any],
    idx: int,
    validation: ValidationResult,
) -> Dict[str, str]:
    """Format a generated transcription as a CSV row matching existing schema."""
    loc = scenario.get("location", {})
    victim = scenario.get("victim", {})
    details = scenario.get("details", {})
    incident_type = scenario.get("incident_type", "unknown")

    # Determine label fields
    fire_present = "yes" if incident_type.startswith("fire_") else "no"
    weapons = "yes" if incident_type == "assault_violence" else "unknown"
    hazmat = "yes" if incident_type == "hazmat" else "unknown"
    trapped = "unknown"
    if incident_type in ("structural_collapse", "fire_building"):
        trapped = random.choice(["yes", "unknown"])

    # Injury severity
    state = victim.get("etat", "")
    if state in ("critique", "décédé"):
        injury = "severe"
    elif state == "blessé":
        injury = random.choice(["minor", "severe"])
    else:
        injury = "unknown"

    return {
        "ID": f"SYN_RG_{idx:05d}",
        "File": f"synthetic_rg_{idx:05d}",
        "Transcription": transcription,
        "incident_type": incident_type,
        "injury_severity": injury,
        "victims_count": str(victim.get("nombre", 1)),
        "fire_present": fire_present,
        "trapped_persons": trapped,
        "weapons_involved": weapons,
        "hazmat_involved": hazmat,
        "intent": "report_incident",
        "urgency_human": scenario.get("urgency", "unknown"),
        "daira": loc.get("daira", "Inconnu"),
        "commune": loc.get("commune", "Inconnu"),
        "lieu": loc.get("lieu_dit", "Inconnu"),
        "location_description": f"{loc.get('lieu_dit', '')} — {loc.get('repere', '')}",
        "summary": details.get("description_fr", ""),
        "notes_cot": f"rule_guided_gen | score={validation.score:.2f} | "
                     f"warnings={len(validation.warnings)}",
    }


# ── Pipeline ────────────────────────────────────────────────

def run_pipeline(
    types_with_counts: Dict[str, int],
    *,
    output_path: Path,
    dry_run: bool = False,
    batch_size: int = 5,
    seed: int = 42,
) -> None:
    """Run the full 3-stage pipeline.

    Args:
        types_with_counts: {incident_type: count} pairs
        output_path: CSV output file
        dry_run: Skip LLM calls, use local fallback
        batch_size: Scenarios per LLM call
        seed: Random seed for reproducibility
    """
    random.seed(seed)

    # Initialize components
    geo = load_geography()
    geo_context = generate_geography_context(geo)
    assembler = KabyleAssembler()
    validator = QualityValidator()

    if not dry_run:
        generator = ScenarioGenerator()
    else:
        generator = ScenarioGenerator(api_key="dry-run")

    total_requested = sum(types_with_counts.values())
    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║  Rule-Guided Kabyle Generation Pipeline          ║")
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  Total scenarios: {total_requested:<31}║")
    print(f"║  Dry run: {str(dry_run):<39}║")
    print(f"║  Output: {str(output_path.name):<40}║")
    print(f"╚══════════════════════════════════════════════════╝")
    print()

    all_rows: List[Dict[str, str]] = []
    global_idx = 0
    total_accepted = 0
    total_rejected = 0

    for incident_type, count in types_with_counts.items():
        print(f"─── {incident_type} ({count} scenarios) ───")
        t0 = time.time()

        # ── Stage 1: Generate French scenarios ──
        remaining = count
        scenarios: List[Dict[str, Any]] = []
        while remaining > 0:
            batch = min(batch_size, remaining)
            if dry_run:
                batch_scenarios = generator._local_fallback(incident_type, batch)
            else:
                batch_scenarios = generator.generate_scenarios(
                    incident_type=incident_type,
                    count=batch,
                    geography_context=geo_context,
                )
            scenarios.extend(batch_scenarios)
            remaining -= len(batch_scenarios)
            if not batch_scenarios:
                print(f"  ⚠ Empty batch — stopping early for {incident_type}")
                break

        print(f"  Stage 1: {len(scenarios)} French scenarios generated")

        # ── Stage 2: Assemble Kabyle transcriptions ──
        transcriptions: List[str] = []
        for s in scenarios:
            try:
                inp = scenario_to_input(s)
                kabyle_text = assembler.assemble(inp)
                transcriptions.append(kabyle_text)
            except Exception as e:
                print(f"  ⚠ Assembly error: {e}")
                transcriptions.append("")

        print(f"  Stage 2: {len(transcriptions)} Kabyle transcriptions assembled")

        # ── Stage 3: Validate ──
        accepted = 0
        rejected = 0
        for i, (text, s) in enumerate(zip(transcriptions, scenarios)):
            if not text:
                rejected += 1
                continue

            result = validator.validate(text, incident_type)
            if result.passed:
                row = to_csv_row(text, s, global_idx, result)
                all_rows.append(row)
                accepted += 1
                global_idx += 1
            else:
                rejected += 1
                if rejected <= 3:  # Only show first 3 rejections per type
                    print(f"    ✗ Rejected: {result.violations}")

        dt = time.time() - t0
        total_accepted += accepted
        total_rejected += rejected
        print(f"  Stage 3: {accepted}✓ accepted, {rejected}✗ rejected ({dt:.1f}s)")
        print()

    # ── Write output ──
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"═══════════════════════════════════════════════════")
    print(f"  ✅ Pipeline complete!")
    print(f"  Total: {total_accepted} accepted, {total_rejected} rejected")
    print(f"  Output: {output_path}")
    print(f"═══════════════════════════════════════════════════")


# ── CLI ─────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rule-Guided Kabyle Emergency Call Generation Pipeline"
    )
    parser.add_argument(
        "--type", "-t",
        type=str,
        default="",
        help="Specific incident type to generate (default: all missing types)",
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=0,
        help="Number of scenarios per type (overrides defaults)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help=f"Output CSV path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip LLM calls, use local fallback scenarios",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Scenarios per LLM API call (default: 5)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.type:
        # Single type
        count = args.count or 10
        types_with_counts = {args.type: count}
    elif args.count > 0:
        # All types with same count
        types_with_counts = {k: args.count for k in ALL_TYPES_WITH_COUNTS}
    else:
        # Default distribution
        types_with_counts = dict(ALL_TYPES_WITH_COUNTS)

    run_pipeline(
        types_with_counts,
        output_path=Path(args.output),
        dry_run=args.dry_run,
        batch_size=args.batch_size,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
