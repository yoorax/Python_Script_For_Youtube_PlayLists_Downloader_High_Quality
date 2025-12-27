# YouTube Playlist Master Downloader

**Language:** Python 3.x  
**Core Library:** yt-dlp

## Overview
This project is a robust automation tool designed to archive entire desired YouTube playlists for offline use. It was engineered specifically to handle unstable internet connections and prevent common Windows filesystem locking errors during large batch downloads.

The script automates the entire pipeline:
- Extracting video links from a playlist  
- Saving them to a local manifest  
- Downloading them in an optimized format suitable for technical tutorials (clear text/diagrams but low file size)

## Key Features
- **Smart Quality Control:** Prioritizes 1080p (FHD) for clarity but automatically falls back to 480p or 360p if FHD is unavailable.  
- **Anti-Crash Robust Mode:** Engineered with a single-fragment download logic to bypass `[WinError 32]`, preventing Windows Defender/Antivirus from locking files and crashing the script during write operations.  
- **Sound Guarantee:** Enforces the `.mp4` container format to ensure audio and video are perfectly merged (avoids the common *silent video* issue with raw streams).  
- **Automated Organization:** Handles file naming, removes illegal characters (e.g., `|`, `?`), and organizes outputs into specific workspace directories.  
- **Resume Capability:** If the internet cuts out, the script can be restarted and will resume exactly where it left off.

## Prerequisites
You need Python installed on your machine. The script relies on the `yt-dlp` library.

```bash
pip install yt-dlp
```
Usage (Important Note!)
Configure the Workspace
Open the script and update the BASE_PATH variable to your desired download location:

```python
BASE_PATH = r"C:\Users\YourName\Desktop\Your_Workspace"
```
### Follow the Prompts
Input 1: Paste the YouTube Playlist URL
(format should be https://www.youtube.com/playlist?list=...)

Input 2: Name the text file
(stores the extracted links of each video in the playlist as a .txt file)

Input 3: Name the folder where videos will be saved
(the folder will be created automatically; only provide the desired name)

## How It Works (The Logic)
The script operates in two distinct phases:

Phase 1 – Extraction
Uses extract_flat to quickly scrape playlist metadata without downloading large files, creating a persistent .txt list of video URLs.

Phase 2 – Acquisition
Iterates through the text file using the format selector:

``` python
best[ext=mp4][height<=1080]
```
This logic acts as a filter:
“Give me the best MP4 available.”

License
This project is for educational purposes and personal archiving of open courseware. For people in rural places with poor internet.
