import json
import subprocess
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
FILE_PATH = PROJECT_ROOT / "verification_tool" / "verification_progress.json"
FILE_PATH_GIT = FILE_PATH.relative_to(PROJECT_ROOT).as_posix()
API_URL = "http://localhost:5000/api/reload"


def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_ROOT)


def load_json_safe(content):
    try:
        if isinstance(content, bytes):
            return json.loads(content.decode("utf-8"))
        if isinstance(content, str):
            return json.loads(content)
        return None
    except Exception:
        return None



def parse_timestamp(entry):
    raw = (entry or {}).get("timestamp", "1970-01-01T00:00:00")
    try:
        return datetime.fromisoformat(raw)
    except Exception:
        return datetime.fromisoformat("1970-01-01T00:00:00")


def merge_progress(base_data, incoming_data):
    merged = dict(base_data or {})
    count_added = 0
    count_updated = 0

    for key, value in (incoming_data or {}).items():
        if key not in merged:
            merged[key] = value
            count_added += 1
            continue
        if parse_timestamp(value) > parse_timestamp(merged[key]):
            merged[key] = value
            count_updated += 1

    return merged, count_added, count_updated


def load_git_object(spec):
    result = subprocess.run(
        ["git", "show", spec],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=PROJECT_ROOT,
    )
    if result.returncode != 0:
        return None
    return load_json_safe(result.stdout)


def read_current_progress():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        ours = load_git_object(f":2:{FILE_PATH_GIT}")
        theirs = load_git_object(f":3:{FILE_PATH_GIT}")
        if ours is None and theirs is None:
            return {}
        if ours is None:
            return theirs
        if theirs is None:
            return ours
        merged, _, _ = merge_progress(theirs, ours)
        return merged


def has_unmerged_file():
    result = run_cmd(f'git ls-files -u "{FILE_PATH_GIT}"')
    return bool(result.stdout.strip())


def sync():
    print("--- Debut de la synchronisation intelligente ---")

    status = run_cmd("git status --porcelain")
    tracked_lines = [line.strip() for line in status.stdout.splitlines() if line.strip()]
    has_changes = any(FILE_PATH_GIT in line for line in tracked_lines)

    stash_created = False
    if has_changes:
        print("[INFO] Modifications locales detectees. Sauvegarde temporaire...")
        stash_result = run_cmd(f'git stash push -m "sync-auto-save" -- "{FILE_PATH_GIT}"')
        stash_created = "No local changes to save" not in stash_result.stdout

    print("[INFO] Recuperation du travail de la binome (git pull)...")
    pull_result = run_cmd("git pull")
    if pull_result.returncode != 0:
        print("[AVERTISSEMENT] git pull a retourne une erreur, tentative de fusion locale.")

    if has_unmerged_file():
        print("[AVERTISSEMENT] Conflit detecte. Resolution en cours...")
        run_cmd(f'git checkout --theirs -- "{FILE_PATH_GIT}"')

    base_data = read_current_progress()
    stash_data = {}

    if stash_created:
        stash_data = load_git_object(f"stash@{{0}}:{FILE_PATH_GIT}") or {}
        if stash_data:
            print(f"[OK] Travail local recupere depuis la reserve ({len(stash_data)} entrees).")
        else:
            print("[ERREUR] Impossible de relire la sauvegarde Git.")

    merged, count_added, count_updated = merge_progress(base_data, stash_data)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"[OK] Fusion terminee : {count_added} nouveaux, {count_updated} mis a jour.")
    print(f"[TOTAL] {len(merged)} appels dans le fichier final.")

    if stash_created:
        run_cmd("git stash drop")
        print("[INFO] Reserve Git nettoyee.")

    if has_unmerged_file() or has_changes or stash_created:
        run_cmd(f'git add "{FILE_PATH_GIT}"')

    print("[INFO] Actualisation de l'outil de verification...")
    try:
        import urllib.request

        request = urllib.request.Request(API_URL, method="POST")
        with urllib.request.urlopen(request, timeout=2) as response:
            if response.status == 200:
                print("[OK] Outil actualise avec succes.")
    except Exception:
        print("[!] L'outil n'etait pas lance, il faudra le demarrer pour voir les changements.")

    print("\n--- Synchronisation reussie ! ---")


if __name__ == "__main__":
    sync()
