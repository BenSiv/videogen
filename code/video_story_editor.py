#!/usr/bin/env python3
"""
Video Story Editor: Programmatically edit MP4 files to create a coherent storyline
from fragmented videos and transcriptions using AI (OpenAI GPT-3.5).
Uses MoviePy for smoother transitions and segment extraction.
"""

import ast
import os
import subprocess
import sys
import tempfile
import openai
import whisper
from moviepy import VideoFileClip, concatenate_videoclips, vfx

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VIDEO_DIR = "data/raw"
TRANSCRIPT_DIR = "data/raw"
OUTPUT_FILE = "data/processed/coherent_storyline.mp4"

# Editing settings for smoothness
HANDLE_PADDING = 0.1  # Seconds to add to start/end of segments
CROSSFADE_DURATION = 0.2  # Seconds of overlap between clips


def parse_timestamp(timestamp):
    """Convert a VTT timestamp to seconds."""
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
    """Parse a VTT file and return timed transcript segments."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    segments = []
    current_text = []
    start = None
    end = None

    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT":
            continue
        if "-->" in line:
            if start is not None and current_text:
                segments.append({
                    "start": start,
                    "end": end,
                    "text": " ".join(current_text).strip(),
                })
                current_text = []
            start_str, end_str = line.split("-->")
            start = parse_timestamp(start_str.strip())
            end = parse_timestamp(end_str.strip())
            continue
        if start is not None:
            current_text.append(line)

    if start is not None and current_text:
        segments.append({
            "start": start,
            "end": end,
            "text": " ".join(current_text).strip(),
        })

    return segments


def transcribe_clip_segments(video_path):
    """Use Whisper to generate segments with timestamps for a clip."""
    print(f"Generating timed transcript for {os.path.basename(video_path)}...")
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return [
        {
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        }
        for seg in result.get("segments", [])
    ]


def generate_transcripts(video_dir, transcript_dir):
    """Generate transcriptions using Whisper if not already present."""
    model = whisper.load_model("base")
    os.makedirs(transcript_dir, exist_ok=True)
    for file in sorted(os.listdir(video_dir)):
        if file.endswith(".mp4"):
            video_path = os.path.join(video_dir, file)
            transcript_txt = os.path.join(transcript_dir, file.replace(".mp4", ".txt"))
            transcript_vtt = os.path.join(transcript_dir, file.replace(".mp4", ".vtt"))
            if not os.path.exists(transcript_txt) and not os.path.exists(transcript_vtt):
                print(f"Transcribing {file}...")
                result = model.transcribe(video_path)
                with open(transcript_txt, "w") as f:
                    f.write(result["text"])
                print(f"Transcription saved to {transcript_txt}")


def load_segments(video_dir, transcript_dir):
    """Load timed segments for each clip from VTT or fallback transcription."""
    segments_by_clip = {}
    clip_files = sorted([f for f in os.listdir(video_dir) if f.endswith(".mp4")])

    if not clip_files:
        print("No video clips found in the videos folder.")
        sys.exit(1)

    for clip in clip_files:
        clip_path = os.path.join(video_dir, clip)
        base_name = os.path.splitext(clip)[0]
        vtt_path = os.path.join(transcript_dir, base_name + ".vtt")
        txt_path = os.path.join(transcript_dir, base_name + ".txt")

        if os.path.exists(vtt_path):
            print(f"Loading VTT transcript for {clip}...")
            segments_by_clip[clip] = parse_vtt_segments(vtt_path)
        elif os.path.exists(txt_path):
            print(f"VTT not found for {clip}. Falling back to timed transcript generation from audio.")
            segments_by_clip[clip] = transcribe_clip_segments(clip_path)
        else:
            print(f"No transcript found for {clip}. Generating timed transcript from audio.")
            segments_by_clip[clip] = transcribe_clip_segments(clip_path)

    return segments_by_clip


def select_story_segments(segments_by_clip):
    """Use AI to choose the best segments for a streamlined storyline."""
    selected_segments = []
    segment_map = {}
    prompt_lines = []

    for clip_name, segments in segments_by_clip.items():
        for idx, seg in enumerate(segments, start=1):
            label = f"{clip_name}_{idx}"
            segment_map[label] = {
                "clip": clip_name,
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
            }
            prompt_lines.append(
                f"{label}: {seg['start']:.2f}-{seg['end']:.2f} | {seg['text']}"
            )

    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY not set. Using all segments.")
        return [segment_map[label] for label in segment_map]

    openai.api_key = OPENAI_API_KEY
    prompt = (
        "Select the segments that should remain in the final streamlined storyline. "
        "Output only a Python list of labels.\n\n" + "\n".join(prompt_lines)
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        labels = ast.literal_eval(response.choices[0].message.content.strip())
        return [segment_map[l] for l in labels if l in segment_map]
    except Exception as e:
        print(f"AI selection failed: {e}. Using all segments.")
        return [segment_map[label] for label in segment_map]


def edit_video(selected_segments, output_file):
    """Extract and concatenate selected segments into the final video using MoviePy."""
    if not selected_segments:
        print("No segments selected.")
        sys.exit(1)

    clips = []
    video_cache = {}

    print(f"Processing {len(selected_segments)} segments with MoviePy...")
    
    try:
        for i, item in enumerate(selected_segments):
            clip_name = item["clip"]
            if clip_name not in video_cache:
                video_cache[clip_name] = VideoFileClip(os.path.join(VIDEO_DIR, clip_name))
            
            full_video = video_cache[clip_name]
            
            # Apply padding (handles) to avoid clipping words
            start = max(0, item["start"] - HANDLE_PADDING)
            end = min(full_video.duration, item["end"] + HANDLE_PADDING)
            
            print(f"  Segment {i+1}: {clip_name} ({start:.2f}s - {end:.2f}s)")
            
            # Extract subclip
            subclip = full_video.subclipped(start, end)
            
            # Add crossfade transition if not the first clip
            if clips and CROSSFADE_DURATION > 0:
                subclip = subclip.with_effects([vfx.CrossFadeIn(CROSSFADE_DURATION)])
            
            clips.append(subclip)

        if not clips:
            print("No valid segments to compile.")
            sys.exit(1)

        print("Joining clips and rendering final video (this may take a while)...")
        # padding=-CROSSFADE_DURATION overlaps clips to allow crossfade effect
        final_video = concatenate_videoclips(clips, method="compose", padding=-CROSSFADE_DURATION)
        
        # Write the file. Using a high quality preset.
        final_video.write_videofile(
            output_file,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="medium",
            threads=4
        )
        
        print(f"Successfully saved coherent storyline to {output_file}")

    finally:
        # Clean up resources
        for v in video_cache.values():
            v.close()


def main():
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)
    generate_transcripts(VIDEO_DIR, TRANSCRIPT_DIR)
    segments_by_clip = load_segments(VIDEO_DIR, TRANSCRIPT_DIR)
    selected_segments = select_story_segments(segments_by_clip)
    edit_video(selected_segments, OUTPUT_FILE)


if __name__ == "__main__":
    main()
