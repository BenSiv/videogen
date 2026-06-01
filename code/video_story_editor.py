#!/usr/bin/env python3
"""
Video Story Editor: Programmatically edit MP4 files to create a coherent storyline
from fragmented videos and transcriptions using AI (OpenAI GPT-3.5).
Uses FFmpeg for efficient segment extraction and concatenation.
"""

import ast
import os
import subprocess
import sys
import tempfile
import openai
import whisper

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set your API key as an environment variable
VIDEO_DIR = "videos"  # Folder containing fragmented MP4 files
TRANSCRIPT_DIR = "transcripts"  # Folder containing corresponding text or VTT files
OUTPUT_FILE = "coherent_storyline.mp4"


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


def get_video_duration(video_path):
    """Get the duration of a video file in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1:csv=p=0", video_path],
        capture_output=True,
        text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


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
    model = whisper.load_model("base")  # Use 'medium' or 'large' for better accuracy
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
            print(
                f"VTT not found for {clip}. Falling back to timed transcript generation from audio."
            )
            segments_by_clip[clip] = transcribe_clip_segments(clip_path)
        else:
            print(f"No transcript found for {clip}. Generating timed transcript from audio.")
            segments_by_clip[clip] = transcribe_clip_segments(clip_path)

        if not segments_by_clip[clip]:
            print(f"Warning: no segments were loaded for {clip}.")

    return segments_by_clip


def format_segment_label(clip_name, index):
    return f"{clip_name}_{index}"


def select_story_segments(segments_by_clip):
    """Use AI to choose the best segments for a streamlined storyline."""
    selected_segments = []
    segment_map = {}
    prompt_lines = []

    for clip_name, segments in segments_by_clip.items():
        for idx, seg in enumerate(segments, start=1):
            label = format_segment_label(clip_name, idx)
            segment_map[label] = {
                "clip": clip_name,
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
            }
            prompt_lines.append(
                f"{label}: {seg['start']:.2f}-{seg['end']:.2f} | {seg['text']}"
            )

    if not prompt_lines:
        print("No transcript segments available to select from.")
        return []

    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY is not set. Keeping all segments in original order.")
        return [segment_map[label] for label in segment_map]

    openai.api_key = OPENAI_API_KEY
    prompt = (
        "You are given video segments from one or more clips. Each segment has a start/end time "
        "and the transcript text. The speaker is talking to camera with fragmented sentences and "
        "multiple subjects. Select the segments that should remain in the final streamlined "
        "storyline. Keep the result coherent and ordered. Output only a Python list of segment "
        "labels in final order, for example ['clip1_3', 'clip1_1']. Do not add any narrative text.\n\n"
        + "\n".join(prompt_lines)
    )

    print("Asking AI to choose the clearest storyline segments...")
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        labels = ast.literal_eval(response.choices[0].message.content.strip())
        if not isinstance(labels, list):
            raise ValueError("Expected a list of labels")

        for label in labels:
            if label in segment_map:
                selected_segments.append(segment_map[label])
            else:
                print(f"Warning: unknown label returned by AI: {label}")

        if not selected_segments:
            raise ValueError("No valid labels returned by AI")

        return selected_segments
    except Exception as e:
        print(f"OpenAI selection failed: {e}")
        print("Falling back to all segments in original order.")
        return [segment_map[label] for label in segment_map]


def edit_video(selected_segments, output_file):
    """Extract and concatenate selected segments into the final video."""
    if not selected_segments:
        print("No segments selected for the output video.")
        sys.exit(1)

    print(f"Extracting {len(selected_segments)} segments...")
    with tempfile.TemporaryDirectory() as tmpdir:
        segment_paths = []
        for i, item in enumerate(selected_segments):
            clip_path = os.path.join(VIDEO_DIR, item["clip"])
            start = max(0, float(item["start"]))
            duration = get_video_duration(clip_path)
            end = min(float(item["end"]), duration or float(item["end"]))
            
            if end <= start:
                print(f"Skipping invalid segment {item['clip']} {start}-{end}")
                continue
            
            segment_output = os.path.join(tmpdir, f"segment_{i:04d}.mp4")
            print(f"Extracting segment {i+1}/{len(selected_segments)}: {item['clip']} ({start:.2f}s - {end:.2f}s)")
            
            cmd = [
                "ffmpeg",
                "-i", clip_path,
                "-ss", str(start),
                "-to", str(end),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-preset", "ultrafast",
                "-crf", "23",
                "-y",
                segment_output,
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            segment_paths.append(segment_output)

        if not segment_paths:
            print("No valid segments available for final output.")
            sys.exit(1)

        print("Concatenating segments...")
        
        # Create a concat file
        concat_file = os.path.join(tmpdir, "concat.txt")
        with open(concat_file, 'w') as f:
            for seg_path in segment_paths:
                f.write(f"file '{os.path.abspath(seg_path)}'\n")

        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            "-y",
            output_file,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"FFmpeg concatenation failed: {result.stderr}")

        print(f"Edited video saved as {output_file}")


def main():
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

    generate_transcripts(VIDEO_DIR, TRANSCRIPT_DIR)
    segments_by_clip = load_segments(VIDEO_DIR, TRANSCRIPT_DIR)

    if not segments_by_clip:
        print("No timed transcript segments available. Add VTT or TXT transcripts and retry.")
        sys.exit(1)

    selected_segments = select_story_segments(segments_by_clip)
    if not selected_segments:
        print("No segments selected for the storyline.")
        sys.exit(1)

    print("Editing video into the coherent storyline...")
    edit_video(selected_segments, OUTPUT_FILE)


if __name__ == "__main__":
    main()
