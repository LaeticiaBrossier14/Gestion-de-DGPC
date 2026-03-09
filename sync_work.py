import json
import os
import sys
import subprocess
from datetime import datetime

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(PROJECT_ROOT, "verification_tool", "verification_progress.json")
API_URL = "http://localhost:5000/api/reload"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=PROJECT_ROOT)
    return result

def load_json_safe(content):
    try:
        return json.loads(content)
    except Exception as e:
        # Handle UTF-16 from Powershell redirect if content came from file
        try:
             return json.loads(content.decode('utf-16'))
        except:
             return None

def sync():
    print("--- Début de la synchronisation intelligente ---")
    
    # 1. Vérifier l'état git
    status = run_cmd("git status --porcelain")
    has_changes = FILE_PATH.replace(PROJECT_ROOT + os.sep, "") in status.stdout or "verification_tool" in status.stdout
    
    if has_changes:
        print("[INFO] Modifications locales détectées. Sauvegarde temporaire...")
        run_cmd("git stash push -m 'sync-auto-save' verification_tool/verification_progress.json")
    
    # 2. Récupérer le travail de la binôme
    print("[INFO] Récupération du travail de la binôme (git pull)...")
    pull_result = run_cmd("git pull")
    
    if "Conflict" in pull_result.stdout or pull_result.returncode != 0:
        print("[AVERTISSEMENT] Conflit détecté ou erreur de pull. Résolution en cours...")
        # On force le fichier à la version du serveur pour avoir une base propre
        run_cmd(f"git checkout --theirs {FILE_PATH}")
    
    # 3. Charger les deux versions
    # Version du serveur (maintenant locale après pull)
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            base_data = json.load(f)
    except:
        base_data = {}

    # Version sauvegardée dans le stash (si elle existe)
    stash_data = {}
    if has_changes:
        stash_show = subprocess.run(f'git show "stash@{{0}}:{FILE_PATH.replace(PROJECT_ROOT + os.sep, "").replace(os.sep, "/")}"', 
                                    shell=True, capture_output=True, cwd=PROJECT_ROOT)
        if stash_show.returncode == 0:
            try:
                # Try UTF-8 then UTF-16
                content = stash_show.stdout
                try:
                    stash_data = json.loads(content.decode('utf-8'))
                except:
                    stash_data = json.loads(content.decode('utf-16'))
                print(f"[OK] Travail local récupéré depuis la réserve ({len(stash_data)} entrées).")
            except Exception as e:
                print(f"[ERREUR] Impossible de lire la sauvegarde : {e}")
        
    # 4. Fusion intelligente par Timestamp
    merged = base_data.copy()
    count_updated = 0
    count_added = 0
    
    for k, v in stash_data.items():
        if k in merged:
            try:
                t_base = datetime.fromisoformat(merged[k].get('timestamp', '1970-01-01T00:00:00'))
                t_stash = datetime.fromisoformat(v.get('timestamp', '1970-01-01T00:00:00'))
                if t_stash > t_base:
                    merged[k] = v
                    count_updated += 1
            except:
                merged[k] = v # On garde le stash par défaut
        else:
            merged[k] = v
            count_added += 1

    # 5. Enregistrement
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Fusion terminée : {count_added} nouveaux, {count_updated} mis à jour.")
    print(f"[TOTAL] {len(merged)} appels dans le fichier final.")

    # 6. Nettoyage et Notification
    if has_changes:
        run_cmd("git stash drop")
        run_cmd(f"git add {FILE_PATH}")
        print("[INFO] Réserve Git nettoyée.")

    # 7. Actualiser l'outil (si lancé)
    print("[INFO] Actualisation de l'outil de vérification...")
    try:
        import urllib.request
        with urllib.request.urlopen(API_URL, timeout=2) as response:
            if response.status == 200:
                print("[OK] Outil actualisé avec succès !")
    except:
        print("[!] Note : L'outil n'était pas lancé, il faudra le démarrer pour voir les changements.")

    print("\n--- Synchronisation réussie ! ---")

if __name__ == "__main__":
    sync()
