"""
safe_generate.py
----------------
Wrapper resilient autour de generate_synthetic.py.
Lance la generation tache par tache avec sauvegarde intermediaire.

Workflow:
  1. merge_and_organize.py  -> calcule pending_tasks.jsonl
  2. Pour chaque tache dans pending_tasks.jsonl:
     a. Ecrit un plan temporaire (1 seule tache)
     b. Lance generate_synthetic.py en subprocess
     c. Si succes: le fichier output existe, on continue
     d. Si erreur: log, on continue a la tache suivante
  3. merge_and_organize.py  -> re-organise tout

Usage:
  python safe_generate.py
  python safe_generate.py --model models/gemini-3.1-pro-preview
  python safe_generate.py --limit 5    # max 5 taches
  python safe_generate.py --batch 3    # 3 taches par run (defaut: 1)
"""

import json
import subprocess
import sys
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATASET_DIR = ROOT / "ml_pipeline" / "dataset"
SYNTH_DIR = DATASET_DIR / "synthetic_generation"
PENDING_PATH = SYNTH_DIR / "pending_tasks.jsonl"
ORGANIZE_SCRIPT = ROOT / "merge_and_organize.py"
GENERATE_SCRIPT = ROOT / "augmentation" / "generate_synthetic.py"

PYTHON = sys.executable


def run_organize():
    """Run merge_and_organize.py to compute pending tasks."""
    result = subprocess.run(
        [PYTHON, str(ORGANIZE_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        print(f"[!] merge_and_organize.py failed: {result.stderr[:300]}")
        return False
    # Print only the summary lines
    for line in result.stdout.splitlines():
        if any(k in line for k in ["SOURCE", "DONE", "organized", "pending", "progress"]):
            print(f"  {line}")
    return True


def load_pending():
    """Load pending tasks from JSONL."""
    if not PENDING_PATH.exists():
        return []
    tasks = []
    with PENDING_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    return tasks


def run_generation(temp_plan_path, output_path, extra_args):
    """Run generate_synthetic.py on a single temp plan file."""
    cmd = [
        PYTHON, str(GENERATE_SCRIPT),
        "--plan_path", str(temp_plan_path),
        "--output_jsonl", str(output_path),
    ] + extra_args

    try:
        result = subprocess.run(
            cmd,
            timeout=600,  # 10 min max per batch
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if result.returncode != 0:
            print(f"  [ERREUR] Exit code {result.returncode}")
            stderr_lines = result.stderr.strip().splitlines()
            for line in stderr_lines[-5:]:
                print(f"    {line}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print("  [TIMEOUT] La tache a depasse 10 minutes")
        return False
    except Exception as e:
        print(f"  [EXCEPTION] {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Safe generation wrapper — task by task with intermediate saves.")
    parser.add_argument("--limit", type=int, default=0, help="Max number of tasks to process (0=all)")
    parser.add_argument("--batch", type=int, default=1, help="Number of tasks per generation run (default: 1)")
    args, extra_args = parser.parse_known_args()

    print("=" * 60)
    print("SAFE GENERATE — Resilient wrapper")
    print("=" * 60)

    # Step 1: Organize and compute pending
    print("\n[1/3] Organizing existing data and computing pending tasks...")
    if not run_organize():
        print("[!] Could not organize. Continuing with existing pending_tasks.jsonl if available.")

    # Step 2: Load pending tasks
    tasks = load_pending()
    if not tasks:
        print("\n[OK] No pending tasks. Everything is generated.")
        return

    total = len(tasks)
    limit = args.limit if args.limit > 0 else total
    batch_size = max(1, args.batch)
    to_process = tasks[:limit]

    print(f"\n[2/3] Processing {len(to_process)}/{total} pending tasks (batch_size={batch_size})")
    if extra_args:
        print(f"  Extra args passed to generate_synthetic.py: {' '.join(extra_args)}")

    done_count = 0
    error_count = 0
    i = 0

    try:
        while i < len(to_process):
            batch = to_process[i:i + batch_size]
            task_ids = [t.get("task_id", "?") for t in batch]

            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            batch_label = f"batch_{i+1:03d}"
            output_file = DATASET_DIR / f"annotations_synthetic_{timestamp}_{batch_label}.jsonl"

            print(f"\n  [{i+1}-{i+len(batch)}/{len(to_process)}] Tasks: {', '.join(task_ids)}")

            # Write temp plan file
            temp_plan = SYNTH_DIR / f"_temp_plan_{batch_label}.jsonl"
            temp_plan.parent.mkdir(parents=True, exist_ok=True)
            with temp_plan.open("w", encoding="utf-8") as f:
                for task in batch:
                    f.write(json.dumps(task, ensure_ascii=False) + "\n")

            # Run generation
            success = run_generation(temp_plan, output_file, extra_args)

            # Cleanup temp plan
            try:
                temp_plan.unlink()
            except OSError:
                pass

            if success and output_file.exists() and output_file.stat().st_size > 0:
                # Count generated rows
                with output_file.open("r", encoding="utf-8") as f:
                    n_rows = sum(1 for line in f if line.strip())
                print(f"  [OK] {n_rows} rows saved to {output_file.name}")
                done_count += len(batch)
            else:
                print(f"  [SKIP] No output generated for this batch")
                error_count += len(batch)
                # Remove empty output file if created
                if output_file.exists() and output_file.stat().st_size == 0:
                    output_file.unlink()

            i += batch_size

    except KeyboardInterrupt:
        print(f"\n\n[CTRL+C] Arret demande par l'utilisateur.")
        print(f"  {done_count} taches completees avant l'arret.")

    # Step 3: Final organize
    print(f"\n[3/3] Final organization...")
    run_organize()

    print(f"\n{'=' * 60}")
    print(f"RESULTAT: {done_count} OK, {error_count} erreurs, {total - done_count - error_count} restantes")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
