# ytstems

A CLI tool that downloads audio from a YouTube URL and splits it into separate stems (vocals, drums, bass, other) using [Demucs](https://github.com/facebookresearch/demucs).

## How it works

1. Prompts you for a YouTube URL
2. Downloads the best available audio as an MP3 via `yt-dlp`
3. Runs `demucs` (mdx_extra model) to separate the audio into 4 stems
4. Saves everything under the `processed/` directory

Output structure:
```
processed/
  <video title>.mp3
  <video title>_demux/
    mdx_extra/
      <video title>/
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
