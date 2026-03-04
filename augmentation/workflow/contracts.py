"""Core contracts for synthetic workflow v2."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence

from ml_pipeline.dataset.enums import IncidentType, InjurySeverity, TriState

FACT_FIELDS: tuple[str, ...] = (
    "incident_type",
    "location",
    "victims_count",
    "injury_severity",
    "fire_present",
    "trapped_persons",
    "weapons_involved",
    "hazmat_involved",
)
FORBIDDEN_FIELDS: set[str] = {"urgency", "dispatch", "assets", "staffing"}

VALID_INCIDENT_TYPES = {item.value for item in IncidentType}
VALID_INJURY_SEVERITY = {item.value for item in InjurySeverity}
VALID_TRISTATE = {item.value for item in TriState}


@dataclass(frozen=True)
class WorkflowConfig:
    plan_path: Path
    output_jsonl: Path
    state_db: Path
    model: str = "models/gemini-2.5-flash"
    candidates_per_task: int = 4
    max_repair_rounds: int = 2
    fewshot_count: int = 2
    resume: bool = False
    quality_gate: float = 0.85
    profile_json: Path = Path("dataset/annotations_real_profile.json")
    real_corpus_csv: Path = Path("dataset/annotations_real_calls.csv")
    guard_rules_path: Path = Path("augmentation/kabyle_guard_rules.yaml")
    guard_calibration_report: Path = Path(
        "ml_pipeline/dataset/synthetic_generation/guard_calibration_report.json"
    )
    dry_run: bool = False
    limit: int = 0


@dataclass(frozen=True)
class TaskDefinition:
    task_id: str
    incident_type: str
    requested_examples: int
    prompt_template: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    knowledge_context: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskUnit:
    task_id: str
    incident_type: str
    unit_index: int
    prompt_template: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    knowledge_context: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StructurePattern:
    pattern_id: str
    incident_type: str
    opening_style: str
    turn_count: int
    has_clarification: bool
    has_action_step: bool
    has_location_refinement: bool
    profile_hint: str
    skeleton: List[str] = field(default_factory=list)


@dataclass
class Candidate:
    run_id: str
    task_id: str
    unit_index: int
    candidate_id: str
    transcription: str
    labels: Dict[str, Any]
    reasoning_trace: Dict[str, Any] = field(default_factory=dict)
    constraints_applied: Dict[str, Any] = field(default_factory=dict)
    retrieved_pattern_ids: List[str] = field(default_factory=list)
    repair_rounds: int = 0
    source_type: str = "synthetic"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "task_id": self.task_id,
            "unit_index": self.unit_index,
            "candidate_id": self.candidate_id,
            "transcription": self.transcription,
            "labels": self.labels,
            "reasoning_trace": self.reasoning_trace,
            "constraints_applied": self.constraints_applied,
            "retrieved_pattern_ids": self.retrieved_pattern_ids,
            "repair_rounds": self.repair_rounds,
            "source_type": self.source_type,
        }


@dataclass(frozen=True)
class CriticScore:
    candidate_id: str
    guard_action: str
    guard_score: float
    llm_rubric_score: float
    scenario_coherence_score: float
    location_grounding_score: float
    drift_penalty: float
    quality_score: float
    verdict: str
    blocking_violations: List[str] = field(default_factory=list)
    quality_violations: List[str] = field(default_factory=list)
    adn_drift_flags: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectionDecision:
    selected_candidate_id: Optional[str]
    rejected_reason: Optional[str]
    considered: int


def load_generation_tasks(plan_path: Path, limit: int = 0) -> List[TaskDefinition]:
    tasks: List[TaskDefinition] = []
    if not plan_path.exists():
        return tasks
    with plan_path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            payload = (raw or "").strip()
            if not payload:
                continue
            doc = json.loads(payload)
            task_id = str(doc.get("task_id") or "").strip()
            if not task_id:
                task_id = f"task_{len(tasks) + 1:04d}"
            tasks.append(
                TaskDefinition(
                    task_id=task_id,
                    incident_type=str(doc.get("incident_type") or "unknown").strip().lower(),
                    requested_examples=max(0, int(doc.get("requested_examples") or 0)),
                    prompt_template=str(doc.get("prompt_template") or "").strip(),
                    constraints=dict(doc.get("constraints") or {}),
                    knowledge_context=dict(doc.get("knowledge_context") or {}),
                )
            )
            if limit > 0 and len(tasks) >= limit:
                break
    return tasks


def iter_task_units(task: TaskDefinition, start_index: int = 0) -> Iterator[TaskUnit]:
    for unit_index in range(max(0, start_index), max(0, task.requested_examples)):
        yield TaskUnit(
            task_id=task.task_id,
            incident_type=task.incident_type,
            unit_index=unit_index,
            prompt_template=task.prompt_template,
            constraints=task.constraints,
            knowledge_context=task.knowledge_context,
        )


def clean_tristate(value: Any) -> str:
    lowered = str(value).strip().lower()
    if lowered in {"yes", "oui", "1", "true"}:
        return "yes"
    if lowered in {"no", "non", "0", "false"}:
        return "no"
    return "unknown"


def clean_severity(value: Any) -> str:
    lowered = str(value).strip().lower()
    if lowered in VALID_INJURY_SEVERITY:
        return lowered
    return "unknown"


def clean_incident(value: Any, fallback: str = "unknown") -> str:
    lowered = str(value).strip().lower()
    if lowered in VALID_INCIDENT_TYPES:
        return lowered
    if fallback in VALID_INCIDENT_TYPES:
        return fallback
    return "unknown"


def clean_victims_count(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    if number < 0:
        return None
    return number


def normalize_labels(raw_labels: Dict[str, Any], fallback_incident: str) -> Dict[str, Any]:
    labels = {
        "incident_type": clean_incident(raw_labels.get("incident_type"), fallback=fallback_incident),
        "location": str(raw_labels.get("location") or "unknown").strip() or "unknown",
        "victims_count": clean_victims_count(raw_labels.get("victims_count")),
        "injury_severity": clean_severity(
            raw_labels.get("injury_severity", raw_labels.get("injuries_severity", "unknown"))
        ),
        "fire_present": clean_tristate(raw_labels.get("fire_present")),
        "trapped_persons": clean_tristate(raw_labels.get("trapped_persons")),
        "weapons_involved": clean_tristate(raw_labels.get("weapons_involved")),
        "hazmat_involved": clean_tristate(raw_labels.get("hazmat_involved")),
    }
    for field in FORBIDDEN_FIELDS:
        labels.pop(field, None)
    return labels


def ensure_fact_only_payload(payload: Dict[str, Any], fallback_incident: str) -> Dict[str, Any]:
    raw_labels = payload.get("labels")
    if not isinstance(raw_labels, dict):
        raw_labels = payload.get("extraction") if isinstance(payload.get("extraction"), dict) else payload
    labels = normalize_labels(dict(raw_labels or {}), fallback_incident=fallback_incident)
    return {
        "transcription": str(payload.get("transcription") or "").strip(),
        "labels": labels,
    }


def safe_json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)
