import yt_dlp
import os
from urllib.parse import urlparse, parse_qs

def master_playlist_downloader():
    # --- CONSTANT BASE PATH ---
    BASE_PATH = r"C:\Users\UserNmae\Desktop\Your_Workspace"

    print("--- MASTER YOUTUBE DOWNLOADER (Auto-Fallback: 1080 -> 720p -> 480p -> 360p) ---")
    print(f"Working in: {BASE_PATH}\n")

    # ==========================================
    # PHASE 1: COLLECT ALL INPUTS
    # ==========================================
    
    # 1. Playlist Link
    raw_url = input(">> 1. Paste the YouTube Playlist link: ").strip()
    if not raw_url:
        print("No link provided. Exiting.")
        return

    # 2. Text File Name
    txt_name = input(">> 2. Name for the links file (e.g. course_links): ").strip()
    if not txt_name:
        txt_name = "yt_links"
    if not txt_name.lower().endswith(".txt"):
        txt_name += ".txt"

    # 3. Video Folder Name
    folder_name = input(">> 3. Name for the videos folder (e.g. My_Course): ").strip()
    if not folder_name:
        folder_name = "Downloaded_Videos"

    # Define Full Paths
    txt_full_path = os.path.join(BASE_PATH, txt_name)
    video_output_path = os.path.join(BASE_PATH, folder_name)

    # ==========================================
    # PHASE 2: EXTRACT LINKS TO TXT
    # ==========================================
    print(f"\n[Phase 2] Analyzing Playlist...")
    
    parsed_url = urlparse(raw_url)
    query_params = parse_qs(parsed_url.query)
    if 'list' in query_params:
        playlist_id = query_params['list'][0]
        playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
    else:
        playlist_url = raw_url

    extract_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True
    }

    links = []
    try:
        with yt_dlp.YoutubeDL(extract_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if 'entries' in info:
                for video in info['entries']:
                    if video and video.get('id'):
                        links.append(f"https://www.youtube.com/watch?v={video['id']}")
            else:
                print("Error: Not a valid playlist.")
                return

        with open(txt_full_path, "w") as f:
            for link in links:
                f.write(link + "\n")
        
        print(f"--> Saved {len(links)} links to '{txt_name}'")

    except Exception as e:
        print(f"Extraction Error: {e}")
        return

    # ==========================================
    # PHASE 3: DOWNLOAD VIDEOS FROM TXT
    # ==========================================
    print(f"\n[Phase 3] Starting Download into '{folder_name}'...")
    print("(Robust Mode: Anti-Crash & Auto-Quality Fallback Active)")

    download_opts = {
        # --- QUALITY SETTING ---
        # 1. Look for MP4 format (Guarantees Sound).
        # 2. Look for Height <= 1080.
        # 3. 'best' automatically picks the highest available from that list.
        #    (If 1080p is missing, it picks 720p. If 720p missing, it picks 480p).
        'format': 'best[ext=mp4][height<=1080]',
        
        'outtmpl': f'{video_output_path}/%(title)s.%(ext)s',
        
        # --- ANTI-CRASH SETTINGS ---
        'restrictfilenames': True,
        'windowsfilenames': True,
        'retries': 20,
        'fragment_retries': 20,
        'file_access_retries': 20,
        'concurrent_fragment_downloads': 1,
        'ignoreerrors': True,
        'quiet': False,
    }

    try:
        with open(txt_full_path, 'r') as f:
            urls_to_download = [line.strip() for line in f if line.strip()]

        if not urls_to_download:
            print("Error: Link file is empty.")
            return

        with yt_dlp.YoutubeDL(download_opts) as ydl:
            ydl.download(urls_to_download)

        print("\n" + "="*40)
        print("SUCCESS! Job Complete.")
        print(f"1. Links saved:  {txt_full_path}")
        print(f"2. Videos saved: {video_output_path}")

    except Exception as e:
        print(f"Download Error: {e}")

if __name__ == "__main__":
    master_playlist_downloader()