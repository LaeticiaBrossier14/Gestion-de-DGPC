
import json
import os
import urllib.request as request

def deep_fix(obj):
    if isinstance(obj, dict):
        return {k: deep_fix(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_fix(x) for x in obj]
    elif isinstance(obj, str):
        # Try to fix mojibake
        try:
            # We assume the string contains CP850 chars that were meant to be UTF-8 bytes
            # We encode to CP850 to get those bytes, then decode as UTF-8
            candidate = obj.encode('cp850').decode('utf-8')
            # If it changed and looks reasonable (doesn't contain mojibake patterns anymore)
            if candidate != obj:
                return candidate
        except:
            pass
        
        # Another common case: interpreted as Latin-1
        try:
            candidate = obj.encode('latin-1').decode('utf-8')
            if candidate != obj:
                return candidate
        except:
            pass
            
        return obj
    return obj

def repair_json(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return False
            
    fixed_data = deep_fix(data)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=2)
    return True

if __name__ == "__main__":
    target = r'f:\dgpc_pipeline_ready\verification_tool\verification_progress.json'
    if repair_json(target):
        print("Success: Deep repair of verification_progress.json complete.")
        try:
           request.urlopen("http://localhost:5000/api/reload", data=b'', timeout=2)
           print("Success: App reloaded.")
        except:
           print("Info: App server not running to reload.")
    else:
        print("Error: Could not repair JSON.")
