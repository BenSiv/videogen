import sys
import os
import tempfile
import subprocess
from video_story_editor import parse_timestamp, get_video_duration, edit_video

def parse_vtt_with_ids(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    segments = {}
    current_id = None
    start = None
    end = None
    current_text = []

    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT":
            continue
        if "-->" in line:
            parts = line.split("-->")
            start = parse_timestamp(parts[0].strip())
            end = parse_timestamp(parts[1].strip())
            continue
        
        # if it's the ID line
        if "/" in line and "-" in line and len(line) > 20: 
            if current_id is not None and start is not None:
                segments[current_id] = {
                    "start": start,
                    "end": end,
                    "text": " ".join(current_text).strip(),
                    "clip": "clip1.mp4"
                }
            current_id = line.split("/")[-1].strip()
            start = None
            end = None
            current_text = []
            continue
            
        if start is not None:
            current_text.append(line)
        
    if current_id is not None and start is not None:
        segments[current_id] = {
            "start": start,
            "end": end,
            "text": " ".join(current_text).strip(),
            "clip": "clip1.mp4"
        }
    return segments

def main():
    vtt_file = "transcripts/clip1.vtt"
    segments = parse_vtt_with_ids(vtt_file)
    
    ordered_ids = [
        "16-0", "16-1", "18-0", "19-0", "20-0", "20-1",
        "21-0", "21-1", "21-2", "28-0", "28-1", "30-0", "30-1",
        "37-0", "37-1", "38-0", "38-1", "40-0", "41-0", "42-0",
        "43-0", "23-0", "23-1", "54-0", "55-0", "56-0", "56-1",
        "56-2", "56-3", "57-0", "57-1", "57-2", "58-0", "60-0",
        "61-0", "61-1", "62-0", "63-0", "63-1", "63-2", "63-3",
        "64-0", "65-0", "65-1", "66-0", "66-1", "66-2", "67-0",
        "67-1", "68-0", "69-0", "70-0", "71-0", "72-0", "73-0",
        "74-0", "75-0", "75-1", "76-0", "76-1", "76-2", "77-0",
        "77-1", "77-2", "78-0", "79-0", "80-0", "81-0", "81-1",
        "87-0", "87-1", "88-0", "115-0", "116-0", "117-0", "118-0",
        "118-1", "118-2", "119-0", "119-1", "120-0", "120-1", "120-2",
        "121-0", "121-1", "122-0", "123-0", "123-1", "123-2", "123-3",
        "124-0", "124-1", "124-2", "124-3", "125-0", "125-1", "125-2",
        "126-0", "126-1", "127-0", "127-1", "89-0", "89-1", "90-0",
        "93-0", "94-0", "95-0", "97-0", "98-0", "101-0", "104-0",
        "104-1", "105-0", "105-1", "106-0", "107-0", "107-1", "108-0",
        "109-0", "111-0", "112-0", "112-1", "113-0", "114-0", "128-0",
        "128-1", "131-0", "131-1", "131-2", "24-0", "24-1", "25-0",
        "133-0", "134-0", "135-0", "136-0", "137-0", "138-0", "139-0",
        "140-0", "140-1"
    ]
    
    selected_segments = []
    for sid in ordered_ids:
        if sid in segments:
            selected_segments.append(segments[sid])
        else:
            print(f"Warning: Segment {sid} not found in VTT.")
            
    print(f"Total segments to extract: {len(selected_segments)}")
    
    if not os.path.exists("videos/clip1.mp4"):
        print("videos/clip1.mp4 not found!")
        return
        
    edit_video(selected_segments, "refactored_video.mp4")
    print("Done. Video saved as refactored_video.mp4")

if __name__ == "__main__":
    main()
