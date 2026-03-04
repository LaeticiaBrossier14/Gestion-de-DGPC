"""
sync_csv_json.py
================
Synchronise et valide la cohérence entre CSV et JSON du dataset 506+

Workflow:
  1. Charge CSV transcriptions
  2. Génère JSON cohérent
  3. Valide intégrité
  4. Crée backups
  5. Exporte en formats multiples
"""

import os
import sys
import csv
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import OrderedDict

PROJECT_DIR = Path(__file__).resolve().parent
DATASET_DIR = PROJECT_DIR / "dataset"

# Fichiers
CSV_FILE = DATASET_DIR / "506_onwards_transcriptions.csv"
JSON_FILE = DATASET_DIR / "506_onwards_transcriptions.json"
METADATA_FILE = DATASET_DIR / "506_onwards_metadata.json"
BACKUP_DIR = DATASET_DIR / ".backups"

# Colonnes définies
COLUMNS = [
    "ID", "File", "Transcription", "incident_type", "injury_severity",
    "victims_count", "fire_present", "trapped_persons", "weapons_involved",
    "hazmat_involved", "intent", "urgency_human", "daira", "commune",
    "lieu", "location_description", "summary", "notes_cot", "_annotation_status"
]


def create_backup():
    """Crée un backup des fichiers actuels"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if CSV_FILE.exists():
        backup_csv = BACKUP_DIR / f"506_onwards_{timestamp}.csv.bak"
        import shutil
        shutil.copy(CSV_FILE, backup_csv)
        print(f"✅ Backup CSV: {backup_csv}")
    
    if JSON_FILE.exists():
        backup_json = BACKUP_DIR / f"506_onwards_{timestamp}.json.bak"
        import shutil
        shutil.copy(JSON_FILE, backup_json)
        print(f"✅ Backup JSON: {backup_json}")


def load_csv():
    """Charge le CSV"""
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        print(f"✅ CSV chargé: {len(df)} lignes, {len(df.columns)} colonnes")
        return df
    except FileNotFoundError:
        print(f"❌ CSV non trouvé: {CSV_FILE}")
        return None


def validate_csv(df):
    """Valide l'intégrité du CSV"""
    print("\n🔍 Validation CSV:")
    
    issues = []
    
    # Vérifier ID uniques
    if df["ID"].duplicated().any():
        dups = df[df["ID"].duplicated()]["ID"].unique()
        issues.append(f"⚠️  IDs dupliquées: {len(dups)}")
    else:
        print(f"  ✅ IDs uniques: {len(df)}")
    
    # Vérifier fichiers audio existent
    audio_missing = 0
    audio_dir = PROJECT_DIR / "audio_processed"
    for _, row in df.iterrows():
        audio_file = audio_dir / row["File"]
        if not audio_file.exists():
            audio_missing += 1
    
    if audio_missing > 0:
        issues.append(f"⚠️  Fichiers audio manquants: {audio_missing}")
    else:
        print(f"  ✅ Tous fichiers audio présents: {len(df)}")
    
    # Vérifier Transcriptions non vides
    empty_trans = df["Transcription"].isna().sum() + (df["Transcription"] == "").sum()
    if empty_trans > 0:
        issues.append(f"⚠️  Transcriptions vides: {empty_trans}")
    else:
        print(f"  ✅ Transcriptions présentes: {len(df)}")
    
    # Vérifier colonnes
    missing_cols = set(COLUMNS) - set(df.columns)
    if missing_cols:
        issues.append(f"⚠️  Colonnes manquantes: {missing_cols}")
    else:
        print(f"  ✅ Toutes colonnes présentes: {len(COLUMNS)}")
    
    if issues:
        print("\n⚠️  Problèmes détectés:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ Validation réussie - Aucun problème!")
    
    return len(issues) == 0


def csv_to_json(df):
    """Convertit CSV en JSON structuré"""
    print("\n📝 Conversion CSV → JSON:")
    
    records = []
    for idx, row in df.iterrows():
        record = OrderedDict()
        
        # Champs principaux
        record["id"] = row.get("ID", f"CALL_{str(idx).zfill(4)}")
        record["file"] = row.get("File", "")
        record["transcription"] = row.get("Transcription", "")
        record["timestamp"] = datetime.now().isoformat()
        
        # Annotation
        record["annotation"] = {
            "incident_type": row.get("incident_type", ""),
            "injury_severity": row.get("injury_severity", ""),
            "victims_count": row.get("victims_count", ""),
            "fire_present": row.get("fire_present", ""),
            "trapped_persons": row.get("trapped_persons", ""),
            "weapons_involved": row.get("weapons_involved", ""),
            "hazmat_involved": row.get("hazmat_involved", ""),
            "intent": row.get("intent", ""),
            "urgency": row.get("urgency_human", ""),
        }
        
        # Location
        record["location"] = {
            "daira": row.get("daira", ""),
            "commune": row.get("commune", ""),
            "lieu": row.get("lieu", ""),
            "description": row.get("location_description", ""),
        }
        
        # Metadata
        record["metadata"] = {
            "summary": row.get("summary", ""),
            "notes_cot": row.get("notes_cot", ""),
            "status": row.get("_annotation_status", "pending"),
        }
        
        records.append(record)
    
    json_data = {
        "version": "1.0",
        "generated": datetime.now().isoformat(),
        "total_calls": len(records),
        "data": records
    }
    
    # Écrire JSON
    try:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON créé: {JSON_FILE}")
        print(f"   Lignes: {len(records)}")
        return True
    except Exception as e:
        print(f"❌ Erreur création JSON: {e}")
        return False


def create_metadata():
    """Crée un fichier de metadata pour synchronisation"""
    print("\n📊 Création metadata:")
    
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        
        metadata = {
            "generated": datetime.now().isoformat(),
            "version": "1.0",
            "statistics": {
                "total_calls": len(df),
                "annotated": len(df[df["_annotation_status"].fillna("") == "annotated"]) if "_annotation_status" in df.columns else 0,
                "pending": len(df[df["_annotation_status"].fillna("") == "pending"]) if "_annotation_status" in df.columns else len(df),
            },
            "file_checksums": {
                "csv": f"{CSV_FILE.stat().st_mtime}",
                "json": f"{JSON_FILE.stat().st_mtime}" if JSON_FILE.exists() else None,
            }
        }
        
        # Incident types distribution
        if "incident_type" in df.columns:
            incident_counts = df["incident_type"].value_counts().to_dict()
            metadata["incident_types"] = incident_counts
        
        # Urgency distribution
        if "urgency_human" in df.columns:
            urgency_counts = df["urgency_human"].value_counts().to_dict()
            metadata["urgency"] = urgency_counts
        
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Metadata créée: {METADATA_FILE}")
        print(f"   Total: {metadata['statistics']['total_calls']}")
        print(f"   Annotés: {metadata['statistics']['annotated']}")
        print(f"   En attente: {metadata['statistics']['pending']}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur création metadata: {e}")
        return False


def export_formats():
    """Exporte en formats multiples"""
    print("\n📤 Export formats multiples:")
    
    try:
        df = pd.read_csv(CSV_FILE, encoding='utf-8')
        
        # Parquet (compressé)
        parquet_file = DATASET_DIR / "506_onwards_transcriptions.parquet"
        df.to_parquet(parquet_file, compression='gzip')
        print(f"✅ Parquet: {parquet_file}")
        
        # Excel
        excel_file = DATASET_DIR / "506_onwards_transcriptions.xlsx"
        df.to_excel(excel_file, index=False)
        print(f"✅ Excel: {excel_file}")
        
        # JSONL (line delimited)
        jsonl_file = DATASET_DIR / "506_onwards_transcriptions.jsonl"
        with open(jsonl_file, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                f.write(json.dumps(row.to_dict(), ensure_ascii=False) + '\n')
        print(f"✅ JSONL: {jsonl_file}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur export: {e}")
        return False


def sync_json_to_csv():
    """Synchronise les mises à jour JSON vers CSV (si JSON plus à jour)"""
    print("\n🔄 Synchronisation JSON → CSV:")
    
    if not JSON_FILE.exists():
        print("❌ JSON non trouvé")
        return False
    
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        records = []
        for item in json_data.get("data", []):
            record = {
                "ID": item.get("id", ""),
                "File": item.get("file", ""),
                "Transcription": item.get("transcription", ""),
                "incident_type": item.get("annotation", {}).get("incident_type", ""),
                "injury_severity": item.get("annotation", {}).get("injury_severity", ""),
                "victims_count": item.get("annotation", {}).get("victims_count", ""),
                "fire_present": item.get("annotation", {}).get("fire_present", ""),
                "trapped_persons": item.get("annotation", {}).get("trapped_persons", ""),
                "weapons_involved": item.get("annotation", {}).get("weapons_involved", ""),
                "hazmat_involved": item.get("annotation", {}).get("hazmat_involved", ""),
                "intent": item.get("annotation", {}).get("intent", ""),
                "urgency_human": item.get("annotation", {}).get("urgency", ""),
                "daira": item.get("location", {}).get("daira", ""),
                "commune": item.get("location", {}).get("commune", ""),
                "lieu": item.get("location", {}).get("lieu", ""),
                "location_description": item.get("location", {}).get("description", ""),
                "summary": item.get("metadata", {}).get("summary", ""),
                "notes_cot": item.get("metadata", {}).get("notes_cot", ""),
                "_annotation_status": item.get("metadata", {}).get("status", "pending"),
            }
            records.append(record)
        
        # Écrire CSV
        synced_csv = DATASET_DIR / "506_onwards_transcriptions_synced.csv"
        with open(synced_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(records)
        
        print(f"✅ CSV synchronisé: {synced_csv}")
        return True
    except Exception as e:
        print(f"❌ Erreur sync: {e}")
        return False


def main():
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           Synchronisation CSV ↔ JSON (506+)              ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Créer backup
    create_backup()
    
    # Charger et valider CSV
    df = load_csv()
    if df is None:
        print("❌ Impossible de continuer sans CSV")
        sys.exit(1)
    
    # Valider
    validate_csv(df)
    
    # Convertir CSV → JSON
    csv_to_json(df)
    
    # Créer metadata
    create_metadata()
    
    # Export formats multiples
    export_formats()
    
    # Sync JSON → CSV (inverse)
    sync_json_to_csv()
    
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║              ✅ SYNCHRONISATION TERMINÉE                 ║
╚═══════════════════════════════════════════════════════════╝

Fichiers créés/mis à jour:
  ✓ {CSV_FILE.name}
  ✓ {JSON_FILE.name}
  ✓ {METADATA_FILE.name}
  ✓ Parquet, Excel, JSONL

Prêt pour:
  → Annotation IA
  → Analyse statistique
  → ML Training
""")


if __name__ == "__main__":
    main()
