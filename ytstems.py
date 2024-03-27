import os
import subprocess

url = input("Enter YouTube URL: ")

def download_audio_from_youtube(url, output_dir):
    try:
        # Download audio using yt-dlp
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", url, "-o", f"{output_dir}/%(title)s.%(ext)s"])
        print("Audio downloaded successfully!")
    except Exception as e:
        print(f"Error downloading audio: {e}")

def split_audio_with_demucs(input_audio, output_dir):
    try:
        # Split audio using demucs
        subprocess.run(["demucs", input_audio, "-o", output_dir])
        print("Audio split into separate tracks!")
    except Exception as e:
        print(f"Error splitting audio: {e}")

if __name__ == "__main__":
    youtube_url = url
    output_directory = "output_audio_tracks"

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Download audio from YouTube
    download_audio_from_youtube(youtube_url, output_directory)

    # Split audio into separate tracks using demucs
    input_audio_file = f"{output_directory}/{os.listdir(output_directory)[0]}"
    split_audio_with_demucs(input_audio_file, output_directory)