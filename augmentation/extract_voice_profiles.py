"""
Extract voice reference segments from real emergency calls.
============================================================
Scans audio files and extracts 10-second segments suitable for TTS voice cloning.

Usage:
    python augmentation/extract_voice_profiles.py \
        --audio_dir G:/audio/Audio_Valides \
        --output_dir voices/
"""

import argparse
import os
from pathlib import Path


def extract_segments(audio_dir: str, output_dir: str, segment_seconds: float = 10.0):
    """Extract voice reference segments from real call audio files."""
    try:
        import torchaudio
    except ImportError:
        print("[ERROR] torchaudio not installed. Run: pip install torchaudio")
        return
    
    audio_path = Path(audio_dir)
    out_path = Path(output_dir)
    
    # Create role directories
    for role in ["caller_male", "caller_female", "operator"]:
        for emotion in ["calm", "neutral", "stressed"]:
            (out_path / role).mkdir(parents=True, exist_ok=True)
    
    # Find WAV files
    wav_files = sorted(audio_path.glob("*.wav"))
    print(f"Found {len(wav_files)} WAV files in {audio_dir}")
    
    extracted = 0
    for i, wav_file in enumerate(wav_files[:30]):  # Process first 30 files
        try:
            waveform, sr = torchaudio.load(str(wav_file))
            duration = waveform.shape[1] / sr
            
            if duration < segment_seconds:
                continue
            
            # Extract a segment from the middle (usually has speech)
            mid = int(waveform.shape[1] / 2)
            half_seg = int(segment_seconds * sr / 2)
            start = max(0, mid - half_seg)
            end = min(waveform.shape[1], mid + half_seg)
            segment = waveform[:, start:end]
            
            # Mono
            if segment.shape[0] > 1:
                segment = segment.mean(dim=0, keepdim=True)
            
            # Normalize
            peak = segment.abs().max()
            if peak > 0:
                segment = segment / peak * 0.9
            
            # Save — user will manually sort into roles later
            role = "caller_male"  # Default — user can rename/sort
            out_file = out_path / role / f"neutral_{extracted:02d}.wav"
            torchaudio.save(str(out_file), segment, sr)
            print(f"  [{extracted+1}] {wav_file.name} → {out_file.name} ({segment_seconds}s @ {sr}Hz)")
            extracted += 1
            
        except Exception as e:
            print(f"  [SKIP] {wav_file.name}: {e}")
    
    print(f"\nExtracted {extracted} voice segments to {output_dir}")
    print(f"\nNext steps:")
    print(f"  1. Listen to each file and sort into caller_male/, caller_female/, operator/")
    print(f"  2. Rename files with emotion: calm_01.wav, stressed_01.wav, etc.")
    print(f"  3. For panic voices: record yourself speaking stressed (10s)")


def main():
    parser = argparse.ArgumentParser(description="Extract voice profiles from real calls")
    parser.add_argument("--audio_dir", default="G:/audio/Audio_Valides", help="Directory with real call WAV files")
    parser.add_argument("--output_dir", default="voices", help="Output directory for voice profiles")
    parser.add_argument("--seconds", type=float, default=10.0, help="Segment duration in seconds")
    args = parser.parse_args()
    
    extract_segments(args.audio_dir, args.output_dir, args.seconds)


if __name__ == "__main__":
    main()
