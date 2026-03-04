import pandas as pd
df = pd.read_csv("dataset/400annotations_local.csv")
print(f"Lignes totales: {len(df)}")
print("\n--- INTENT ---")
print(df['intent'].value_counts(dropna=False))
print("\n--- URGENCY ---")
print(df['urgency_human'].value_counts(dropna=False))
print("\n--- INCIDENT TYPE ---")
print(df['incident_type'].value_counts(dropna=False))
