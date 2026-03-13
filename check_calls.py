import csv
import json

# Lire CSV
with open('dataset/500annotations_local.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total rows in CSV: {len(rows)}")
print(f"CSV Headers: {list(rows[0].keys())}")

# Chercher les appels entre 108-149
count_108_149 = 0
for i, row in enumerate(rows):
    if 105 <= i <= 115:
        print(f"Row {i}: {row}")
    # Chercher par numéro
    for key in row:
        if row[key] and any(str(n) in str(row[key]) for n in range(108, 150)):
            count_108_149 += 1
            if count_108_149 <= 5:
                print(f"Found in row {i}: {row}")

print(f"\nAppels 108-149 found: {count_108_149}")

# Afficher les progressions trouvées
with open('verification_tool/verification_progress.json', 'r', encoding='utf-8') as f:
    progress = json.load(f)

print(f"\nTotal in progress file: {len(progress)}")
print("Sample progress keys:")
for key in list(progress.keys())[:5]:
    print(f"  - {key}")
