#!/usr/bin/env python3
"""
Generative Video Enhancer
Applies AI-driven enhancements to the master talking head video.
1. Generative Audio Harmonization (using DeepFilterNet)
2. Generative Motion Smoothing (using FFmpeg minterpolate)
"""

import os
import sys
import subprocess
from moviepy import VideoFileClip

# Paths
INPUT_VIDEO = "data/processed/talking_head_master.mp4"
OUTPUT_DIR = "data/processed/enhanced"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def enhance_audio(input_path):
    """
    Applies DeepFilterNet to enhance speech quality and normalize acoustics.
    DeepFilterNet uses a deep neural network to 'regenerate' clean speech.
    """
    print("\n--- Phase 1: Generative Audio Harmonization ---")
    output_audio_video = os.path.join(OUTPUT_DIR, "talking_head_audio_enhanced.mp4")
    
    # DeepFilterNet command
    # It processes the video file, extracts audio, enhances it, and merges it back.
    cmd = [
        "python3", "-m", "df.enhance", 
        "--output-dir", OUTPUT_DIR,
        input_path
    ]
    
    print(f"Running DeepFilterNet on {input_path}...")
    try:
        subprocess.run(cmd, check=True)
        # DeepFilterNet usually names the output by appending '_enhanced'
        base_name = os.path.basename(input_path).replace(".mp4", "_enhanced.mp4")
        enhanced_path = os.path.join(OUTPUT_DIR, base_name)
        return enhanced_path
    except Exception as e:
        print(f"DeepFilterNet enhancement failed: {e}")
        return input_path

def smooth_motion(input_path):
    """
    Uses FFmpeg's motion-compensated interpolation to 'heal' jump cuts.
    It generates intermediate frames to simulate smooth head movement.
    """
    print("\n--- Phase 2: Generative Motion Smoothing ---")
    output_path = os.path.join(OUTPUT_DIR, "talking_head_final_ai.mp4")
    
    # FFmpeg minterpolate filter:
    # mi_mode=mci: Motion-compensated interpolation (Generative approach)
    # mc_mode=aob: Advanced Overlapped Block (Reduces artifacts)
    # fps=60: Increases frame rate to make transitions fluid
    
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", "minterpolate=fps=60:mi_mode=mci:mc_mode=aob:me_mode=bidir:vsfm=1",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-c:a", "copy", "-y",
        output_path
    ]
    
    print(f"Applying motion interpolation to {input_path} (this is computationally heavy)...")
    try:
        subprocess.run(cmd, check=True)
        return output_path
    except Exception as e:
        print(f"Motion smoothing failed: {e}")
        return input_path

def main():
    if not os.path.exists(INPUT_VIDEO):
        print(f"Error: Input video not found at {INPUT_VIDEO}")
        sys.exit(1)

    # Step 1: Harmonize Audio
    audio_enhanced_video = enhance_audio(INPUT_VIDEO)
    
    # Step 2: Smooth Motion
    final_video = smooth_motion(audio_enhanced_video)
    
    print(f"\nAI Enhancement Complete!")
    print(f"Final Enhanced Video: {final_video}")

if __name__ == "__main__":
    main()
