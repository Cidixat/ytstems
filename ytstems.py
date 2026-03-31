import os
from yt_dlp import YoutubeDL
import subprocess

url = input("Enter YouTube URL: ")

def get_video_title_directly(url):
   try:
       with YoutubeDL({"outtmpl": "%(id)s.%(ext)s"}) as ydl:
           info_dict = ydl.extract_info(url, download=False)
           return info_dict.get("title")
   except Exception as e:
       print(f"Error extracting video title: {e}")
       return None


video_title = get_video_title_directly(url)

def download_audio_directly(url, output_dir):
   try:
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
       print("Audio downloaded successfully!")
   except Exception as e:
       print(f"Error downloading audio: {e}")

def split_audio_with_demucs(input_audio, output_dir):
    # Extract filename without extension
    filename, _ = os.path.splitext(os.path.basename(input_audio))
    # Create unique output directory with filename
    unique_output_dir = os.path.join(output_dir, f"{filename}_demux")
    os.makedirs(unique_output_dir, exist_ok=True)

    try:
        # Split audio using demucs with the new directory
        subprocess.run(["demucs", input_audio, "-o", unique_output_dir, "-n", "mdx_extra"])
        print("Audio split into separate tracks!")
    except Exception as e:
        print(f"Error splitting audio: {e}")

if __name__ == "__main__":
    youtube_url = url
    output_directory = "processed"

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Download audio from YouTube
    download_audio_directly(youtube_url, output_directory)

    # Find the downloaded mp3 and split into stems
    mp3_files = [f for f in os.listdir(output_directory) if f.endswith(".mp3")]
    if not mp3_files:
        print("No MP3 file found in output directory. Download may have failed.")
    else:
        input_audio_file = os.path.join(output_directory, mp3_files[0])
        split_audio_with_demucs(input_audio_file, output_directory)