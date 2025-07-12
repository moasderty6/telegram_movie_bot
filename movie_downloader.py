import os
import subprocess

def download_torrent(torrent_url, download_path="downloads"):
    os.makedirs(download_path, exist_ok=True)
    try:
        subprocess.run(["aria2c", torrent_url, "-d", download_path], check=True)
        for file in os.listdir(download_path):
            if file.endswith(".mp4") or file.endswith(".mkv"):
                return os.path.join(download_path, file)
        return None
    except Exception as e:
        print(f"Error downloading torrent: {e}")
        return None

def cleanup_downloads(download_path="downloads"):
    for file in os.listdir(download_path):
        os.remove(os.path.join(download_path, file))