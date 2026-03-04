"""
pipeline_menu.py
================
Menu interactif pour gérer le pipeline complet: Transcription → Annotation → Vérification

Usage:
  python pipeline_menu.py
"""

import os
import sys
import subprocess
from pathlib import Path
import time

PROJECT_DIR = Path(__file__).resolve().parent

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def print_menu():
    clear_screen()
    print("""
╔═════════════════════════════════════════════════════════════════╗
║                                                                 ║
║           🛡️  DGPC PIPELINE - Menu Principal                   ║
║           Transcription Appels 506+ → Annotation               ║
║                                                                 ║
╚═════════════════════════════════════════════════════════════════╝

1️⃣  Transcrire avec WHISPER (Rapide, GPU/CPU)
2️⃣  Transcrire avec QWEN3-ASR (Meilleur pour Kabyle, GPU)
3️⃣  Lancer l'OUTIL D'ANNOTATION (Streamlit)
4️⃣  Vérifier le DATASET créé
5️⃣  Exporter / Fusionner datasets
6️⃣  Voir la DOCUMENTATION
0️⃣  Quitter

════════════════════════════════════════════════════════════════════
""")

def transcribe_whisper():
    print("\n🎙️  Transcription WHISPER")
    print("=" * 60)
    
    start = input("\n📍 Appel de départ (défaut: 506): ").strip() or "506"
    end = input("📍 Appel de fin (défaut: dernier): ").strip() or ""
    
    cmd = [sys.executable, "transcribe_from_506.py", "--start", start]
    if end:
        cmd.extend(["--end", end])
    
    auto_launch = input("\n🚀 Lancer l'annotation automatiquement? (o/n - défaut: n): ").lower() == "o"
    if auto_launch:
        cmd.append("--auto-launch")
    
    print("\n[En cours]")
    subprocess.run(cmd, cwd=PROJECT_DIR)
    input("\nAppuyez sur Entrée pour continuer...")

def transcribe_qwen3():
    print("\n🎙️  Transcription QWEN3-ASR")
    print("=" * 60)
    
    start = input("\n📍 Appel de départ (défaut: 506): ").strip() or "506"
    end = input("📍 Appel de fin (défaut: dernier): ").strip() or ""
    cpu = input("💻 Forcer CPU? (o/n - défaut: n): ").lower() == "o"
    
    cmd = [sys.executable, "transcribe_qwen3_from_506.py", "--start", start]
    if end:
        cmd.extend(["--end", end])
    if cpu:
        cmd.append("--use-cpu")
    
    print("\n[En cours] ⏳")
    subprocess.run(cmd, cwd=PROJECT_DIR)
    input("\nAppuyez sur Entrée pour continuer...")

def launch_annotation():
    print("\n📝 Lancement de l'outil d'annotation...")
    print("=" * 60)
    
    annotation_py = PROJECT_DIR / "annotation_app" / "dgpc_annotation_local.py"
    
    if not annotation_py.exists():
        print(f"\n❌ Erreur: {annotation_py} non trouvé")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print("\n✅ Streamlit démarre...")
    print("   📱 URL: http://localhost:8501")
    print("\n   Appuyez sur CTRL+C pour arrêter\n")
    
    try:
        os.chdir(PROJECT_DIR / "annotation_app")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(annotation_py),
            "--logger.level=warning"
        ])
    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt demandé")
    finally:
        os.chdir(PROJECT_DIR)
    
    input("\nAppuyez sur Entrée pour continuer...")

def check_dataset():
    print("\n📊 Vérification du Dataset")
    print("=" * 60)
    
    try:
        import pandas as pd
    except ImportError:
        print("\n[!] Pandas non installé. Installation...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "-q"])
        import pandas as pd
    
    dataset_paths = [
        PROJECT_DIR / "dataset" / "506_onwards_transcriptions.csv",
        PROJECT_DIR / "dataset" / "506_onwards_transcriptions_qwen3.csv",
        PROJECT_DIR / "dataset" / "500annotations_local.csv"
    ]
    
    print("\n📁 Fichiers dataset disponibles:\n")
    
    for ds_path in dataset_paths:
        if ds_path.exists():
            df = pd.read_csv(ds_path, encoding='utf-8', nrows=5)
            print(f"✅ {ds_path.name}")
            print(f"   Lignes: {len(pd.read_csv(ds_path, encoding='utf-8'))}")
            print(f"   Colonnes: {len(df.columns)}")
            print()
        else:
            print(f"❌ {ds_path.name} (non trouvé)\n")
    
    input("\nAppuyez sur Entrée pour continuer...")

def export_merge():
    print("\n📤 Export / Fusion de Datasets")
    print("=" * 60)
    
    print("""
Vous pouvez:
  1. Fusionner Whisper + Qwen3-ASR
  2. Exporter en JSON
  3. Exporter en Excel
  4. Comparer les transcriptions
    """)
    
    print("\n⚠️  Fonction avancée - En développement")
    input("\nAppuyez sur Entrée pour continuer...")

def show_docs():
    print("\n📖 Documentation & Guide")
    print("=" * 60)
    
    doc_file = PROJECT_DIR / "TRANSCRIPTION_GUIDE_506.md"
    
    if doc_file.exists():
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Afficher par pages (80 lignes par page)
            lines = content.split('\n')
            for i in range(0, len(lines), 40):
                print('\n'.join(lines[i:i+40]))
                if i + 40 < len(lines):
                    input("\n[Appuyez sur Entrée pour continuer...]")
    else:
        print(f"\n❌ Documentation non trouvée: {doc_file}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def main_loop():
    while True:
        print_menu()
        choice = input("👉 Choisissez une option (0-6): ").strip()
        
        if choice == "1":
            transcribe_whisper()
        elif choice == "2":
            transcribe_qwen3()
        elif choice == "3":
            launch_annotation()
        elif choice == "4":
            check_dataset()
        elif choice == "5":
            export_merge()
        elif choice == "6":
            show_docs()
        elif choice == "0":
            print("\n👋 Au revoir!\n")
            sys.exit(0)
        else:
            print("\n❌ Option invalide. Reessayez.")
            time.sleep(1)

if __name__ == "__main__":
    main_loop()
