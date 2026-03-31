import pandas as pd

df = pd.read_csv('f:/dgpc_pipeline_ready/TALN/TALN.csv')
chars = set(''.join(df['Transcription'].dropna().astype(str)))
non_ascii_chars = [c for c in chars if ord(c) > 127]

with open('f:/dgpc_pipeline_ready/TALN/non_ascii_chars.txt', 'w', encoding='utf-8') as f:
    f.write(".\n".join(sorted(non_ascii_chars)))
