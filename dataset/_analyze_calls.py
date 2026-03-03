"""Analyze real annotated calls to extract linguistic DNA."""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CSV_PATH = Path(r"g:\AZ\Documents\gestion des appelles telephoniques\dataset\annotations_local.csv")

def load_calls():
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows

def analyze():
    rows = load_calls()
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {list(rows[0].keys())[:15]}...")
    
    # Filter rows with transcriptions
    calls = [r for r in rows if r.get("Transcription", "").strip()]
    print(f"Rows with transcription: {len(calls)}")
    
    # Incident type distribution
    incident_counts = Counter()
    for r in calls:
        it = r.get("incident_type", "").strip() or r.get("Type_incident", "").strip() or "unknown"
        incident_counts[it] += 1
    print(f"\n=== INCIDENT TYPE DISTRIBUTION ===")
    for k, v in incident_counts.most_common():
        print(f"  {k}: {v} ({v/len(calls)*100:.1f}%)")
    
    # Print ALL transcriptions for deep analysis
    print(f"\n{'='*80}")
    print(f"=== ALL {len(calls)} TRANSCRIPTIONS (FULL TEXT) ===")
    print(f"{'='*80}")
    
    for i, row in enumerate(calls):
        transcript = row.get("Transcription", "").strip()
        incident = row.get("incident_type", "") or row.get("Type_incident", "") or "?"
        location = row.get("location_description", "") or row.get("lieu", "") or row.get("commune", "") or "?"
        severity = row.get("injury_severity", "") or row.get("gravite", "") or "?"
        intent = row.get("intent", "") or "?"
        
        print(f"\n--- CALL #{i+1} | incident={incident} | severity={severity} ---")
        print(f"Location: {location}")
        print(f"Intent: {intent}")
        print(f"Transcription:")
        print(transcript)
        print(f"---")

def write_analysis():
    import io
    out_path = CSV_PATH.parent / "_call_analysis_output.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        import sys
        old_stdout = sys.stdout
        sys.stdout = f
        analyze()
        sys.stdout = old_stdout
    print(f"Written to {out_path}")

if __name__ == "__main__":
    write_analysis()
