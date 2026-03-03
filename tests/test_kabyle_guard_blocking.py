from pathlib import Path

from augmentation.kabyle_guard import evaluate_kabyle_guard, load_guard_rules


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "augmentation" / "kabyle_guard_rules.yaml"


def _labels() -> dict:
    return {
        "incident_type": "medical_emergency",
        "location": "Bejaia",
        "victims_count": 1,
        "injury_severity": "severe",
        "fire_present": "no",
        "trapped_persons": "no",
        "weapons_involved": "no",
        "hazmat_involved": "no",
    }


def test_r1_blocking_min_length() -> None:
    rules = load_guard_rules(RULES_PATH)
    result = evaluate_kabyle_guard("allo", _labels(), rules)
    assert result.action == "reject"
    assert "R1" in result.blocking_violations


def test_r2_blocking_missing_greeting() -> None:
    rules = load_guard_rules(RULES_PATH)
    text = "bonjour dayi tura chwiya ghli deg bejaia d'accord saha"
    result = evaluate_kabyle_guard(text, _labels(), rules)
    assert result.action == "reject"
    assert "R2" in result.blocking_violations


def test_r3_blocking_missing_kabyle_markers() -> None:
    rules = load_guard_rules(RULES_PATH)
    text = "allo ghli ambulance urgence bejaia d'accord merci"
    result = evaluate_kabyle_guard(text, _labels(), rules)
    assert result.action == "reject"
    assert "R3" in result.blocking_violations


def test_r4_blocking_forbidden_unicode() -> None:
    rules = load_guard_rules(RULES_PATH)
    text = "allo dayi tura chwiya ghli ɛ bejaia d'accord saha"
    result = evaluate_kabyle_guard(text, _labels(), rules)
    assert result.action == "reject"
    assert "R4" in result.blocking_violations


def test_r5_blocking_no_kabyle_verb() -> None:
    rules = load_guard_rules(RULES_PATH)
    text = "allo dayi tura chwiya ambulance urgence bejaia d'accord saha"
    result = evaluate_kabyle_guard(text, _labels(), rules)
    assert result.action == "reject"
    assert "R5" in result.blocking_violations


def test_r6_blocking_bad_negation() -> None:
    rules = load_guard_rules(RULES_PATH)
    text = "allo dayi tura chwiya ur yella mochkila ghli deg bejaia d'accord"
    result = evaluate_kabyle_guard(text, _labels(), rules)
    assert result.action == "reject"
    assert "R6" in result.blocking_violations

