"""Quick check: SYNTH metadata in Phase 2 output."""
import json, pathlib

f = pathlib.Path("ml_pipeline/dataset/synthetic_generation/_test_phase2.jsonl")
rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]

print(f"Total rows: {len(rows)}")
r = rows[0]
meta = r["meta"]
print(f"\nMeta keys: {sorted(meta.keys())}")
print(f"\nexercise_type: {meta.get('exercise_type', 'MISSING')}")
print(f"is_negative: {meta.get('is_negative', 'MISSING')}")
print(f"seed_id: {meta.get('seed_id', 'MISSING')}")
print(f"source_type: {meta.get('source_type', 'MISSING')}")
print(f"constraints_applied: {meta.get('constraints_applied', 'MISSING')}")
print(f"timestamp_utc: {meta.get('timestamp_utc', 'MISSING')}")

# Verify all rows
synth_fields = ["exercise_type", "seed_id", "is_negative", "source_type", "timestamp_utc"]
for i, row in enumerate(rows):
    for field in synth_fields:
        assert field in row["meta"], f"Row {i}: missing {field}"
    assert "constraints_applied" in row["meta"], f"Row {i}: missing constraints_applied"
    ca = row["meta"]["constraints_applied"]
    for k in ["lang_profile", "stress_level", "info_quantity", "time_period"]:
        assert k in ca, f"Row {i}: missing constraints_applied.{k}"

print(f"\n All {len(rows)} rows verified: SYNTH metadata complete")

# Cleanup
f.unlink()
print("Test file deleted.")
