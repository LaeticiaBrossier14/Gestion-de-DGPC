"""
# Pipeline de Découpage ASR (Forced Alignment) - SOTA 2026
# Rôle : 
# 1. Lire les longs audios (.wav) et les transcriptions (.csv).
# 2. Extraire les "tours de parole" et nettoyer le texte pour le modèle CTC.
# 3. Aligner chaque mot sur l'audio (MMS-300m) et découper en "chunks" d'environ 12s.
# 4. Exporter les chunks et générer un 'segments_asr_ready.jsonl'.
"""

import os
import re
import csv
import json
from pathlib import Path

# IMPORTANT : Le Tri Naturel pour régler le bug 'Appelle 1, Appelle 10, Appelle 2' !
def natural_sort_key(s):
    """
    Sépare les lettres et les chiffres pour trier comme un humain.
    Ex: 'Appelle 1_c001' -> ['Appelle ', 1, '_c', 1]
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', str(s))]

def get_audio_files_sorted(audio_dir):
    """
    Récupère tous les fichiers WAV d'un dossier et les trie naturellement.
    C'est la base pour garder la cohérence avec le fichier CSV.
    """
    audio_path = Path(audio_dir)
    wav_files = list(audio_path.rglob('*.wav'))
    
    # On applique le tri magique ici !
    wav_files.sort(key=lambda x: natural_sort_key(x.name))
    return wav_files

def normalize_for_fa(text):
    """
    Normalisation du texte selon ton dictionnaire Arabizi pour l'Alignement.
    (Transformation des chiffres prononcés et des sons spéciaux)
    """
    t = text.lower()
    
    # 1. Conversion Arabizi standard (on garde les lettres pour que MMS puisse lire)
    mapping_arabizi = {
        '3': 'a', '7': 'h', '9': 'k', '5': 'kh'
    }
    
    # 2. (Ton travail de nettoyage du mémoire va ici)
    # Les chiffres non-arabizi isolés (comme les numéros de téléphone)
    # deviendront des entités exprimées en français pour correspondre au son réel.
    # Ex: "15" -> "quinze"
    # ...
    # (Par soucis de concision pour ce brouillon, c'est l'idée globale)
    
    return t.strip()

# =========================================================================
# LA SUITE SERA À EXÉCUTER SUR COLAB (OU SUR UN PC AVEC CARTE GRAPHIQUE)
# Car torchaudio + facebook/mms demande au moins 4Go de VRAM (GPU)
# =========================================================================

def run_forced_alignment(audio_path, text, device="cuda"):
    """
    1. torchaudio charge le fichier à 16kHz
    2. facebook/mms écoute et compare au texte 'text'
    3. Renvoie la liste des timestamps (début, fin) de chaque mot.
    """
    print(f"Alignement en cours pour {audio_path.name}...")
    # Code d'inférence Torchaudio (Simulé ici pour la structure)
    # ...
    return []

if __name__ == "__main__":
    print("=== DÉBUT DU PIPELINE DE PRÉTRAITEMENT ASR ===\\n")
    
    # Dossier de tes audios bruts (sur ton Drive ou local)
    AUDIO_SOURCES = "f:/dgpc_pipeline_ready/Pretraitement/asr_dataset/wavs_16k"
    
    # On vérifie que le tri fonctionne correctement !
    fichiers = get_audio_files_sorted(AUDIO_SOURCES)
    
    print(f"Trouvé {len(fichiers)} fichiers audio.")
    if len(fichiers) > 0:
        print("\\nLes 10 premiers fichiers détectés avec le TRI NATUREL :")
        for f in fichiers[:10]:
            print(f" -> {f.name}")
        
    print("\\nNote: Ces chunks pourront maintenant être envoyés à l'étape 2 (Feature Extraction).")
