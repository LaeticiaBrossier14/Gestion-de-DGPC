"""
merge_and_organize.py
---------------------
1. Lit tous les annotations_synthetic*.jsonl depuis ml_pipeline/dataset/
2. Organise en sous-dossiers par type d'incident
3. Compare avec generation_tasks.jsonl pour suivre la progression
4. Ecrit pending_tasks.jsonl avec les taches restantes

Usage:
    python merge_and_organize.py
    python merge_and_organize.py --no_track   (sans suivi de progression)
"""
import json
import glob
import os
import re
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
DATASET_DIR = ROOT / "ml_pipeline" / "dataset"
ORGANIZED_DIR = DATASET_DIR / "organized"
SOURCE_PATTERN = str(DATASET_DIR / "annotations_synthetic*.jsonl")
GENERATION_TASKS_PATH = DATASET_DIR / "synthetic_generation" / "generation_tasks.jsonl"
PENDING_TASKS_PATH = DATASET_DIR / "synthetic_generation" / "pending_tasks.jsonl"
PROGRESS_REPORT_PATH = DATASET_DIR / "synthetic_generation" / "progress_report.json"


# ─────────────────────────────────────────────
#  STEP 1: Merge & Organize
# ─────────────────────────────────────────────

def merge_and_organize():
    """Lit tous les JSONL source, deduplique, organise par incident_type."""
    source_files = sorted(glob.glob(SOURCE_PATTERN))
    if not source_files:
        print("[!] Aucun fichier annotations_synthetic*.jsonl trouve dans ml_pipeline/dataset/")
        return 0

    print(f"[SOURCE] {len(source_files)} fichier(s) trouve(s):")
    for f in source_files:
        print(f"   - {os.path.basename(f)}")

    # Lire et dedupliquer par id
    all_rows: dict = {}
    total_read = 0
    for fp in source_files:
        count = 0
        with open(fp, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    row_id = row.get("id", "")
                    if row_id and row_id not in all_rows:
                        all_rows[row_id] = row
                        count += 1
                except json.JSONDecodeError:
                    continue
        total_read += count
        print(f"   OK {os.path.basename(fp)}: {count} entrees chargees")

    print(f"\n[STATS] Total: {len(all_rows)} entrees uniques (sur {total_read} lues)")

    # Grouper par incident_type
    by_type: dict = defaultdict(list)
    no_type = 0
    for row in all_rows.values():
        incident = row.get("labels", {}).get("incident_type", "")
        if not incident:
            incident = "unknown"
            no_type += 1
        by_type[incident].append(row)

    if no_type:
        print(f"   [!] {no_type} entree(s) sans incident_type -> classees dans 'unknown'")

    # Ecrire les fichiers organises
    ORGANIZED_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n[ORGANISATION] Dossier cible: {ORGANIZED_DIR}")
    total_written = 0
    for incident_type, rows in sorted(by_type.items()):
        type_dir = ORGANIZED_DIR / incident_type
        type_dir.mkdir(exist_ok=True)
        out_path = type_dir / "scenarios.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"   {incident_type}/: {len(rows)} scenarios")
        total_written += len(rows)

    print(f"\n[DONE] {total_written} scenarios organises dans {len(by_type)} dossiers")
    return total_written


# ─────────────────────────────────────────────
#  STEP 2: Progress Tracking
# ─────────────────────────────────────────────

def count_generated_per_task(organized_dir: Path) -> Counter:
    """Compte les rows par meta.task_id depuis les fichiers organises."""
    counts: Counter = Counter()
    for scenarios_file in organized_dir.glob("*/scenarios.jsonl"):
        with scenarios_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    tid = row.get("meta", {}).get("task_id", "")
                    if tid:
                        counts[tid] += 1
                except json.JSONDecodeError:
                    continue
    return counts


def track_progress(tasks_path: Path, organized_dir: Path):
    """Compare generation_tasks avec les donnees organisees.
    Retourne (master_tasks, generated_counts, pending_tasks, stats)."""

    # Charger les taches
    master_tasks = []
    with tasks_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                master_tasks.append(json.loads(line))

    # Compter ce qui est deja genere
    generated_counts = count_generated_per_task(organized_dir)

    # Classer chaque tache
    pending_tasks = []
    stats = {"done": 0, "partial": 0, "pending": 0}

    for task in master_tasks:
        task_id = task["task_id"]
        requested = task["requested_examples"]
        generated = generated_counts.get(task_id, 0)
        remaining = max(0, requested - generated)

        if remaining == 0:
            stats["done"] += 1
        elif generated > 0:
            stats["partial"] += 1
            pending_task = json.loads(json.dumps(task))
            pending_task["requested_examples"] = remaining
            pending_task["prompt_template"] = re.sub(
                r"^Generate \d+",
                f"Generate {remaining}",
                pending_task.get("prompt_template", ""),
            )
            pending_tasks.append(pending_task)
        else:
            stats["pending"] += 1
            pending_tasks.append(task)

    return master_tasks, generated_counts, pending_tasks, stats


def print_progress_table(master_tasks, generated_counts):
    """Affiche le tableau de progression (ASCII, pas d'emojis)."""
    by_type = defaultdict(lambda: {
        "tasks": 0, "done": 0, "partial": 0, "pending": 0,
        "generated": 0, "requested": 0
    })

    for task in master_tasks:
        tid = task["task_id"]
        itype = task["incident_type"]
        requested = task["requested_examples"]
        generated = min(generated_counts.get(tid, 0), requested)
        remaining = max(0, requested - generated)

        entry = by_type[itype]
        entry["tasks"] += 1
        entry["requested"] += requested
        entry["generated"] += generated
        if remaining == 0:
            entry["done"] += 1
        elif generated > 0:
            entry["partial"] += 1
        else:
            entry["pending"] += 1

    header = f"{'Type':<24} {'Tasks':>5} {'Done':>5} {'Part.':>5} {'Pend.':>5} {'Gen/Req':>10}"
    sep = "-" * len(header)

    print("\n=== PROGRESS REPORT ===")
    print(header)
    print(sep)

    totals = {"tasks": 0, "done": 0, "partial": 0, "pending": 0, "generated": 0, "requested": 0}
    for itype, e in sorted(by_type.items()):
        print(f"{itype:<24} {e['tasks']:>5} {e['done']:>5} {e['partial']:>5} {e['pending']:>5} {e['generated']:>4}/{e['requested']:<4}")
        for k in totals:
            totals[k] += e[k]

    print(sep)
    print(f"{'TOTAL':<24} {totals['tasks']:>5} {totals['done']:>5} {totals['partial']:>5} {totals['pending']:>5} {totals['generated']:>4}/{totals['requested']:<4}")

    pct = (totals["generated"] / totals["requested"] * 100) if totals["requested"] else 0
    print(f"\nProgression: {pct:.1f}%")


def write_pending_tasks(pending_tasks, output_path: Path):
    """Ecrit les taches restantes dans un fichier JSONL."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for task in pending_tasks:
            f.write(json.dumps(task, ensure_ascii=False) + "\n")


def write_progress_report(master_tasks, generated_counts, pending_tasks, stats):
    """Ecrit un rapport machine-readable en JSON."""
    total_requested = sum(t["requested_examples"] for t in master_tasks)
    total_generated = sum(
        min(generated_counts.get(t["task_id"], 0), t["requested_examples"])
        for t in master_tasks
    )

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tasks_total": len(master_tasks),
        "tasks_done": stats["done"],
        "tasks_partial": stats["partial"],
        "tasks_pending": stats["pending"],
        "rows_generated": total_generated,
        "rows_requested": total_requested,
        "rows_remaining": total_requested - total_generated,
        "pending_tasks_path": str(PENDING_TASKS_PATH),
        "pending_tasks_count": len(pending_tasks),
    }

    PROGRESS_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Merge, organize, and track synthetic data.")
    parser.add_argument("--tasks_path", default=str(GENERATION_TASKS_PATH),
                        help="Chemin vers generation_tasks.jsonl")
    parser.add_argument("--no_track", action="store_true",
                        help="Sauter le suivi de progression")
    args = parser.parse_args()

    # --- Organiser ---
    merge_and_organize()

    # --- Suivi de progression ---
    tasks_path = Path(args.tasks_path)
    if args.no_track:
        return

    if not tasks_path.exists():
        print(f"\n[SKIP] Pas de suivi: {tasks_path.name} introuvable")
        return

    master_tasks, generated_counts, pending_tasks, stats = track_progress(
        tasks_path, ORGANIZED_DIR
    )

    print_progress_table(master_tasks, generated_counts)

    if pending_tasks:
        write_pending_tasks(pending_tasks, PENDING_TASKS_PATH)
        write_progress_report(master_tasks, generated_counts, pending_tasks, stats)
        remaining = sum(t["requested_examples"] for t in pending_tasks)
        print(f"\n[PENDING] {len(pending_tasks)} tache(s) restante(s) -> {PENDING_TASKS_PATH.name}")
        print(f"   {remaining} exemples a generer")
    else:
        print("\n[COMPLET] Toutes les taches sont completees!")
        if PENDING_TASKS_PATH.exists():
            PENDING_TASKS_PATH.unlink()


if __name__ == "__main__":
    main()
