
import json
import os
import urllib.request as request

REPLACEMENTS = {
    "├®": "é",
    "├á": "à",
    "├¿": "è",
    "├┤": "ô",
    "├»": "ï",
    "├¬": "ê",
    "├ù": "ù",
    "├ç": "ç",
    "ÔÇÖ": "’",
    "n?Test": "n'est",
    "d?Tinformations": "d'informations",
    "n?est": "n'est",
    "l?Tappel": "l'appel",
    "d?Tappelant": "d'appelant",
    "l?-est": "l'est",
    "l?Tincident": "l'incident"
}

def repair_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    modified = False
    for mangled, fixed in REPLACEMENTS.items():
        if mangled in content:
            content = content.replace(mangled, fixed)
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    target = r'f:\dgpc_pipeline_ready\verification_tool\verification_progress.json'
    if repair_file(target):
        print("Success: Fixed mangled characters in verification_progress.json")
        try:
           request.urlopen("http://localhost:5000/api/reload", data=b'', timeout=2)
           print("Success: App reloaded.")
        except:
           print("Info: App server not running to reload, but file saved.")
    else:
        print("Done: Nothing found to repair.")
