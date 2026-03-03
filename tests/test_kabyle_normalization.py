from pathlib import Path

from augmentation.kabyle_guard import load_guard_rules, normalize_text


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "augmentation" / "kabyle_guard_rules.yaml"


def test_normalization_tolerates_unicode_and_normalizes_to_arabizi() -> None:
    rules = load_guard_rules(RULES_PATH)
    raw = "  Xati, ɣli ḥna ʃwiya  "
    normalized = normalize_text(raw, rules.normalization)
    assert normalized == "khati, ghli 7na chwiya"

