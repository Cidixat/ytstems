import os
import subprocess
from yt_dlp import YoutubeDL


def download_audio(url, output_dir="processed"):
    os.makedirs(output_dir, exist_ok=True)

    # First extract the title so we can create the named folder
    with YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "unknown")

    track_dir = os.path.join(output_dir, title)
    os.makedirs(track_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": f"{track_dir}/%(title)s.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    mp3_files = [f for f in os.listdir(track_dir) if f.endswith(".mp3")]
    if not mp3_files:
        raise RuntimeError("Download failed — no MP3 found in output directory.")
    return os.path.join(track_dir, mp3_files[0]), track_dir


def split_stems(input_audio, track_dir, model="htdemucs_ft"):
    subprocess.run(
        ["demucs", input_audio, "-o", track_dir, "-n", model],
        check=True
    )
    filename, _ = os.path.splitext(os.path.basename(input_audio))
    nested_dir = os.path.join(track_dir, model, filename)
    stems_dir = os.path.join(track_dir, model)

    # Flatten: move wav files up one level, remove the nested folder
    for f in os.listdir(nested_dir):
        os.rename(os.path.join(nested_dir, f), os.path.join(stems_dir, f))
    os.rmdir(nested_dir)

    return stems_dir


def process(url, stem_option="4-stem (vocals, drums, bass, other)", output_dir="processed"):
    model = MODELS[stem_option]
    mp3_path, track_dir = download_audio(url, output_dir)
    stems_dir = split_stems(mp3_path, track_dir, model)
    return mp3_path, stems_dir


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    mp3, stems = process(url)
    print(f"MP3: {mp3}")
    print(f"Stems: {stems}")
