#!/usr/bin/env python3
"""
Fix Missing Transcriptions Script

Detects and repairs empty transcriptions in the annotation database.
Uses Gemini 3.1 Pro Preview with the same system prompt as the annotation app.
"""

import json
import os
import sys
import pandas as pd
import google.generativeai as genai
from pathlib import Path
from datetime import datetime
from pydub import AudioSegment

# ============================================================================
# CONFIGURATION
# ============================================================================

ANNOTATIONS_FILE = "dataset/annotations_local.json"
ANNOTATIONS_CSV = "dataset/annotations_local.csv"
AUDIO_RAW_DIR = "audio_raw"
AUDIO_PROC_DIR = "audio_processed"

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

# System prompt (same as annotation app)
SYSTEM_PROMPT = """Tu es un expert linguiste du dialecte BÃ©jaoui (Taqbaylit n Bgayet), un mÃ©lange fluide de Kabyle, FranÃ§ais et Arabe AlgÃ©rien.

RÃˆGLES DE TRANSCRIPTION (GOLD STANDARD):

1. ROMANISATION ARABIZI (OBLIGATOIRE):
   Utilise UNIQUEMENT le systÃ¨me arabizi, JAMAIS les caractÃ¨res linguistiques acadÃ©miques.

2. CODE-SWITCHING "Bejaia Style":
   - Garde les mots franÃ§ais intÃ©grÃ©s avec l'article "l'" collÃ©: l'ambulance, l'accident, l'bloc, l'camion.
   - Termes mÃ©dicaux FR maintenus: crise, tension, saturation, inconscient, blessÃ©.

3. NÃ‰GATION (CIRCUMFIXE OBLIGATOIRE):
   - Forme verbale: ur {verbe} ara  (ex: "ur yezmir ara" = il ne peut pas)
   - Nominal: ulach / wlach (il n'y a pas)

4. PARTICULES & MARQUEURS:
   - Affirmation: an3am, ih, iyeh, d'accord
   - DÃ©ictiques: dayi, dagi, dinna, tura
   - Interrogatifs: anda, amek, dachu, anwa

5. VERBES D'URGENCE (conjugaison corpus):
   - ghli (tomber/s'Ã©vanouir): i-ghli, t-ghli, ye-ghli
   - che3l (brÃ»ler): tche3l, ich3el, cha3let
   - nuffes (respirer): t-nuffes, ur t-nuffes ara

6. FORMAT DE DIALOGUE:
   Utilise le format flux continu (sans marqueur) ou tirets (â€”)

CONTEXTE URGENCE BÃ‰JAÃA:
Fournis une transcription VERBATIM exacte de ce qui est dit dans l'audio.
"""

# ============================================================================
# UTILITIES
# ============================================================================

def load_data(p):
    """Load JSON data"""
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def process_audio(audio_path):
    """Convert audio to 16kHz WAV"""
    try:
        out = os.path.join(AUDIO_PROC_DIR, Path(audio_path).stem + ".wav")
        os.makedirs(AUDIO_PROC_DIR, exist_ok=True)
        if not os.path.exists(out):
            audio = AudioSegment.from_file(audio_path)
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(out, format="wav")
        return out
    except Exception as e:
        print(f"âŒ Error processing {audio_path}: {e}")
        return None

def transcribe_audio(api_key, audio_path):
    """Transcribe audio using Gemini"""
    try:
        genai.configure(api_key=api_key)
        
        # Prepare audio file
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        # Create a temporary file for Gemini (it can't handle bytes directly in this context)
        # So we'll use the file URI approach or upload it
        print(f"  ðŸ“Š Transcribing {Path(audio_path).name}...")
        
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        
        # Upload file for processing
        import mimetypes
        mime_type = "audio/wav"
        
        media = genai.upload_file(audio_path, mime_type=mime_type)
        
        # Create message with audio
        message = model.generate_content([
            "Fournis UNE transcription VERBATIM exacte et complÃ¨te de cet appel (tout ce qui est dit, sans rien ajouter). " +
            "Respecte EXACTEMENT les rÃ¨gles Arabizi et le style BÃ©jaoui. " +
            "La transcription DOIT Ãªtre complÃ¨te et JAMAIS vide.",
            media
        ])
        
        transcription = message.text.strip()
        
        # Clean up uploaded file
        genai.delete_file(media.name)
        
        return transcription if transcription else None
        
    except Exception as e:
        print(f"  âŒ Transcription error: {e}")
        return None

def save_all(data_list):
    """Save data to JSON and CSV"""
    with open(ANNOTATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)
    
    rows = []
    for a in data_list:
        row = {
            'ID': a.get('id_audio'),
            'File': a.get('audio_file'),
            'Transcription': a.get('transcription', ''),
        }
        row.update(a.get('extraction', {}))
        rows.append(row)
    
    pd.DataFrame(rows).to_csv(ANNOTATIONS_CSV, index=False, encoding='utf-8-sig')

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("=" * 80)
    print("  DGPC: Fix Missing Transcriptions")
    print("=" * 80)
    
    if not GEMINI_API_KEY:
        print("\nâŒ ERROR: GEMINI_API_KEY not found in environment!")
        print("Please set it in .env file or as environment variable.")
        sys.exit(1)
    
    # Load annotations
    annotations = load_data(ANNOTATIONS_FILE)
    print(f"\nðŸ“– Loaded {len(annotations)} annotations")
    
    # Find missing transcriptions
    missing = [a for a in annotations if not a.get('transcription') or a.get('transcription').strip() == '']
    print(f"ðŸš¨ Found {len(missing)} annotations with empty transcriptions")
    
    if not missing:
        print("âœ… All transcriptions are complete!")
        return
    
    # Process each missing transcription
    repaired = 0
    for entry in missing:
        audio_file = entry.get('audio_file')
        audio_path = os.path.join(AUDIO_RAW_DIR, audio_file)
        
        if not os.path.exists(audio_path):
            print(f"  âš ï¸  Audio file not found: {audio_file}")
            continue
        
        print(f"\nðŸ”§ Processing {audio_file}...")
        
        # Process audio to WAV
        wav_path = process_audio(audio_path)
        if not wav_path:
            continue
        
        # Transcribe
        transcription = transcribe_audio(GEMINI_API_KEY, wav_path)
        if transcription:
            # Update entry
            entry['transcription'] = transcription
            entry['timestamp'] = datetime.now().isoformat()
            repaired += 1
            print(f"  âœ… Transcription added ({len(transcription)} chars)")
        else:
            print(f"  âŒ Failed to transcribe")
    
    # Save results
    if repaired > 0:
        print(f"\nðŸ’¾ Saving {repaired} repaired records...")
        save_all(annotations)
        print(f"âœ… Successfully fixed {repaired} transcriptions!")
    else:
        print("âŒ No transcriptions were successfully repaired.")

if __name__ == "__main__":
    main()

