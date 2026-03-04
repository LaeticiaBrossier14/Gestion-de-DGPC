from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from augmentation.kabyle_guard import KabyleGuardRules, load_guard_rules


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "augmentation" / "kabyle_guard_rules.yaml"


def test_load_guard_rules_yaml_strict() -> None:
    rules = load_guard_rules(RULES_PATH)
    assert rules.thresholds.min_chars == 30
    assert rules.thresholds.min_words == 8
    assert abs(rules.thresholds.pass_score - 0.80) < 1e-9
    assert "R1" in rules.blocking_rules
    assert "Q1" in rules.quality_rules


def test_guard_rules_reject_unknown_fields() -> None:
    payload = yaml.safe_load(RULES_PATH.read_text(encoding="utf-8"))
    payload["unexpected_key"] = "boom"
    with pytest.raises(ValidationError):
        KabyleGuardRules.model_validate(payload)

