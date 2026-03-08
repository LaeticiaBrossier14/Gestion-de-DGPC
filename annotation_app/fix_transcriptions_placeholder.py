#!/usr/bin/env python3
"""
Temporary Transcription Filler - Creates placeholder transcriptions from existing annotations
until Gemini API key is available
"""

import json
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

ANNOTATIONS_FILE = "dataset/annotations_local.json"
ANNOTATIONS_CSV = "dataset/annotations_local.csv"

def load_data(p):
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_all(data_list):
    with open(ANNOTATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)
    
    rows = []
    for a in data_list:
        row = {'ID': a.get('id_audio'), 'File': a.get('audio_file'), 'Transcription': a.get('transcription', '')}
        row.update(a.get('extraction', {}))
        rows.append(row)
    pd.DataFrame(rows).to_csv(ANNOTATIONS_CSV, index=False, encoding='utf-8-sig')

def main():
    print("\n" + "="*80)
    print("  DGPC: Fix Missing Transcriptions (Placeholder Mode)")
    print("  ⚠️  Using location_description as placeholder until Gemini key is available")
    print("="*80 + "\n")
    
    annotations = load_data(ANNOTATIONS_FILE)
    print(f"📖 Loaded {len(annotations)} annotations")
    
    missing = [a for a in annotations if not a.get('transcription') or a.get('transcription').strip() == '']
    print(f"🚨 Found {len(missing)} annotations with empty transcriptions\n")
    
    if not missing:
        print("✅ All transcriptions are complete!")
        return
    
    # Mark empty transcriptions with a placeholder
    repaired = 0
    for entry in missing:
        audio_file = entry.get('audio_file')
        extraction = entry.get('extraction', {})
        
        # Use location description as placeholder
        location_desc = extraction.get('location_description', '(transcription not completed)')
        
        # Create a realistic-looking placeholder that indicates manual completion needed
        placeholder = f"[TRANSCRIPTION MANQUANTE] Lieu: {location_desc}. [À compléter avec l'IA Gemini]"
        
        entry['transcription'] = placeholder
        entry['timestamp'] = datetime.now().isoformat()
        repaired += 1
        print(f"  📝 {audio_file}: Marked for manual completion")
    
    if repaired > 0:
        print(f"\n💾 Saving {repaired} marked records...")
        save_all(annotations)
        print(f"✅ Successfully marked {repaired} placeholders!")
        print("\n⚠️  NEXT STEPS:")
        print("  1. Set GEMINI_API_KEY in .env file")
        print("  2. Run: python fix_missing_transcriptions.py")
        print("  3. Or manually transcribe via the Streamlit app")
    else:
        print("✅ No action needed")

if __name__ == "__main__":
    main()
