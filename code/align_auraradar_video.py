#!/usr/bin/env python3
"""
AuraRadar Video Alignment Compiler
Refined to produce a smooth Talking Head (A-Roll) master video.
"""

import os
import sys

# Add the current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from video_story_editor import parse_vtt_segments, edit_video

def compile_auraradar_video():
    root_dir = os.path.dirname(current_dir)
    raw_video = os.path.join(root_dir, "data", "raw", "raw_talk.mp4")
    vtt_file = os.path.join(root_dir, "data", "raw", "raw_talk.vtt")
    output_video = os.path.join(root_dir, "data", "processed", "talking_head_master.mp4")
    
    os.makedirs(os.path.join(root_dir, "data", "raw"), exist_ok=True)
    os.makedirs(os.path.join(root_dir, "data", "processed"), exist_ok=True)

    if not os.path.exists(raw_video):
        print(f"Error: Raw footage not found at: {raw_video}")
        return
        
    print("Parsing VTT segments...")
    segments = parse_vtt_segments(vtt_file)
    print(f"Found {len(segments)} segments in VTT.")
    
    # ----------------------------------------------------
    # REFINED SELECTION: Picked the single best takes for each line.
    # Sequential 1-based indices in the 176-segment VTT.
    # ----------------------------------------------------
    selected_indices = [
        3, 4, 8, 9, 10, 11, 13, 14, 17, 18, 19, 22, 25, 26, 28, 33, 34, 39, 42, 43, 
        47, 48, 51, 56, 57, 58, 63, 67, 68, 70, 75, 76, 77, 79, 80, 81, 82, 85, 94, 
        97, 98, 99, 100, 103, 105, 107, 109, 114, 115, 116, 125, 126, 127, 128, 
        130, 135, 138, 144, 146, 149
    ]
    
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
            
    print(f"\nCompiling {len(selected_segments)} refined segments into {output_video}...")
    
    prev_cwd = os.getcwd()
    os.chdir(root_dir)
    try:
        edit_video(selected_segments, output_video)
        print(f"Talking Head Master compiled successfully! Saved as {output_video}")
    finally:
        os.chdir(prev_cwd)

if __name__ == "__main__":
    compile_auraradar_video()
