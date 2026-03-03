"""
TTS Batch Pipeline — Synthetic emergency call audio generation
================================================================
Converts synthetic transcriptions (JSONL) → audio WAV files using F5-TTS
with voice cloning, arabizi normalization, and telephone post-processing.

Requirements (install on RTX 4070 machine):
    pip install f5-tts torch torchaudio soundfile pydub

Usage:
    python augmentation/tts_batch_pipeline.py \
        --input ml_pipeline/dataset/annotations_synthetic_rare.jsonl \
        --output_dir ml_pipeline/dataset/synthetic_audio \
        --voice_dir voices/

Pipeline:
    1. Load synthetic transcriptions (JSONL)
    2. Normalize arabizi → IPA-like (7→ħ, 3→ɛ, 9→q)
    3. Generate audio via F5-TTS with voice cloning
    4. Apply telephone post-processing (8kHz, bandpass, noise)
    5. Save WAV files + manifest CSV
"""

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Import arabizi normalizer ────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))
from arabizi_normalizer import normalize_arabizi_for_tts


# ── Constants ─────────────────────────────────────────────────────────

# Speed multipliers for stress levels (mel duration control)
STRESS_SPEED = {
    "calm":    1.0,   # Normal speed
    "hurried": 0.85,  # 15% faster
    "panic":   0.75,  # 25% faster
}

# Telephone quality parameters
PHONE_LOWCUT = 300    # Hz — telephone highpass
PHONE_HIGHCUT = 3400  # Hz — telephone lowpass
PHONE_SAMPLE_RATE = 8000  # G.711 standard


# ── Voice Profile Manager ────────────────────────────────────────────

class VoiceProfileManager:
    """Manages voice reference audio files for TTS cloning."""
    
    def __init__(self, voice_dir: str):
        self.voice_dir = Path(voice_dir)
        self.profiles: Dict[str, Dict] = {}
        self._load_profiles()
    
    def _load_profiles(self):
        """Scan voice directory for WAV files organized by role/emotion."""
        if not self.voice_dir.exists():
            print(f"[WARN] Voice directory not found: {self.voice_dir}")
            print(f"       Create it with subdirectories: caller_male/, caller_female/, operator/")
            return
        
        for wav_file in self.voice_dir.rglob("*.wav"):
            # Extract role from parent dir name
            role = wav_file.parent.name  # e.g., "caller_male", "operator"
            # Extract emotion hint from filename
            # e.g., "calm_01.wav", "panic_02.wav", "neutral.wav"
            emotion = wav_file.stem.split("_")[0] if "_" in wav_file.stem else "neutral"
            
            key = f"{role}_{emotion}"
            if key not in self.profiles:
                self.profiles[key] = {
                    "role": role,
                    "emotion": emotion,
                    "files": [],
                }
            self.profiles[key]["files"].append(str(wav_file))
        
        print(f"[OK] Loaded {len(self.profiles)} voice profiles from {self.voice_dir}")
        for k, v in self.profiles.items():
            print(f"     {k}: {len(v['files'])} files")
    
    def get_voice(self, role: str = "caller", stress: str = "calm") -> Optional[str]:
        """Pick a voice file matching the role and stress level."""
        # Map stress to voice emotion preference
        emotion_map = {
            "calm": ["calm", "neutral", "normal"],
            "hurried": ["hurried", "fast", "stressed", "neutral"],
            "panic": ["panic", "scream", "stressed", "hurried", "neutral"],
        }
        preferred = emotion_map.get(stress, ["neutral"])
        
        # Try matching role + preferred emotion
        for emotion in preferred:
            key = f"{role}_{emotion}"
            if key in self.profiles and self.profiles[key]["files"]:
                return random.choice(self.profiles[key]["files"])
        
        # Fallback: any file in this role
        for key, profile in self.profiles.items():
            if profile["role"] == role and profile["files"]:
                return random.choice(profile["files"])
        
        # Final fallback: any voice at all
        all_files = [f for p in self.profiles.values() for f in p["files"]]
        if all_files:
            return random.choice(all_files)
        
        return None


# ── Telephone Post-Processing ────────────────────────────────────────

def apply_telephone_filter(
    input_path: str,
    output_path: str,
    snr_db: float = 15.0,
    noise_path: Optional[str] = None,
) -> bool:
    """Apply telephone-quality degradation to an audio file.
    
    Pipeline:
    1. Bandpass filter 300-3400 Hz
    2. Resample to 8000 Hz mono
    3. Optional: add background noise at specified SNR
    """
    try:
        import torchaudio
        import torch
        
        waveform, sr = torchaudio.load(input_path)
        
        # Mono
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        
        # Bandpass filter using torchaudio
        # Highpass at 300Hz
        waveform = torchaudio.functional.highpass_biquad(waveform, sr, PHONE_LOWCUT)
        # Lowpass at 3400Hz
        waveform = torchaudio.functional.lowpass_biquad(waveform, sr, PHONE_HIGHCUT)
        
        # Resample to 8kHz
        if sr != PHONE_SAMPLE_RATE:
            resampler = torchaudio.transforms.Resample(sr, PHONE_SAMPLE_RATE)
            waveform = resampler(waveform)
        
        # Optional noise injection
        if noise_path and os.path.isfile(noise_path):
            noise, noise_sr = torchaudio.load(noise_path)
            if noise_sr != PHONE_SAMPLE_RATE:
                noise = torchaudio.transforms.Resample(noise_sr, PHONE_SAMPLE_RATE)(noise)
            if noise.shape[0] > 1:
                noise = noise.mean(dim=0, keepdim=True)
            # Loop noise to match signal length
            if noise.shape[1] < waveform.shape[1]:
                repeats = (waveform.shape[1] // noise.shape[1]) + 1
                noise = noise.repeat(1, repeats)
            noise = noise[:, :waveform.shape[1]]
            # Scale noise to desired SNR
            signal_power = waveform.pow(2).mean()
            noise_power = noise.pow(2).mean()
            if noise_power > 0:
                scale = torch.sqrt(signal_power / (noise_power * (10 ** (snr_db / 10))))
                waveform = waveform + scale * noise
        
        # Normalize
        peak = waveform.abs().max()
        if peak > 0:
            waveform = waveform / peak * 0.95
        
        torchaudio.save(output_path, waveform, PHONE_SAMPLE_RATE)
        return True
        
    except Exception as e:
        print(f"  [WARN] Telephone filter failed: {e}")
        # Fallback: just copy
        import shutil
        shutil.copy2(input_path, output_path)
        return False


# ── Main TTS Pipeline ─────────────────────────────────────────────────

def generate_audio_batch(
    input_jsonl: str,
    output_dir: str,
    voice_dir: str = "voices",
    noise_dir: Optional[str] = None,
    phone_filter: bool = True,
    limit: Optional[int] = None,
    model: str = "F5TTS_v1_Base",
):
    """Generate audio from synthetic transcriptions using F5-TTS."""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    raw_dir = output_path / "raw"
    raw_dir.mkdir(exist_ok=True)
    phone_dir = output_path / "phone"  
    phone_dir.mkdir(exist_ok=True)
    
    # Load transcriptions
    print(f"Loading transcriptions from: {input_jsonl}")
    entries = []
    with open(input_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    if limit:
        entries = entries[:limit]
    print(f"  {len(entries)} entries loaded")
    
    # Load voice profiles
    voice_mgr = VoiceProfileManager(voice_dir)
    
    # Collect noise files
    noise_files = []
    if noise_dir and os.path.isdir(noise_dir):
        noise_files = [str(p) for p in Path(noise_dir).glob("*.wav")]
        print(f"  {len(noise_files)} noise files found")
    
    # Initialize F5-TTS
    print(f"\nInitializing F5-TTS model: {model}")
    try:
        from f5_tts.api import F5TTS
        tts = F5TTS(model_type=model)
        print(f"  [OK] F5-TTS loaded on GPU")
    except ImportError:
        print("[ERROR] F5-TTS not installed. Install with:")
        print("  pip install f5-tts")
        print("\nFalling back to XTTS-v2...")
        tts = None
    
    # Generate manifest
    manifest = []
    failed = 0
    
    for idx, entry in enumerate(entries):
        task_id = entry.get("meta", {}).get("task_id", f"synth_{idx:04d}")
        raw_text = entry.get("transcription", "")
        stress = entry.get("meta", {}).get("constraints_applied", {}).get("stress_level", "calm")
        incident = entry.get("labels", {}).get("incident_type", "unknown")
        
        filename = f"{task_id}_{idx:04d}"
        raw_wav = raw_dir / f"{filename}.wav"
        phone_wav = phone_dir / f"{filename}.wav"
        
        print(f"\n[{idx+1}/{len(entries)}] {task_id} ({incident}, {stress})")
        
        # Step 1: Normalize arabizi
        normalized_text = normalize_arabizi_for_tts(raw_text)
        print(f"  Text: {normalized_text[:80]}...")
        
        # Step 2: Get voice profile
        # Alternate between caller roles
        role = random.choice(["caller_male", "caller_female"]) if random.random() > 0.3 else "operator"
        voice_file = voice_mgr.get_voice(role=role, stress=stress)
        
        if not voice_file:
            print(f"  [SKIP] No voice profile found. Create voices/ directory with WAV files.")
            failed += 1
            continue
        
        # Step 3: Generate audio with F5-TTS
        try:
            if tts:
                # F5-TTS generation
                speed = STRESS_SPEED.get(stress, 1.0)
                wav, sr, _ = tts.infer(
                    ref_file=voice_file,
                    ref_text="",  # Empty = auto-transcribe reference
                    gen_text=normalized_text,
                    file_wave=str(raw_wav),
                    speed=speed,
                    seed=random.randint(0, 99999),
                )
                print(f"  [OK] Audio generated: {raw_wav.name} ({speed}x speed)")
            else:
                # Fallback to existing XTTS-v2 pipeline
                from ml_pipeline.synthetic.tts_generator import TTSGenerator
                xtts = TTSGenerator(speaker_wav=voice_file, language="fr")
                xtts.synthesize(normalized_text, str(raw_wav))
                print(f"  [OK] Audio generated via XTTS-v2: {raw_wav.name}")
        except Exception as e:
            print(f"  [FAIL] TTS error: {e}")
            failed += 1
            continue
        
        # Step 4: Apply telephone post-processing
        if phone_filter and raw_wav.exists():
            noise_file = random.choice(noise_files) if noise_files else None
            snr = random.uniform(8, 20)  # Variable SNR for diversity
            success = apply_telephone_filter(
                str(raw_wav), str(phone_wav),
                snr_db=snr, noise_path=noise_file
            )
            final_wav = phone_wav if success else raw_wav
            print(f"  [OK] Phone filter: SNR={snr:.0f}dB → {phone_wav.name}")
        else:
            final_wav = raw_wav
        
        # Add to manifest
        manifest.append({
            "file": str(final_wav),
            "transcription": raw_text,
            "normalized_text": normalized_text,
            "incident_type": incident,
            "stress_level": stress,
            "voice_role": role,
            "voice_file": os.path.basename(voice_file),
        })
    
    # Save manifest
    manifest_path = output_path / "manifest.csv"
    import csv
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        if manifest:
            writer = csv.DictWriter(f, fieldnames=manifest[0].keys())
            writer.writeheader()
            writer.writerows(manifest)
    
    print(f"\n{'='*60}")
    print(f"  Generated: {len(manifest)}/{len(entries)} audio files")
    print(f"  Failed:    {failed}")
    print(f"  Raw audio: {raw_dir}")
    print(f"  Phone audio: {phone_dir}")
    print(f"  Manifest:  {manifest_path}")


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TTS Batch Pipeline for synthetic calls")
    parser.add_argument("--input", required=True, help="Input JSONL file with synthetic transcriptions")
    parser.add_argument("--output_dir", default="ml_pipeline/dataset/synthetic_audio", help="Output directory")
    parser.add_argument("--voice_dir", default="voices", help="Directory with voice WAV files")
    parser.add_argument("--noise_dir", default=None, help="Directory with noise WAV files for SNR mixing")
    parser.add_argument("--no_phone_filter", action="store_true", help="Skip telephone post-processing")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of entries")
    parser.add_argument("--model", default="F5TTS_v1_Base", help="F5-TTS model variant")
    args = parser.parse_args()
    
    generate_audio_batch(
        input_jsonl=args.input,
        output_dir=args.output_dir,
        voice_dir=args.voice_dir,
        noise_dir=args.noise_dir,
        phone_filter=not args.no_phone_filter,
        limit=args.limit,
        model=args.model,
    )


if __name__ == "__main__":
    main()
