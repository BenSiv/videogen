# Video Story Editor

A Python tool to programmatically edit MP4 files and generate a coherent storyline from fragmented videos and transcriptions using AI (OpenAI GPT-3.5) and FFmpeg.

## How It Works

1. **Load Transcripts**: Reads VTT subtitle files or auto-generates transcripts via Whisper.
2. **Parse Segments**: Extracts all timed speech segments from the transcription.
3. **AI Selection** (Optional): Uses GPT-3.5 to intelligently select the best segments that form a coherent narrative, removing filler and repetition.
4. **FFmpeg Extraction & Concatenation**: Efficiently extracts selected segments using FFmpeg and concatenates them into a streamlined video.

### Segment Selection Logic

- **With OpenAI API**: AI analyzes each segment's transcript and selects those that make narrative sense, removing dead air, repetitions, and off-topic sections.
- **Without API**: Uses all segments in order (for testing/fallback mode).

## Features
- Automatic transcription of MP4 files using Whisper (with timed segments).
- Support for VTT subtitle files for pre-existing transcriptions.
- AI-powered intelligent segment selection using GPT-3.5 (optional).
- FFmpeg-based segment extraction and concatenation for reliability and speed.
- Fallback mode when OpenAI API is unavailable.

## Prerequisites
- Python 3.8+
- FFmpeg and FFprobe (system-level binaries)
- OpenAI API key (optional; for intelligent segment selection)

## Installation
1. Clone or download this project.
2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Workflow

1. Place your fragmented MP4 video files in the `videos/` folder.
2. If you have pre-existing VTT transcripts, place them in the `transcripts/` folder with the same base filename as each clip.
   - Example: `videos/clip1.mp4` and `transcripts/clip1.vtt`
   - If VTT is missing, the script will transcribe audio with Whisper and generate timed segments automatically.
3. (Optional) Set your OpenAI API key for intelligent segment selection:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```
4. Run the script:
   ```
   python video_story_editor.py
   ```
5. The generated streamlined video will be saved as `coherent_storyline.mp4`.

### Example

```bash
# With API key for AI segment selection (smarter story curation)
export OPENAI_API_KEY="sk-..."
python video_story_editor.py

# Without API key (uses all segments in extracted order - faster)
python video_story_editor.py
```

## Output

- **Without API**: All transcript segments extracted and concatenated (reduces dead space between speech).
- **With API**: Only meaningful segments selected by AI, creating a tighter, more coherent narrative.

## Troubleshooting

- **"FFmpeg not found"**: Install FFmpeg:
  - Linux: `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **No segments extracted**: Ensure VTT or TXT transcripts are in the `transcripts/` folder with matching filenames to videos.
- **API quota exceeded**: Run the script without setting `OPENAI_API_KEY` to use fallback mode (all segments concatenated).
- **VideoClip read errors**: Video files should be valid MP4 files. Re-encode if needed: `ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4`

## License
MIT License