import json

with open('verification_tool/verification_progress.json', 'r', encoding='utf-8') as f:
    prog = json.load(f)

examples = list(prog.items())[:3]
for k, v in examples:
    print(f"KEY: {k}")
    print(f"  status: {v.get('status')}")
    print(f"  corrected_transcription: {repr(v.get('corrected_transcription', '')[:100])}")
    print(f"  original_transcription field exists: {'original_transcription' in v}")
    print(f"  keys: {list(v.keys())}")
    print()
