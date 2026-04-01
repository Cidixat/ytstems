# ytstems

Downloads audio from a YouTube URL and splits it into separate stems using [Demucs](https://github.com/facebookresearch/demucs). Includes both a CLI and a Gradio web UI.

## How it works

1. Paste a YouTube URL into the web UI (or run via CLI)
2. Downloads the best available audio as an MP3 via `yt-dlp`
3. Runs `demucs` to separate the audio into stems
4. Saves everything under the `processed/` directory

Choose between two modes:
- 4-stem — vocals, drums, bass, other (`htdemucs_ft`)
- 6-stem — vocals, drums, bass, other, guitar, piano (`htdemucs_6s`)

Output structure:
```
processed/
  <video title>/
    <video title>.mp3
    htdemucs_ft/
      vocals.wav
      drums.wav
      bass.wav
      other.wav
```

## Requirements

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/download.html) installed and on your PATH

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

**Web UI**
```bash
python app.py
# Opens at http://localhost:7860
```

**CLI**
```bash
python ytstems.py
# Enter YouTube URL: https://www.youtube.com/watch?v=...
```

## Dependencies

| Package | Purpose |
|---|---|
| yt-dlp | YouTube audio download |
| demucs | AI-powered audio source separation |
| torch / torchaudio | ML backend for demucs |
| ffmpeg | Audio conversion |
| gradio | Web UI |
