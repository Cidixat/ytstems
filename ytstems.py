import os
import subprocess
from yt_dlp import YoutubeDL


def download_audio(url, output_dir="processed"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    mp3_files = [f for f in os.listdir(output_dir) if f.endswith(".mp3")]
    if not mp3_files:
        raise RuntimeError("Download failed — no MP3 found in output directory.")
    return os.path.join(output_dir, mp3_files[0])


def split_stems(input_audio, output_dir="processed"):
    filename, _ = os.path.splitext(os.path.basename(input_audio))
    unique_output_dir = os.path.join(output_dir, f"{filename}_demux")
    os.makedirs(unique_output_dir, exist_ok=True)
    subprocess.run(
        ["demucs", input_audio, "-o", unique_output_dir, "-n", "mdx_extra"],
        check=True
    )
    stems_dir = os.path.join(unique_output_dir, "mdx_extra", filename)
    return stems_dir


def process(url, output_dir="processed"):
    mp3_path = download_audio(url, output_dir)
    stems_dir = split_stems(mp3_path, output_dir)
    return mp3_path, stems_dir


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    mp3, stems = process(url)
    print(f"MP3: {mp3}")
    print(f"Stems: {stems}")
