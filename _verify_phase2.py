"""Phase 2 verification: test constraint generation, prompt building, and E2E output."""
import json, pathlib, sys
sys.path.insert(0, ".")

from augmentation.generate_synthetic import (
    build_synth_constraints,
    build_generation_prompt,
    pick_exercise_type,
    SYNTH_EXERCISE_TYPES,
    _LANG_PROFILES,
)
import random

rng = random.Random(42)

# ── Test 1: build_synth_constraints returns well-formed dict ──
print("=== Test 1: build_synth_constraints ===")
for ex_type in SYNTH_EXERCISE_TYPES:
    c = build_synth_constraints(ex_type, "fire_building", rng)
    assert "constraint_text" in c, f"Missing constraint_text for {ex_type}"
    assert "lang_profile" in c
    assert "exercise_type" in c and c["exercise_type"] == ex_type
    is_neg = (ex_type == "ex6_full_flow_negative")
    assert c["is_negative"] == is_neg, f"is_negative mismatch for {ex_type}"
    print(f"  {ex_type:30s} lang={c['lang_profile']:20s} stress={c['stress_level']:8s} neg={c['is_negative']}")
print("  PASS\n")

# ── Test 2: build_generation_prompt with constraints is longer ──
print("=== Test 2: Prompt enrichment ===")
task = {
    "task_id": "test_001",
    "incident_type": "fire_building",
    "requested_examples": 5,
    "prompt_template": "Generate 5 fire calls.",
}
prompt_plain = build_generation_prompt(task, constraints=None)
c = build_synth_constraints("ex2_kabyle_negation", "fire_building", rng)
prompt_rich = build_generation_prompt(task, constraints=c)

len_plain = len(prompt_plain)
len_rich = len(prompt_rich)
delta_pct = ((len_rich - len_plain) / len_plain) * 100
print(f"  Plain prompt: {len_plain} chars")
print(f"  Rich prompt:  {len_rich} chars (+{delta_pct:.0f}%)")
assert len_rich > len_plain, "Rich prompt must be longer"
assert "CONSTRAINTS FOR THIS BATCH" in prompt_rich
assert "Negation" in prompt_rich or "negation" in prompt_rich
print("  PASS\n")

# ── Test 3: Constraint text contains exercise focus ──
print("=== Test 3: Exercise focus in constraint text ===")
for ex_type, expected_kw in [
    ("ex1_urgency_verbs", "urgency verb"),
    ("ex2_kabyle_negation", "negation"),
    ("ex3_geographic_anchor", "location"),
    ("ex4_code_switching", "code-switching"),
    ("ex5_open_close", "opening"),
    ("ex6_full_flow_negative", "NOT a real emergency"),
]:
    c = build_synth_constraints(ex_type, "fire_building", rng)
    found = expected_kw.lower() in c["constraint_text"].lower()
    status = "PASS" if found else "FAIL"
    print(f"  {ex_type:30s} has '{expected_kw}': {status}")
    assert found, f"Exercise focus missing for {ex_type}"
print("  PASS\n")

# ── Test 4: System prompt has corpus-validated patterns from annotation v2 ──
print("=== Test 4: System prompt corpus patterns ===")
from augmentation.generate_synthetic import GENERATION_SYSTEM_PROMPT
checks = [
    ("sbitar", "Medical hybrid term"),
    ("crise n'wul", "Cardiac crisis term"),
    ("ul", "Bejaia negation variant"),
    ("l'ambulance", "l'-article pattern"),
    ("it-respirerara", "Hybrid FR+KAB verb"),
    ("59%", "Corpus greeting frequency"),
    ("dayi(25)", "Particle corpus frequency"),
    ("65%", "Dialogue format distribution"),
    ("7imaya", "Emergency center term"),
]
for term, desc in checks:
    found = term in GENERATION_SYSTEM_PROMPT
    status = "PASS" if found else "FAIL"
    print(f"  [{status}] {desc}: '{term}'")
    assert found, f"Missing: {term} ({desc})"
print("  PASS\n")

# ── Test 5: Language profile distribution ──
print("=== Test 5: Language profile weights ===")
for name, weight in _LANG_PROFILES:
    print(f"  {name}: {weight}%")
assert sum(w for _, w in _LANG_PROFILES) == 100, "Weights must sum to 100"
print("  PASS\n")

print("=" * 60)
print(" ALL 5 PHASE 2 TESTS PASSED")
print("=" * 60)
