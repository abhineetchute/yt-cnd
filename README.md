# yt-CND: The Filmmaker's YouTube Downloader

A lightning-fast, robust command-line tool designed to download high-quality video and audio from YouTube. Built specifically for video editors, it natively integrates SponsorBlock to automatically cut out baked-in ads and perfectly synchronizes highest-quality streams for non-linear editors (NLEs) like Premiere Pro.

## ✨ Features
* **Smart Quality:** Defaults to max 1080p to prevent accidental multi-gigabyte 4K downloads, with a `--max` flag to override when archival 4K/8K resolution is needed.
* **Lossless Audio:** One-flag extraction of pristine, uncompressed WAV audio (avoids timeline drift caused by MP3 variable bitrates).
* **Interactive Playlist Detection:** If you paste a link that contains a playlist, the tool will automatically ask if you want to download the single video or the entire playlist. Playlists are automatically saved into their own named folders.
* **SponsorBlock Integration:** Automatically detects and strips sponsored segments out of the final video file.
* **Smart Defaults:** Drops files directly into your system's `Downloads` folder automatically. Cross-platform compatible (macOS & Windows).

## 🛠️ Prerequisites

`yt-CND` requires two system-level libraries to merge streams and decrypt bot protection.

**For macOS (via Homebrew):**
```bash
brew install ffmpeg node
```

**For Windows (via Winget in PowerShell):**
```powershell
winget install ffmpeg
winget install OpenJS.NodeJS
```

## 📦 Installation

To install `yt-CND` globally on your machine directly from GitHub, run:

```bash
pip install git+https://github.com/abhineetchute/yt-cnd.git
```
*(If installing from source locally, navigate to the project directory and run `pip install .`)*

## 🚀 Usage

Using the tool is as simple as calling `yt-cnd` followed by your URL. By default, it will drop a 1080p MP4 file into your `Downloads` folder.

**Standard 1080p Download:**
```bash
yt-cnd "<YOUR_YOUTUBE_URL>"
```

**Audio-Only (WAV extraction for editing):**
```bash
yt-cnd "<YOUR_YOUTUBE_URL>" -a
```

**Maximum Available Resolution (Bypass 1080p cap):**
```bash
yt-cnd "<YOUR_YOUTUBE_URL>" --max
```

**Custom Output Directory:**
```bash
yt-cnd "<YOUR_YOUTUBE_URL>" -o /path/to/custom/folder
```

**Download a Playlist:**
(Automatically detects the playlist, asks for confirmation, and creates a sub-folder)
```text
yt-cnd "<YOUR_YOUTUBE_PLAYLIST_URL>"
```

## 📝 Disclaimer
Please respect copyright laws and YouTube's Terms of Service. This tool is designed for downloading royalty-free material, creative commons footage, and archival material for fair use documentary editing.
```
