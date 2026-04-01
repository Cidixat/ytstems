import os
import shutil
import subprocess
from yt_dlp import YoutubeDL


MODELS = {
    "4-stem — fast (vocals, drums, bass, other)": "htdemucs",
    "4-stem — best quality (vocals, drums, bass, other)": "htdemucs_ft",
    "6-stem — best quality, piano experimental (vocals, drums, bass, other, guitar, piano)": "htdemucs_6s",
}


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
    # Use a temp dir so demucs doesn't nest inside track_dir directly
    tmp_dir = os.path.join(track_dir, "_tmp_demucs")
    subprocess.run(
        ["demucs", input_audio, "-o", tmp_dir, "-n", model],
        check=True
    )
    # demucs outputs to: tmp_dir/<model>/<filename>/
    filename, _ = os.path.splitext(os.path.basename(input_audio))
    nested_dir = os.path.join(tmp_dir, model, filename)
    stems_dir = os.path.join(track_dir, model)
    os.makedirs(stems_dir, exist_ok=True)

    # Move wav files to track_dir/<model>/
    for f in os.listdir(nested_dir):
        shutil.move(os.path.join(nested_dir, f), os.path.join(stems_dir, f))
    shutil.rmtree(tmp_dir)

    return stems_dir


def process(url, stem_option="4-stem — fast (vocals, drums, bass, other)", output_dir="processed"):
    model = MODELS[stem_option]
    mp3_path, track_dir = download_audio(url, output_dir)
    stems_dir = split_stems(mp3_path, track_dir, model)
    return mp3_path, stems_dir


def process_file(file_path, stem_option="4-stem — fast (vocals, drums, bass, other)", output_dir="processed"):
    model = MODELS[stem_option]
    filename, _ = os.path.splitext(os.path.basename(file_path))
    track_dir = os.path.join(output_dir, filename)
    os.makedirs(track_dir, exist_ok=True)

    # Copy the uploaded file into the track folder
    dest = os.path.join(track_dir, os.path.basename(file_path))
    shutil.copy(file_path, dest)

    stems_dir = split_stems(dest, track_dir, model)
    return dest, stems_dir


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    mp3, stems = process(url)
    print(f"MP3: {mp3}")
    print(f"Stems: {stems}")
