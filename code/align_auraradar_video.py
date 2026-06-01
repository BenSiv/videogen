#!/usr/bin/env python3
"""
AuraRadar Video Alignment Compiler
Slices and concatenates raw talk footage based on custom transcript selections.
Designed specifically for compiling the AuraRadar YouTube presentation.
"""

import os
import sys

# Add the current directory to path to support running from root or code folder
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from video_story_editor import parse_vtt_segments, edit_video

def compile_auraradar_video():
    # Define paths relative to the project root
    root_dir = os.path.dirname(current_dir)
    raw_video = os.path.join(root_dir, "videos", "raw_talk.mp4")
    vtt_file = os.path.join(root_dir, "transcripts", "raw_talk.vtt")
    output_video = os.path.join(root_dir, "coherent_storyline.mp4")
    
    # Create required directories
    os.makedirs(os.path.join(root_dir, "videos"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "transcripts"), exist_ok=True)

    if not os.path.exists(raw_video):
        print(f"Error: Raw footage not found at: {raw_video}")
        print("Please:")
        print("  1. Record your talk (incorporating multiple takes/mistakes naturally).")
        print("  2. Save it as 'raw_talk.mp4' in the 'videos/' folder.")
        print("  3. Run this script again to auto-transcribe and compile.")
        return
        
    if not os.path.exists(vtt_file):
        print(f"VTT transcript not found at {vtt_file}. Generating auto-transcription with Whisper...")
        try:
            import whisper
            model = whisper.load_model("base")
            print("Transcribing audio (this may take a few minutes)...")
            result = model.transcribe(raw_video)
            
            # Simple VTT exporter
            with open(vtt_file, "w", encoding="utf-8") as f:
                f.write("WEBVTT\n\n")
                for idx, seg in enumerate(result.get("segments", []), start=1):
                    start_sec = seg["start"]
                    end_sec = seg["end"]
                    text = seg["text"].strip()
                    
                    # Convert to VTT timestamp format (HH:MM:SS.mmm)
                    def format_time(s):
                        hours = int(s // 3600)
                        minutes = int((s % 3600) // 60)
                        seconds = s % 60
                        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
                    
                    f.write(f"segment_{idx}\n")
                    f.write(f"{format_time(start_sec)} --> {format_time(end_sec)}\n")
                    f.write(f"{text}\n\n")
            print(f"VTT transcript generated at {vtt_file}")
        except ImportError:
            print("Error: 'whisper' library is not installed in your environment.")
            print("Please run: pip install openai-whisper torch")
            return
        except Exception as e:
            print(f"Whisper transcription failed: {e}")
            return

    # Parse segments
    print("Parsing VTT segments...")
    segments = parse_vtt_segments(vtt_file)
    
    print(f"Found {len(segments)} segments in VTT.")
    
    # ----------------------------------------------------
    # INSTRUCTIONS:
    # Once raw_talk.vtt is generated in your transcripts/ folder,
    # inspect it to find the index of your best takes.
    # List the segment indices in order here to build your narrative:
    # ----------------------------------------------------
    selected_indices = []
    
    if not selected_indices:
        print("\nTip: Your 'selected_indices' list in this script is currently empty.")
        print("We will preview the first 15 segments for you:")
        print("--------------------------------------------------")
        for idx, seg in enumerate(segments[:15], start=1):
            print(f"Segment {idx} ({seg['start']:.1f}s - {seg['end']:.1f}s): {seg['text']}")
        print("--------------------------------------------------")
        print("Please edit 'code/align_auraradar_video.py' to list the segment indices of your best takes in order!")
        print("Falling back to compiling ALL segments sequentially for preview...")
        selected_indices = list(range(1, len(segments) + 1))
    
    selected_segments = []
    for idx in selected_indices:
        if 1 <= idx <= len(segments):
            seg = segments[idx - 1]
            selected_segments.append({
                "clip": "raw_talk.mp4",
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"]
            })
            
    print(f"\nCompiling {len(selected_segments)} selected segments into {output_video}...")
    
    # Temporarily change working directory to videogen root to let edit_video resolve relative paths
    prev_cwd = os.getcwd()
    os.chdir(root_dir)
    try:
        edit_video(selected_segments, "coherent_storyline.mp4")
        print(f"Final video compiled successfully! Saved as {output_video}")
    finally:
        os.chdir(prev_cwd)

if __name__ == "__main__":
    compile_auraradar_video()
