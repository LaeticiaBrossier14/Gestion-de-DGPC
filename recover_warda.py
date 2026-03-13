import json
import subprocess

print("Extraction des données de Warda depuis le commit 76755ad...")
result = subprocess.run(
    ["git", "show", "76755ad:verification_tool/verification_progress.json"], 
    cwd=r"f:\dgpc_pipeline_ready", 
    capture_output=True, 
    text=True, 
    encoding='utf-8'
)

if result.returncode != 0:
    print("Failed to run git show")
    exit(1)

content = result.stdout
try:
    warda_progress = json.loads(content)
except Exception as e:
    print("Error parsing warda progress:", e)
    exit(1)

current_path = r"f:\dgpc_pipeline_ready\verification_tool\verification_progress.json"

with open(current_path, "r", encoding="utf-8") as f:
    current_progress = json.load(f)

added = 0
for key, value in warda_progress.items():
    if key not in current_progress:
        current_progress[key] = value
        added += 1
    else:
        current_ts = current_progress[key].get("timestamp", "")
        warda_ts = value.get("timestamp", "")
        if warda_ts > current_ts:
            current_progress[key] = value
            added += 1

with open(current_path, "w", encoding="utf-8") as f:
    json.dump(current_progress, f, indent=2, ensure_ascii=False)

print(f"Fusion terminée ! {added} audios ont été récupérés/mis à jour.")
