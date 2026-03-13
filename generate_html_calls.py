import csv
import json
import os

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
target_calls = []
for i in range(108, 150):
    key = f'Appelle {i}.wav'
    if key in calls_data:
        target_calls.append({
            'numero': i,
            'file': key,
            'data': calls_data[key]
        })

# Lire le fichier de progression
with open('verification_tool/verification_progress.json', 'r', encoding='utf-8') as f:
    progress = json.load(f)

# Créer un fichier HTML
html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Appels 108-149 - Transcriptions Originales</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        .call {{ background: white; margin: 20px 0; padding: 15px; border-radius: 8px; border-left: 4px solid #6366f1; }}
        .number {{ font-size: 18px; font-weight: bold; color: #6366f1; }}
        .status {{ display: inline-block; padding: 5px 10px; border-radius: 4px; font-size: 12px; margin-left: 10px; }}
        .status.pending {{ background: #fef08a; color: #854d0e; }}
        .status.verified {{ background: #dcfce7; color: #15803d; }}
        .status.corrected {{ background: #e0e7ff; color: #3730a3; }}
        .info {{ color: #666; font-size: 14px; margin: 10px 0; }}
        .transcription {{ background: #f9fafb; padding: 10px; border-radius: 4px; font-size: 14px; line-height: 1.6; margin-top: 10px; border-left: 2px solid #e5e7eb; }}
        .location {{ color: #0284c7; font-weight: 500; }}
        .type {{ color: #7c3aed; font-weight: 500; }}
    </style>
</head>
<body>
    <h1>📋 Appels 108-149 - Transcriptions Originales</h1>
    <p>Total trouvé: <strong>{len(target_calls)}/42</strong></p>
'''

for call in target_calls:
    numero = call['numero']
    key = call['file']
    data = call['data']
    status = progress.get(key, {}).get('status', 'pending')
    
    status_class = status.lower()
    status_label = {'pending': '⏳ En attente', 'verified': '✅ Vérifié', 'corrected': '✏️ Corrigé'}.get(status, status)
    
    transcription = data.get('Transcription', 'N/A')
    incident_type = data.get('incident_type', '?')
    location = data.get('lieu', '?')
    
    html_content += f'''
    <div class="call">
        <div class="number">[{numero}] {key} <span class="status {status_class}">{status_label}</span></div>
        <div class="info">
            <span class="type">Type: {incident_type}</span> | 
            <span class="location">Lieu: {location}</span>
        </div>
        <div class="transcription">{transcription}</div>
    </div>
'''

html_content += '''
    <hr>
    <h2>📝 Instructions</h2>
    <ol>
        <li>Ouvre: <strong>http://127.0.0.1:5000</strong></li>
        <li>Navigue vers <strong>Appelle 108.wav</strong></li>
        <li>Pour chaque appel:
            <ul>
                <li>🎧 Écoute l'audio</li>
                <li>📄 Lis la transcription affichée (ci-dessus)</li>
                <li>✏️ Clique "Corriger" si tu veux modifier</li>
                <li>✅ Clique "Vérifier" si c'est correct</li>
            </ul>
        </li>
        <li>Les données seront automatiquement sauvegardées</li>
    </ol>
    <footer style="color: #999; margin-top: 40px; font-size: 12px;">
        Généré le 13 mars 2026 - Vérification DGPC
    </footer>
</body>
</html>
'''

# Écrire dans un fichier HTML
with open('verification_tool/calls_108_149.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'✅ Fichier HTML créé: verification_tool/calls_108_149.html')
print(f'📊 Appels trouvés: {len(target_calls)}/42')
print(f'\n1. Ouvre le fichier dans ton navigateur:')
print(f'   file://{os.path.abspath("verification_tool/calls_108_149.html")}')
print(f'\n2. Ou ouvre directement: http://127.0.0.1:5000')
print(f'\n3. Puis re-vérifie chaque appel...')
