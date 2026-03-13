import csv
import json

# Lire le CSV original
csv_file = 'dataset/500annotations_local.csv'
calls_data = {}

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        file_name = row.get('File', '').strip()
        if file_name:
            calls_data[file_name] = row

# Filtrer les appels 108-149
target_calls = {}
for i in range(108, 150):
    key = f'Appelle {i}.wav'
    if key in calls_data:
        target_calls[key] = calls_data[key]

print('='*80)
print(f'APPELS 108-149 - TRANSCRIPTIONS ORIGINALES DU CSV')
print(f'Total trouvé: {len(target_calls)}/42')
print('='*80)

# Lire le fichier de progression pour voir le statut
with open('verification_tool/verification_progress.json', 'r', encoding='utf-8') as f:
    progress = json.load(f)

# Afficher chaque appel
for i in range(108, 150):
    key = f'Appelle {i}.wav'
    if key in target_calls:
        row = target_calls[key]
        status = progress.get(key, {}).get('status', 'pending')
        
        print(f'\n{"="*80}')
        print(f'[{i}] {key}')
        print(f'    Status: {status.upper()}')
        print(f'    Incident Type: {row.get("incident_type", "?")}')
        print(f'    Location: {row.get("lieu", "?")}')
        print(f'-'*80)
        print(f'TRANSCRIPTION ORIGINALE:')
        print(f'{row.get("Transcription", "N/A")}')
        print(f'-'*80)
    else:
        print(f'\n[{i}] Appelle {i}.wav - INTROUVABLE')

print(f'\n{"="*80}')
print('INSTRUCTIONS POUR RE-VÉRIFIER:')
print('1. Ouvre: http://127.0.0.1:5000')
print('2. Utilise la liste à gauche pour naviguer vers Appelle 108.wav')
print('3. Écoute l\'audio + lis la transcription')
print('4. Clique "Corriger" SI tu veux modifier la transcription')
print('5. Clique "Vérifier" si c\'est correct')
print('6. Les données seront automatiquement sauvegardées')
print('='*80)
