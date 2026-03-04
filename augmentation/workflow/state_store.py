"""SQLite state storage for workflow v2.

The store is intentionally append-friendly and idempotent:
- candidate rows are keyed by (run_id, task_id, unit_index, candidate_id)
- final rows are keyed by (run_id, row_id)
- guard history is global to the DB for cross-run calibration
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

from augmentation.workflow.contracts import Candidate, CriticScore, TaskDefinition, WorkflowConfig


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class StateStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def initialize(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                PRAGMA journal_mode=WAL;

                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    config_json TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tasks (
                    run_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    incident_type TEXT NOT NULL,
                    requested_examples INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    next_unit_index INTEGER NOT NULL DEFAULT 0,
                    completed_units INTEGER NOT NULL DEFAULT 0,
                    error TEXT,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (run_id, task_id)
                );

                CREATE TABLE IF NOT EXISTS candidates (
                    run_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    unit_index INTEGER NOT NULL,
                    candidate_id TEXT NOT NULL,
                    repair_rounds INTEGER NOT NULL DEFAULT 0,
                    transcription TEXT NOT NULL,
                    labels_json TEXT NOT NULL,
                    reasoning_trace_json TEXT NOT NULL,
                    constraints_json TEXT NOT NULL,
                    retrieved_pattern_ids_json TEXT NOT NULL,
                    critic_json TEXT,
                    guard_action TEXT,
                    guard_score REAL,
                    quality_score REAL,
                    verdict TEXT,
                    selected INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (run_id, task_id, unit_index, candidate_id)
                );

                CREATE INDEX IF NOT EXISTS idx_candidates_task
                    ON candidates(run_id, task_id, unit_index);
                CREATE INDEX IF NOT EXISTS idx_candidates_selected
                    ON candidates(run_id, selected);

                CREATE TABLE IF NOT EXISTS final_rows (
                    run_id TEXT NOT NULL,
                    row_id TEXT NOT NULL,
                    task_id TEXT NOT NULL,
                    unit_index INTEGER NOT NULL,
                    candidate_id TEXT NOT NULL,
                    row_json TEXT NOT NULL,
                    quality_score REAL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (run_id, row_id)
                );

                CREATE INDEX IF NOT EXISTS idx_final_rows_task
                    ON final_rows(run_id, task_id, unit_index);

                CREATE TABLE IF NOT EXISTS guard_history (
                    guard_run_id TEXT PRIMARY KEY,
                    timestamp_utc TEXT NOT NULL,
                    pass_rate REAL NOT NULL,
                    mean_score REAL NOT NULL,
                    summary_json TEXT NOT NULL
                );
                """
            )

    def latest_active_run(self) -> Optional[str]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT run_id FROM runs
                WHERE status IN ('running', 'paused')
                ORDER BY updated_at DESC
                LIMIT 1
                """
            ).fetchone()
            return str(row["run_id"]) if row else None

    def create_or_resume_run(self, config: WorkflowConfig, resume: bool = False) -> str:
        with self._connect() as conn:
            if resume:
                row = conn.execute(
                    "SELECT run_id FROM runs WHERE status IN ('running', 'paused') ORDER BY updated_at DESC LIMIT 1"
                ).fetchone()
                if row:
                    run_id = str(row["run_id"])
                    conn.execute(
                        "UPDATE runs SET status='running', updated_at=? WHERE run_id=?",
                        (_utc_now(), run_id),
                    )
                    return run_id

            run_id = datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%SZ")
            payload = json.dumps(asdict(config), default=str, ensure_ascii=False)
            now = _utc_now()
            conn.execute(
                "INSERT INTO runs(run_id, created_at, updated_at, status, config_json) VALUES (?, ?, ?, ?, ?)",
                (run_id, now, now, "running", payload),
            )
            return run_id

    def set_run_status(self, run_id: str, status: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE runs SET status=?, updated_at=? WHERE run_id=?",
                (status, _utc_now(), run_id),
            )

    def upsert_task(self, run_id: str, task: TaskDefinition) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO tasks(run_id, task_id, incident_type, requested_examples, status, next_unit_index, completed_units, error, updated_at)
                VALUES (?, ?, ?, ?, 'pending', 0, 0, NULL, ?)
                ON CONFLICT(run_id, task_id)
                DO UPDATE SET
                    incident_type=excluded.incident_type,
                    requested_examples=excluded.requested_examples,
                    updated_at=excluded.updated_at
                """,
                (
                    run_id,
                    task.task_id,
                    task.incident_type,
                    int(task.requested_examples),
                    _utc_now(),
                ),
            )

    def list_tasks(self, run_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT run_id, task_id, incident_type, requested_examples, status, next_unit_index, completed_units, error
                FROM tasks
                WHERE run_id=?
                ORDER BY task_id
                """,
                (run_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def set_task_state(
        self,
        run_id: str,
        task_id: str,
        *,
        status: str,
        next_unit_index: int,
        completed_units: int,
        error: Optional[str] = None,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE tasks
                SET status=?, next_unit_index=?, completed_units=?, error=?, updated_at=?
                WHERE run_id=? AND task_id=?
                """,
                (status, int(next_unit_index), int(completed_units), error, _utc_now(), run_id, task_id),
            )

    def count_completed_units(self, run_id: str, task_id: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM final_rows WHERE run_id=? AND task_id=?",
                (run_id, task_id),
            ).fetchone()
            return int(row["cnt"] if row else 0)

    def unit_already_selected(self, run_id: str, task_id: str, unit_index: int) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT 1 FROM final_rows
                WHERE run_id=? AND task_id=? AND unit_index=?
                LIMIT 1
                """,
                (run_id, task_id, int(unit_index)),
            ).fetchone()
            return bool(row)

    def save_candidate(self, candidate: Candidate, critic: Optional[CriticScore]) -> None:
        critic_payload = critic.to_dict() if critic is not None else None
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO candidates(
                    run_id, task_id, unit_index, candidate_id, repair_rounds, transcription,
                    labels_json, reasoning_trace_json, constraints_json, retrieved_pattern_ids_json,
                    critic_json, guard_action, guard_score, quality_score, verdict, selected, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                ON CONFLICT(run_id, task_id, unit_index, candidate_id)
                DO UPDATE SET
                    repair_rounds=excluded.repair_rounds,
                    transcription=excluded.transcription,
                    labels_json=excluded.labels_json,
                    reasoning_trace_json=excluded.reasoning_trace_json,
                    constraints_json=excluded.constraints_json,
                    retrieved_pattern_ids_json=excluded.retrieved_pattern_ids_json,
                    critic_json=excluded.critic_json,
                    guard_action=excluded.guard_action,
                    guard_score=excluded.guard_score,
                    quality_score=excluded.quality_score,
                    verdict=excluded.verdict
                """,
                (
                    candidate.run_id,
                    candidate.task_id,
                    int(candidate.unit_index),
                    candidate.candidate_id,
                    int(candidate.repair_rounds),
                    candidate.transcription,
                    json.dumps(candidate.labels, ensure_ascii=False),
                    json.dumps(candidate.reasoning_trace, ensure_ascii=False),
                    json.dumps(candidate.constraints_applied, ensure_ascii=False),
                    json.dumps(candidate.retrieved_pattern_ids, ensure_ascii=False),
                    json.dumps(critic_payload, ensure_ascii=False) if critic_payload is not None else None,
                    critic.guard_action if critic else None,
                    float(critic.guard_score) if critic else None,
                    float(critic.quality_score) if critic else None,
                    critic.verdict if critic else None,
                    _utc_now(),
                ),
            )

    def list_candidates(self, run_id: str, task_id: str, unit_index: int) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT candidate_id, repair_rounds, transcription, labels_json, reasoning_trace_json,
                       constraints_json, retrieved_pattern_ids_json, critic_json,
                       guard_action, guard_score, quality_score, verdict, selected
                FROM candidates
                WHERE run_id=? AND task_id=? AND unit_index=?
                ORDER BY quality_score DESC, candidate_id ASC
                """,
                (run_id, task_id, int(unit_index)),
            ).fetchall()

        payload: List[Dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            for key in (
                "labels_json",
                "reasoning_trace_json",
                "constraints_json",
                "retrieved_pattern_ids_json",
                "critic_json",
            ):
                raw = item.pop(key, None)
                if raw:
                    item[key.replace("_json", "")] = json.loads(raw)
                else:
                    item[key.replace("_json", "")] = {} if "ids" not in key else []
            payload.append(item)
        return payload

    def mark_selected_candidate(
        self,
        run_id: str,
        task_id: str,
        unit_index: int,
        candidate_id: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE candidates
                SET selected=CASE WHEN candidate_id=? THEN 1 ELSE 0 END
                WHERE run_id=? AND task_id=? AND unit_index=?
                """,
                (candidate_id, run_id, task_id, int(unit_index)),
            )

    def insert_final_row(
        self,
        run_id: str,
        row_id: str,
        task_id: str,
        unit_index: int,
        candidate_id: str,
        row_payload: Dict[str, Any],
        quality_score: float,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO final_rows(
                    run_id, row_id, task_id, unit_index, candidate_id, row_json, quality_score, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    row_id,
                    task_id,
                    int(unit_index),
                    candidate_id,
                    json.dumps(row_payload, ensure_ascii=False),
                    float(quality_score),
                    _utc_now(),
                ),
            )

    def get_final_rows(self, run_id: str) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT row_id, task_id, unit_index, candidate_id, row_json, quality_score
                FROM final_rows
                WHERE run_id=?
                ORDER BY task_id ASC, unit_index ASC
                """,
                (run_id,),
            ).fetchall()
        output: List[Dict[str, Any]] = []
        for row in rows:
            record = dict(row)
            record["row"] = json.loads(record.pop("row_json"))
            output.append(record)
        return output

    def list_selected_transcriptions(self, run_id: str) -> List[str]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT row_json FROM final_rows
                WHERE run_id=?
                ORDER BY task_id ASC, unit_index ASC
                """,
                (run_id,),
            ).fetchall()
        texts: List[str] = []
        for row in rows:
            payload = json.loads(row["row_json"])
            text = str(payload.get("transcription") or "").strip()
            if text:
                texts.append(text)
        return texts

    def record_guard_summary(self, guard_run_id: str, summary: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO guard_history(guard_run_id, timestamp_utc, pass_rate, mean_score, summary_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(guard_run_id)
                DO UPDATE SET
                    timestamp_utc=excluded.timestamp_utc,
                    pass_rate=excluded.pass_rate,
                    mean_score=excluded.mean_score,
                    summary_json=excluded.summary_json
                """,
                (
                    guard_run_id,
                    str(summary.get("timestamp_utc") or _utc_now()),
                    float(summary.get("pass_rate") or 0.0),
                    float(summary.get("mean_score") or 0.0),
                    json.dumps(summary, ensure_ascii=False),
                ),
            )

    def list_guard_history(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT summary_json FROM guard_history ORDER BY timestamp_utc ASC"
            ).fetchall()
        return [json.loads(row["summary_json"]) for row in rows]

    def export_output_jsonl(self, run_id: str, output_path: Path) -> int:
        rows = self.get_final_rows(run_id)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row["row"], ensure_ascii=False) + "\n")
        return len(rows)
