#!/usr/bin/env python3
"""
Video Story Editor: Programmatically edit MP4 files to create a coherent storyline.
Focuses on producing a smooth A-Roll (Talking Head) master video.
"""

import ast
import os
import sys
import tempfile
import openai
import whisper
from moviepy import VideoFileClip, concatenate_videoclips, vfx

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VIDEO_DIR = "data/raw"
TRANSCRIPT_DIR = "data/raw"
OUTPUT_FILE = "data/processed/talking_head_master.mp4"

# Editing settings for maximum smoothness
HANDLE_PADDING = 0.2  # Seconds of extra footage to add to start/end of segments
CROSSFADE_DURATION = 0.4  # Seconds of overlap between clips to hide jump cuts


def parse_timestamp(timestamp):
    timestamp = timestamp.replace(",", ".")
    parts = timestamp.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours) * 3600 + float(minutes) * 60 + float(seconds)
    if len(parts) == 2:
        minutes, seconds = parts
        return float(minutes) * 60 + float(seconds)
    return float(parts[0])


def parse_vtt_segments(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    segments, current_text = [], []
    start, end = None, None
    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT": continue
        if "-->" in line:
            if start is not None and current_text:
                segments.append({"start": start, "end": end, "text": " ".join(current_text).strip()})
                current_text = []
            start_str, end_str = line.split("-->")
            start, end = parse_timestamp(start_str.strip()), parse_timestamp(end_str.strip())
            continue
        if start is not None: current_text.append(line)
    if start is not None and current_text:
        segments.append({"start": start, "end": end, "text": " ".join(current_text).strip()})
    return segments


def edit_video(selected_segments, output_file, broll_plan=None):
    """
    Concatenates selected segments into a smooth Talking Head master.
    Ignores B-Roll to ensure the primary footage is uninterrupted.
    """
    if not selected_segments:
        print("No segments selected.")
        sys.exit(1)

    talk_clips = []
    video_cache = {}
    
    print(f"Processing {len(selected_segments)} segments into a smooth Talking Head master...")
    
    try:
        for i, item in enumerate(selected_segments):
            clip_name = item["clip"]
            if clip_name not in video_cache:
                video_cache[clip_name] = VideoFileClip(os.path.join(VIDEO_DIR, clip_name))
            
            full_video = video_cache[clip_name]
            
            # Use padding to ensure words aren't cut and transitions are smooth
            start = max(0, item["start"] - HANDLE_PADDING)
            end = min(full_video.duration, item["end"] + HANDLE_PADDING)
            
            print(f"  Segment {i+1}: {clip_name} ({start:.2f}s - {end:.2f}s)")
            
            subclip = full_video.subclipped(start, end)
            
            # Add crossfade effect to every clip except the first one
            if talk_clips and CROSSFADE_DURATION > 0:
                subclip = subclip.with_effects([vfx.CrossFadeIn(CROSSFADE_DURATION)])
            
            talk_clips.append(subclip)

        if not talk_clips:
            print("No valid segments to compile.")
            sys.exit(1)

        print("Joining clips and rendering high-quality master (this may take a while)...")
        # method="compose" and padding=-CROSSFADE_DURATION creates the overlap for crossfades
        final_video = concatenate_videoclips(talk_clips, method="compose", padding=-CROSSFADE_DURATION)
        
        final_video.write_videofile(
            output_file,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="medium",
            threads=4
        )
        
        print(f"Successfully saved Talking Head Master to {output_file}")

    finally:
        for v in video_cache.values():
            v.close()


def main():
    # Placeholder for standalone runs
    print("Use code/align_auraradar_video.py to compile your master video.")


if __name__ == "__main__":
    main()
