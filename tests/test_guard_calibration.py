from pathlib import Path

from augmentation.kabyle_guard import (
    GuardResult,
    load_guard_rules,
    summarize_guard_results,
    update_guard_calibration_report,
)


ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "augmentation" / "kabyle_guard_rules.yaml"


def _mk_result(score: float, action: str) -> GuardResult:
    return GuardResult(
        normalized_transcription="allo dayi tura chwiya ghli deg bejaia d'accord saha",
        score=score,
        action=action,  # type: ignore[arg-type]
        blocking_violations=[],
        quality_violations=[],
        penalties={},
        metrics={},
    )


def test_calibration_stability_over_two_runs(tmp_path: Path) -> None:
    rules = load_guard_rules(RULES_PATH)
    report_path = tmp_path / "guard_calibration_report.json"

    run1 = summarize_guard_results(
        [
            _mk_result(0.91, "pass"),
            _mk_result(0.88, "pass"),
            _mk_result(0.70, "borderline"),
            _mk_result(0.62, "reject"),
        ],
        run_id="run_001",
    )
    update_guard_calibration_report(report_path, rules, run1)

    run2 = summarize_guard_results(
        [
            _mk_result(0.90, "pass"),
            _mk_result(0.86, "pass"),
            _mk_result(0.71, "borderline"),
            _mk_result(0.63, "reject"),
        ],
        run_id="run_002",
    )
    report = update_guard_calibration_report(report_path, rules, run2)

    assert len(report.runs) == 2
    assert report.stability.two_run_stable is True
    assert report.stability.pass_rate_delta is not None
    assert report.stability.mean_score_delta is not None

