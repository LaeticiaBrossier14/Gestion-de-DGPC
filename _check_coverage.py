import re, json
from urllib.request import urlopen

# 1. Parse scenarios from scenarios_data.js
with open("g:/AZ/Documents/collecte-audio-bejaia/scenarios_data.js", "r", encoding="utf-8") as f:
    content = f.read()

# Extract scenario IDs
ids = re.findall(r'id:\s*["\x27](.*?)["\x27]', content)
print(f"Total scenarios in app: {len(ids)}")

# 2. Fetch stats from Google Apps Script
url = "https://script.google.com/macros/s/AKfycbxA7OCkwYrnwGi2otRHvZw8Wkn9rW8Vvar9crXrwsM-b4Wg_Fej8q-ZiBt1uDUrw00/exec"
try:
    resp = urlopen(url, timeout=15)
    stats = json.loads(resp.read().decode())
    recorded = set(stats.get("scenarios", {}).keys())
    print(f"Scenarios with recordings: {len(recorded)}")
    print(f"Total audios: {stats.get('total_audios', '?')}")
    print(f"Total contributors: {stats.get('total_contributors', '?')}")
except Exception as e:
    print(f"Could not fetch stats: {e}")
    # Fallback: just list all scenario IDs
    recorded = set()

# 3. Compare
all_ids = set(ids)
missing = all_ids - recorded
extra = recorded - all_ids

print(f"\n--- COVERAGE ---")
print(f"Scenarios in app: {len(all_ids)}")
print(f"Scenarios recorded: {len(recorded)}")
print(f"Missing (no audio): {len(missing)}")

if missing:
    print(f"\nMissing scenarios:")
    for m in sorted(missing):
        print(f"  - {m}")

if extra:
    print(f"\nExtra (in Drive but not in app): {len(extra)}")
    for e in sorted(extra):
        print(f"  - {e}")

# 4. Coverage per scenario (how many contributors)
if recorded:
    scenarios = stats.get("scenarios", {})
    one_contrib = [s for s, c in scenarios.items() if c == 1]
    two_contrib = [s for s, c in scenarios.items() if c == 2]
    three_plus = [s for s, c in scenarios.items() if c >= 3]
    print(f"\n--- DEPTH ---")
    print(f"1 contributor only: {len(one_contrib)}")
    print(f"2 contributors: {len(two_contrib)}")
    print(f"3+ contributors (target met): {len(three_plus)}")
