import json

# Lire le fichier de progression
with open('verification_progress.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Compter les transcriptions corrigées
corrected_count = 0
corrected_calls = []

for call_id, entry in data.items():
    if entry.get('status') == 'corrected' and entry.get('corrected_transcription'):
        corrected_count += 1
        corrected_calls.append({
            'id': call_id,
            'transcription_length': len(entry.get('corrected_transcription', ''))
        })

print('Total transcriptions corrigees:', corrected_count)
print('\nPremiers appels corriges:')
for call in sorted(corrected_calls, key=lambda x: x['id'])[:10]:
    print('  -', call['id'], ':', call['transcription_length'], 'caracteres')

# Afficher les stats globales
print('\nStatistiques globales:')
stats = {}
for call_id, entry in data.items():
    status = entry.get('status', 'unknown')
    stats[status] = stats.get(status, 0) + 1

for status, count in sorted(stats.items()):
    print('  ', status, ':', count)

# Afficher les appels d'aujourd'hui
print('\n=== APPELS D\'AUJOURD\'HUI (2026-03-13) ===')
today_appels = []
for call_id, entry in data.items():
    if entry.get('timestamp', '').startswith('2026-03-13'):
        today_appels.append({
            'id': call_id,
            'status': entry.get('status'),
            'has_transcription': bool(entry.get('corrected_transcription'))
        })

print('Nombre d\'appels traites aujourd\'hui:', len(today_appels))
for appel in today_appels:
    print('  -', appel['id'], ':', appel['status'], '| Transcription:', 'OUI' if appel['has_transcription'] else 'NON')
