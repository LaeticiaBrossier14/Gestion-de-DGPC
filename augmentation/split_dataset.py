import pandas as pd
import os
from sklearn.model_selection import train_test_split

INPUT_CSV = r"g:\AZ\Documents\gestion des appelles telephoniques\dataset\annotations_local.csv"
SYNTHETIC_CSV = r"g:\AZ\Documents\gestion des appelles telephoniques\dataset\synthetic_batch_1.csv"
OUTPUT_DIR = r"g:\AZ\Documents\gestion des appelles telephoniques\dataset\split"

def split_dataset():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # Load real data
    try:
        df_real = pd.read_csv(INPUT_CSV)
        df_real['is_synthetic'] = False
    except FileNotFoundError:
        print(f"Error: {INPUT_CSV} not found.")
        return

    # Load synthetic data if exists
    if os.path.exists(SYNTHETIC_CSV):
        try:
            df_synth = pd.read_csv(SYNTHETIC_CSV)
            # Ensure columns match
            missing_cols = set(df_real.columns) - set(df_synth.columns)
            for col in missing_cols:
                df_synth[col] = None # Fill missing with None/NaN
            
            df_synth['is_synthetic'] = True
            # Reorder columns to match real
            df_synth = df_synth[df_real.columns]
        except Exception as e:
            print(f"Error loading synthetic data: {e}")
            df_synth = pd.DataFrame()
    else:
        df_synth = pd.DataFrame()

    print(f"Real samples: {len(df_real)}")
    print(f"Synthetic samples: {len(df_synth)}")

    # Split Real Data: Train (80%), Val (10%), Test (10%)
    # Using stratify on 'incident_type' if possible
    try:
        train_real, temp_real = train_test_split(df_real, test_size=0.2, stratify=df_real['incident_type'], random_state=42)
        val_real, test_real = train_test_split(temp_real, test_size=0.5, stratify=temp_real['incident_type'], random_state=42)
    except ValueError:
        # Fallback if stratify fails (e.g. single sample classes)
        print("Warning: Stratification failed, using random split.")
        train_real, temp_real = train_test_split(df_real, test_size=0.2, random_state=42)
        val_real, test_real = train_test_split(temp_real, test_size=0.5, random_state=42)

    # Add ALL synthetic data to TRAIN only
    if not df_synth.empty:
        train_final = pd.concat([train_real, df_synth])
    else:
        train_final = train_real

    # Save
    train_final.to_csv(os.path.join(OUTPUT_DIR, "train.csv"), index=False)
    val_real.to_csv(os.path.join(OUTPUT_DIR, "val.csv"), index=False)
    test_real.to_csv(os.path.join(OUTPUT_DIR, "test.csv"), index=False)

    print("\n=== SPLIT SUMMARY ===")
    print(f"Train: {len(train_final)} (Real: {len(train_real)}, Synth: {len(df_synth)})")
    print(f"Val:   {len(val_real)} (Real only)")
    print(f"Test:  {len(test_real)} (Real only)")
    print(f"Saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    split_dataset()
