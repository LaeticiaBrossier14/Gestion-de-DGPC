import pandas as pd
import json

def analyze_csv(path):
    # Load dataset
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    print("=== DATASET OVERVIEW ===")
    print(f"Total Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\n")

    # Incident Type Distribution
    print("=== INCIDENT TYPE DISTRIBUTION ===")
    incident_dist = df['incident_type'].value_counts()
    print(incident_dist)
    print("\n")

    # Urgency Distribution
    print("=== URGENCY HUMAN DISTRIBUTION ===")
    if 'urgency_human' in df.columns:
        urgency_dist = df['urgency_human'].value_counts()
        print(urgency_dist)
    else:
        print("Column 'urgency_human' missing")
    print("\n")

    # Location Distribution (Top 10)
    print("=== TOP 10 LOCATIONS ===")
    if 'commune' in df.columns:
        location_dist = df['commune'].value_counts().head(10)
        print(location_dist)
    else:
        print("Column 'commune' missing")
    print("\n")
    
    # Missing Values
    print("=== MISSING VALUES PER COLUMN ===")
    print(df.isnull().sum())
    
    return incident_dist.to_dict()

if __name__ == "__main__":
    analyze_csv(r"g:\AZ\Documents\gestion des appelles telephoniques\dataset\annotations_local.csv")
