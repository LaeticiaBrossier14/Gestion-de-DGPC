"""
Extract synthetic scenarios from JSONL files and generate JavaScript for the voice collection app.
"""
import json, re, os, glob

# Lire depuis le dossier organisé (sous-dossiers par type d'incident)
_ORGANIZED_DIR = os.path.join(os.path.dirname(__file__), '../ml_pipeline/dataset/organized')
JSONL_FILES = sorted(glob.glob(os.path.join(_ORGANIZED_DIR, '*/scenarios.jsonl')))

INCIDENT_EMOJIS = {
    'accident_vehicular': '🚗 Accident véhiculaire',
    'accident_pedestrian': '🚶 Accident piéton',
    'fire_building': '🏠 Incendie bâtiment',
    'fire_forest': '🌲 Feu de forêt',
    'fire_vehicle': '🔥 Véhicule en feu',
    'medical_emergency': '🩺 Urgence médicale',
    'drowning': '🌊 Noyade',
    'assault_violence': '👊 Agression/Violence',
    'theft_robbery': '🚨 Vol/Cambriolage',
    'natural_disaster': '⛰️ Catastrophe naturelle',
    'hazmat': '☣️ Matières dangereuses',
    'lost_person': '🔍 Personne disparue',
    'structural_collapse': '🏗️ Effondrement',
    'unknown': '❓ Fausse alerte',
    'other': '📝 Autre',
}

def parse_turns(text):
    """Parse transcription into list of {role, text} turns."""
    turns = []
    
    # Check for labeled turns (caller: / operator: / s1: / s2: / agent: / appelant:)
    if re.search(r'(?:caller|operator|s1|s2|agent|appelant)\s*:', text, re.IGNORECASE):
        parts = re.split(r'(caller|operator|s1|s2|agent|appelant)\s*:', text, flags=re.IGNORECASE)
        
        s1_role, s2_role = None, None
        
        for i in range(1, len(parts), 2):
            label = parts[i].lower()
            t = parts[i+1].strip() if i+1 < len(parts) else ''
            
            if label in ('caller', 'appelant'):
                role = 'caller'
            elif label in ('operator', 'agent'):
                role = 'operator'
            else: # s1 or s2
                if label == 's1' and s1_role is None:
                    t_lower = t.lower()
                    if ('istima3' in t_lower or 'm3akoum' in t_lower or ('7imaya' in t_lower and '?' not in t_lower and not t_lower.startswith('allo') and not t_lower.startswith('salam'))):
                        s1_role, s2_role = 'operator', 'caller'
                    else:
                        s1_role, s2_role = 'caller', 'operator'
                
                role = s1_role if label == 's1' else s2_role
                if role is None: role = 'caller' # fallback
            
            if t:
                turns.append({'role': role, 'text': t})
                
    # dash_turns format (— or -)
    elif text.lstrip().startswith(('-', '—')):
        parts = re.split(r'\s*(?:—\s*|(?<!\w)- )', text)
        parts = [p.strip() for p in parts if p.strip()]
        
        first_is_operator = False
        if len(parts) >= 2:
            t0 = parts[0].lower()
            t1 = parts[1].lower()
            
            def is_op_turn(t):
                return 'istima3' in t or 'm3akoum' in t or ('l\'7imaya' in t and '?' not in t and not t.startswith('allo') and not t.startswith('salam'))
            
            if is_op_turn(t0) and not is_op_turn(t1):
                first_is_operator = True
            elif not is_op_turn(t0) and is_op_turn(t1):
                first_is_operator = False
            else:
                first_is_operator = False # default
                
        for i, t in enumerate(parts):
            role = 'operator' if (i % 2 == 0) == first_is_operator else 'caller'
            turns.append({'role': role, 'text': t})
            
    return turns

def main():
    scenarios = []
    seen = set()
    
    for fp in JSONL_FILES:
        path = os.path.join(os.path.dirname(__file__), fp)
        if not os.path.exists(path):
            print(f"⚠️ Fichier non trouvé: {fp}")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                sid = d.get('id', '')
                if sid in seen:
                    continue
                seen.add(sid)
                
                t = d.get('transcription', '')
                inc = d.get('labels', {}).get('incident_type', 'unknown')
                loc = d.get('labels', {}).get('location', 'unknown')
                
                turns = parse_turns(t)
                if turns and len(turns) >= 2:
                    scenarios.append({
                        'id': sid,
                        'incident': inc,
                        'location': loc,
                        'type_label': INCIDENT_EMOJIS.get(inc, f'❓ {inc}'),
                        'turns': turns,
                    })
    
    # Stats
    types = {}
    for s in scenarios:
        t = s['incident']
        types[t] = types.get(t, 0) + 1
    
    print(f"✅ {len(scenarios)} scénarios extraits")
    for t, n in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {n}")
    total_turns = sum(len(s['turns']) for s in scenarios)
    print(f"  Total tours de parole: {total_turns}")
    
    # Generate JS
    js_lines = ['const SCENARIOS = [']
    for s in scenarios:
        js_lines.append('  {')
        js_lines.append(f'    type: {json.dumps(s["type_label"], ensure_ascii=False)},')
        js_lines.append(f'    incident: {json.dumps(s["incident"], ensure_ascii=False)},')
        js_lines.append(f'    location: {json.dumps(s["location"], ensure_ascii=False)},')
        js_lines.append(f'    id: {json.dumps(s["id"], ensure_ascii=False)},')
        js_lines.append('    turns: [')
        for turn in s['turns']:
            text_json = json.dumps(turn['text'], ensure_ascii=False)
            js_lines.append(f'      {{ role: "{turn["role"]}", text: {text_json} }},')
        js_lines.append('    ]')
        js_lines.append('  },')
    js_lines.append('];')
    
    js_output = '\n'.join(js_lines)
    
    out_path = os.path.join(os.path.dirname(__file__), 'scenarios_data.js')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(js_output)
    
    print(f"\n📁 Fichier JS généré: {out_path}")
    print(f"   Taille: {len(js_output)} caractères")

if __name__ == '__main__':
    main()
