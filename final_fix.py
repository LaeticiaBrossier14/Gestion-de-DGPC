
import json
import os
import urllib.request as request

def fix_string(s):
    if not isinstance(s, str): return s
    # Common mojibake: UTF-8 bytes read as CP850
    try:
        # Step 1: try CP850 roundtrip
        b = s.encode('cp850')
        fixed = b.decode('utf-8')
        if fixed != s: return fixed
    except:
        pass
    
    # Step 2: try Latin-1 roundtrip
    try:
        b = s.encode('latin-1')
        fixed = b.decode('utf-8')
        if fixed != s: return fixed
    except:
        pass
    
    # Step 3: Hard replacements for known issues that failed roundtrip
    repls = {
        "├«": "ç",
        "├¬": "ê",
        "├ù": "ù",
        "├ç": "ç",
        "├Ö": "Ö",
        "├¿": "è",
        "├á": "à",
        "├®": "é",
        "├»": "ï",
        "├┤": "ô",
        "├╗": "û",
        "├ó": "â",
        "├î": "î",
        "├í": "á",
        "├ö": "ö",
        "├»": "ï",
        "├║": "ú",
        "├▒": "ñ",
        "├ƒ": "ß",
        "├ñ": "ä",
        "ÔÇÖ": "’",
        "ÔÇô": "–",
        "ÔÇª": "…",
        "ÔÇ£": "“",
        "ÔÇ\u009d": "”"
    }
    for k, v in repls.items():
        if k in s:
            s = s.replace(k, v)
    
    return s

def deep_fix(obj):
    if isinstance(obj, dict):
        return {k: deep_fix(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_fix(x) for x in obj]
    elif isinstance(obj, str):
        return fix_string(obj)
    return obj

def repair_json(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    fixed_data = deep_fix(data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    target = r'f:\dgpc_pipeline_ready\verification_tool\verification_progress.json'
    repair_json(target)
    print("Success: Final repair complete.")
    try:
        request.urlopen("http://localhost:5000/api/reload", data=b'', timeout=2)
    except:
        pass
