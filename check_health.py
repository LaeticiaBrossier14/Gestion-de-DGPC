"""
check_health.py
===============
Script de vérification (health check) pour le pipeline.

Vérifie:
- ✅ Python version
- ✅ Dépendances installées
- ✅ Fichiers audio présents
- ✅ Dataset accessible
- ✅ GPU disponibilité
- ✅ Dossiers créés

Usage:
  python check_health.py
"""

import sys
import subprocess
from pathlib import Path
import os

PROJECT_DIR = Path(__file__).resolve().parent
AUDIO_DIR = PROJECT_DIR / "audio_processed"
DATASET_DIR = PROJECT_DIR / "dataset"

REQUIRED = [
    "numpy", "pandas", "pydub", "streamlit",
    "google.generativeai", "dotenv"
]

OPTIONAL = ["whisper", "qwen_asr", "torch"]

def check_python_version():
    """Vérifier Python >= 3.8"""
    version = sys.version_info
    status = "✅" if version >= (3, 8) else "❌"
    print(f"{status} Python: {version.major}.{version.minor}.{version.micro}")
    return version >= (3, 8)

def check_module(module_name):
    """Vérifier si un module est installé"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def check_dependencies():
    """Vérifier les dépendances"""
    print("\n📦 Dépendances Requises:")
    all_ok = True
    for mod in REQUIRED:
        if check_module(mod):
            print(f"  ✅ {mod}")
        else:
            print(f"  ❌ {mod} (manquant)")
            all_ok = False
    
    print("\n📦 Dépendances Optionnelles:")
    for mod in OPTIONAL:
        if check_module(mod):
            print(f"  ✅ {mod}")
        else:
            print(f"  ⚠️  {mod} (non installé)")
    
    return all_ok

def check_gpu():
    """Vérifier disponibilité GPU"""
    try:
        import torch
        has_gpu = torch.cuda.is_available()
        if has_gpu:
            gpu_name = torch.cuda.get_device_name(0)
            print(f"  ✅ GPU: {gpu_name}")
        else:
            print(f"  ℹ️  GPU non disponible (CPU mode)")
        return has_gpu
    except Exception as e:
        print(f"  ⚠️  PyTorch non installé: {str(e)[:50]}")
        return False

def check_files():
    """Vérifier existence des fichiers"""
    print("\n📁 Fichiers:")
    
    # Vérifier dossiers
    for folder, name in [(AUDIO_DIR, "Audio"), (DATASET_DIR, "Dataset")]:
        if folder.exists():
            print(f"  ✅ {name}: {folder}")
        else:
            print(f"  ❌ {name} n'existe pas: {folder}")
    
    # Vérifier fichiers audio
    audio_files = list(AUDIO_DIR.glob("appelle *.wav")) + list(AUDIO_DIR.glob("Appelle *.wav"))
    if audio_files:
        print(f"  ✅ Fichiers audio: {len(audio_files)} trouvés")
        # Vérifier si 506 existe
        has_506 = any("506" in f.name for f in audio_files)
        status_506 = "✅" if has_506 else "❌"
        print(f"    {status_506} Appelle 506.wav: {'Trouvé' if has_506 else 'Manquant'}")
    else:
        print(f"  ❌ Aucun fichier audio trouvé")
    
    # Vérifier dataset
    if DATASET_DIR.exists():
        csv_files = list(DATASET_DIR.glob("*.csv"))
        if csv_files:
            print(f"  ✅ Fichiers CSV: {len(csv_files)}")
            for csv_file in csv_files[:5]:
                print(f"    - {csv_file.name}")
        else:
            print(f"  ℹ️  Aucun CSV encore (à créer après transcription)")

def check_scripts():
    """Vérifier existence des scripts"""
    print("\n🐍 Scripts Python:")
    scripts = [
        "transcribe_from_506.py",
        "transcribe_qwen3_from_506.py",
        "pipeline_menu.py",
        "check_health.py"
    ]
    for script in scripts:
        script_path = PROJECT_DIR / script
        if script_path.exists():
            print(f"  ✅ {script}")
        else:
            print(f"  ❌ {script} (manquant)")

def check_batch_files():
    """Vérifier existence des batch files"""
    print("\n🟡 Fichiers Batch:")
    batches = [
        "LancerMenu.bat",
        "run_transcription_506.bat",
        "run_qwen3_transcription_506.bat"
    ]
    for batch in batches:
        batch_path = PROJECT_DIR / batch
        if batch_path.exists():
            print(f"  ✅ {batch}")
        else:
            print(f"  ❌ {batch} (manquant)")

def print_recommendations():
    """Afficher les recommandations"""
    print("\n💡 Recommandations:")
    
    has_gpu = False
    try:
        import torch
        has_gpu = torch.cuda.is_available()
    except:
        pass
    
    if not has_gpu:
        print("  • GPU non détecté → Transcription sera lente")
        print("    Installer: CUDA + cuDNN OR utiliser --use-cpu")
    
    if not check_module("whisper"):
        print("  • Whisper non installé → Installer pour transcription rapide")
        print("    pip install openai-whisper")
    
    if not check_module("qwen_asr"):
        print("  • Qwen3-ASR non installé → Installer pour Kabyle optimisé")
        print("    pip install qwen-asr")
    
    audio_files = list(AUDIO_DIR.glob("Appelle *.wav")) + list(AUDIO_DIR.glob("appelle *.wav"))
    if len(audio_files) < 10:
        print(f"  • Peu de fichiers audio ({len(audio_files)}) → Vérifier audio_processed/")
    
    print("\n🚀 Prêt à lancer:")
    print("  python pipeline_menu.py")
    print("  OU")
    print("  Double-cliquer: LancerMenu.bat")

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║           ✅ HEALTH CHECK - Pipeline DGPC 506+           ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Vérifications
    check_python_version()
    check_dependencies()
    check_gpu()
    check_files()
    check_scripts()
    check_batch_files()
    print_recommendations()
    
    print("\n" + "=" * 60)
    print("✅ Vérification terminée!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
    input("Appuyez sur Entrée pour fermer...")
