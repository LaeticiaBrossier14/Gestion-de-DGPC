"""
Fusionne les vérifications de Warda (commit edfcf13) dans le fichier actuel.
Le fichier de Warda contient un conflit de fusion Git corrompu — ce script
l'extrait proprement en parsant les blocs JSON valides.
"""
import json
import re
import subprocess
import unicodedata
from pathlib import Path

BASE = Path(__file__).parent
PROGRESS_FILE = BASE / "verification_tool" / "verification_progress.json"
WARDA_RAW = BASE / "verification_tool" / "verification_progress_warda.json"

MOJIBAKE_MARKERS = ("Ã", "Â", "â", "ð", "€", "├", "┬", "ÔÇ", "┼ô")

def repair(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize("NFC", text.replace("\ufeff", ""))
    if not any(m in text for m in MOJIBAKE_MARKERS):
        return text
    for enc in ("cp1252", "latin-1", "cp850"):
        try:
            candidate = text.encode(enc).decode("utf-8")
            if candidate != text:
                text = unicodedata.normalize("NFC", candidate)
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
    return text


def sanitize(obj):
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    if isinstance(obj, str):
        return repair(obj)
    return obj


def load_warda_raw():
    """Lit le fichier de Warda (UTF-16) et retire les marqueurs de conflits Git."""
    with open(WARDA_RAW, "r", encoding="utf-16") as f:
        content = f.read()

    lines = content.splitlines()
    # Retirer les lignes de marqueurs de conflit
    clean_lines = [
        l for l in lines
        if not l.startswith("<<<<<<<")
        and not l.startswith("=======")
        and not l.startswith(">>>>>>>")
    ]
    return "\n".join(clean_lines)


def extract_entries_from_broken_json(content):
    """
    Extrait les entrées valides d'un JSON partiellement corrompu
    en cherchant les blocs "Appelle X.wav": { ... } un par un.
    """
    entries = {}
    # Pattern pour trouver chaque clé d'appel et son bloc JSON
    pattern = re.compile(
        r'"((?:Appelle|appelle)\s[\w\s.]+\.wav)"\s*:\s*(\{)',
        re.IGNORECASE
    )

    for match in pattern.finditer(content):
        key = match.group(1)
        start_brace = match.start(2)
        # Trouver la fermeture du bloc en comptant les accolades
        depth = 0
        i = start_brace
        while i < len(content):
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        
        block_str = content[start_brace:i+1]
        try:
            block = json.loads(block_str)
            entries[key] = block
        except json.JSONDecodeError:
            # Essayer de nettoyer le bloc et réessayer
            try:
                block_clean = re.sub(r'[^\x00-\x7F\u00C0-\u024F\u1E00-\u1EFF]+', '?', block_str)
                block = json.loads(block_clean)
                entries[key] = block
                print(f"  [REPAIRED] {key}")
            except json.JSONDecodeError as e:
                print(f"  [SKIP] Impossible de parser le bloc pour '{key}': {e}")

    return entries


def main():
    print("=" * 60)
    print("  Fusion des vérifications de Warda")
    print("=" * 60)

    # 1. Charger les vérifications actuelles (fichier valide)
    print("\n[1] Chargement du fichier de progression actuel...")
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        current_progress = json.load(f)
    print(f"    → {len(current_progress)} entrées actuelles")

    # 2. Charger et parser le fichier de Warda
    print("\n[2] Lecture du fichier de Warda (avec correction des conflits)...")
    raw_content = load_warda_raw()

    # Essayer d'abord de parser directement
    try:
        warda_progress = json.loads(raw_content)
        print(f"    → JSON valide directement ! {len(warda_progress)} entrées")
    except json.JSONDecodeError as e:
        print(f"    → JSON invalide ({e.msg} à ligne {e.lineno}), extraction bloc par bloc...")
        warda_progress = extract_entries_from_broken_json(raw_content)
        print(f"    → {len(warda_progress)} entrées extraites")

    # 3. Fusionner : les entrées de Warda complètent celles actuelles
    print("\n[3] Fusion en cours...")
    added = 0
    updated = 0
    skipped = 0

    for key, warda_entry in warda_progress.items():
        if key not in current_progress:
            # Nouvelle entrée de Warda → on l'ajoute
            current_progress[key] = sanitize(warda_entry)
            added += 1
        else:
            # L'entrée existe déjà : conserver la plus récente
            current_ts = current_progress[key].get("timestamp", "")
            warda_ts = warda_entry.get("timestamp", "")
            if warda_ts > current_ts:
                current_progress[key] = sanitize(warda_entry)
                updated += 1
            else:
                skipped += 1

    print(f"    → {added} nouvelles entrées ajoutées depuis Warda")
    print(f"    → {updated} entrées mises à jour (Warda plus récente)")
    print(f"    → {skipped} entrées ignorées (déjà à jour)")
    print(f"    → Total final : {len(current_progress)} entrées")

    # 4. Sauvegarder
    print("\n[4] Sauvegarde du fichier fusionné...")
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(current_progress, f, ensure_ascii=False, indent=2)
    print(f"    → Sauvegardé : {PROGRESS_FILE}")

    print("\n✅ Fusion terminée avec succès !")
    print("   Faites POST /api/reload dans l'outil de vérification pour voir les changements.")
    print("=" * 60)


if __name__ == "__main__":
    main()
