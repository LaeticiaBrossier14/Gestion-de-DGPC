"""Inspect transcription quality - write to file to avoid encoding issues."""
import json, pathlib

f = pathlib.Path("ml_pipeline/dataset/synthetic_generation/synth_batch_phase3.jsonl")
rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]

out = pathlib.Path("_quality_review.txt")
lines = [f"Total: {len(rows)} rows\n\n"]
for i, r in enumerate(rows[:15]):
    score = r["meta"].get("guard_score", "?")
    ex = r["meta"].get("exercise_type", "?")
    t = r["transcription"]
    wc = len(t.split())
    lines.append(f"--- [{i+1}] score={score} ex={ex} words={wc} ---\n{t}\n\n")

out.write_text("".join(lines), encoding="utf-8")
print(f"Written {len(lines)-1} samples to {out}")
