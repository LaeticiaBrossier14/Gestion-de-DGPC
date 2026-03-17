import json
import re

with open('warda_temp.json', 'r', encoding='utf-16') as f:
    text = f.read()

# On supprime toutes les balises git de conflit éventuelles
text = re.sub(r'<<<<<<<.*?\n', '', text)
text = re.sub(r'=======\n', '', text)
text = re.sub(r'>>>>>>>.*?\n', '', text)

try:
    d = json.loads(text)
except json.JSONDecodeError as e:
    pass

lines = text.split('\n')
audios = ['295', '298', '299', '300']
found = False
for i, line in enumerate(lines):
    if any(m in line for m in audios) and '"Appelle ' in line:
        found = True
        print(f"Trouve {line.strip()}:")
        for j in range(1, 15):
            print("  " + lines[i+j].strip())

if not found:
    print("Aucun des audios manquant n'est dans ce fichier non plus.")
