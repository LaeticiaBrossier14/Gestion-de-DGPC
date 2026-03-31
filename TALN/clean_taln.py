import pandas as pd

def clean_text(text):
    if not isinstance(text, str):
        return text
    
    # 1. Réductions globales des doubles lettres (sauf 'tt' et 'dd' qu'on gère à part)
    doubles = [
        'xx', 'qq', 'čč', 'mm', 'ww', 'ss', 'kk', 'ff', 'll', 'nn', 
        'ğğ', 'gg', 'ṛṛ', 'rr', 'bb', 'ẓẓ', 'ṭṭ', 'zz', 'jj', 'cc', 'ẓz'
    ]
    
    # Pour chaque double lettre, on remplace toutes les variantes de majuscules/minuscules
    for d in doubles:
        d1, d2 = d[0], d[1]
        text = text.replace(d1.lower() + d2.lower(), d1.lower())
        text = text.replace(d1.upper() + d2.lower(), d1.upper())
        text = text.replace(d1.lower() + d2.upper(), d1.lower())
        text = text.replace(d1.upper() + d2.upper(), d1.upper())

    i = 0
    res = []
    while i < len(text):
        # 2. Gestion spécifique de 'tt' et 'dd'
        if i + 1 < len(text) and text[i:i+2].lower() == 'tt':
            res.append(text[i:i+2]) # 'tt' reste tel quel
            i += 2
        elif i + 1 < len(text) and text[i:i+2].lower() == 'dd':
            # 'dd' devient un simple 'd'
            res.append('D' if text[i].isupper() else 'd')
            i += 2
        else:
            # 3. Mapping caractère par caractère
            char = text[i]
            mapping = {
                'Č': 'Tch', 'č': 'tch',
                'C': 'Ch', 'c': 'ch',
                'Ğ': 'Dj', 'ğ': 'dj', 'Ǧ': 'Dj', 'ǧ': 'dj',
                'Ɣ': 'Gh', 'ɣ': 'gh',
                'X': 'Kh', 'x': 'kh',
                'Ɛ': '3', 'ɛ': '3', 'ԑ': '3', 'ε': '3',
                'Ḥ': '7', 'ḥ': '7',
                'Ḍ': 'Dh', 'ḍ': 'dh',   # ḍ devient dh
                'Ṭ': 'T', 'ṭ': 't',
                'Ṣ': 'S', 'ṣ': 's',
                'Ẓ': 'Z', 'ẓ': 'z',
                'Ṛ': 'R', 'ṛ': 'r',
                'Q': '9', 'q': '9',
                'U': 'Ou', 'u': 'ou',
                'Ə': 'E', 'ə': 'e',
                'T': 'Th', 't': 'th',   # t devient th
                'D': 'Dh', 'd': 'dh'    # d devient dh
            }
            res.append(mapping.get(char, char))
            i += 1
            
    return ''.join(res)

# Chargement du fichier
df = pd.read_csv('f:/dgpc_pipeline_ready/TALN/TALN.csv')

# Application du nettoyage
df['Transcription'] = df['Transcription'].apply(clean_text)

# Sauvegarde
output_path = 'f:/dgpc_pipeline_ready/TALN/TALN_cleaned.csv'
df.to_csv(output_path, index=False)

print(f"Nettoyage termine avec le nouveau tableau ! Les donnees sont sauvegardees dans : {output_path}")
