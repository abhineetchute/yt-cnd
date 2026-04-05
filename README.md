# yt-CND (Docu Editor's Youtube Downloader)

A lightning-fast, robust YouTube downloader designed specifically for filmmakers, documentarians, and video editors who need clean, high-quality assets without the hassle of ads, terminal clutter, or bot blocks.

## ✨ Features
* **1080p Standard:** Defaults to 1080p MP4—the "sweet spot" for proxy editing and high-quality references.
* **Smart Playlist Detection:** Automatically identifies playlists and offers an interactive choice to download the entire set or just the current video.
* **Automatic Organization:** Playlists are automatically saved into their own named sub-folders to keep your project directories clean.
* **Exact Filenames:** Saves files using the exact YouTube title. No random strings or numbers—just clean metadata for your project bins.
* **Bandwidth Throttling:** Includes a built-in rate limit to prevent crashing home/studio Wi-Fi during large batch downloads (Default: 5MB/s).
* **Bot-Block Bypass:** Integrates browser cookies and advanced JS runtimes (**Deno/Node**) to solve YouTube's "Sign in to confirm" errors using aggressive mobile spoofing.
* **SponsorBlock Integration:** Automatically strips out sponsors, intros, and self-promotions to give you clean, edit-ready footage.
* **Cinematic UI:** Hides chaotic backend terminal logs and displays a clean, single-line updating progress bar.

---

## 🛠 Installation

We have completely automated the setup process for fresh machines. You do not need to manually configure Homebrew, Python virtual environments, Node, or FFmpeg. 

### The 1-Line Setup
Open your Mac's **Terminal** app, paste this exact command, and hit Enter:

```bash
curl -sSL https://raw.githubusercontent.com/abhineetchute/yt-cnd/main/install.sh | bash
```

*Note: The script will safely install missing dependencies in the background, isolate the Python environment so it doesn't break your Mac, and link the command globally. You may be prompted for your Mac password once. When it says "Setup Complete," restart your terminal.*

---

## 🚀 Usage & Defaults

| Argument | Description | Default |
| :--- | :--- | :--- |
| `url` | The YouTube video or playlist link | **(Required)** |
| `-o`, `--output` | Destination folder for downloads | `~/Downloads` |
| `-a`, `--audio` | Download as lossless **WAV** instead of MP4 | Video (MP4) |
| `--max` | Bypass 1080p cap for **4K/8K** resolution | 1080p |
| `--limit` | Bandwidth throttle (e.g., `2M`, `5M`, `0` for none) | `5M` (5MB/s) |
| `--cookies` | Browser to pull session from (`chrome`, `safari`, `brave`) | None |

---

### 📂 Output Structure
The tool handles your library organization automatically based on the URL type:

* **Single Video:** `~/Downloads/Video Title.mp4`
* **Playlist:** `~/Downloads/Playlist Name/Video Title.mp4`

---

### Common Workflows

**Standard Download (1080p Proxy):**
```bash
yt-cnd "<YOUR YOUTUBE URL>"
```

**Bypass Bot Protection / Age Restrictions:**
*Ensure you are logged into YouTube in your chosen browser first.*
```bash
yt-cnd "<YOUR YOUTUBE URL>" --cookies chrome
```

**Custom Bandwidth Limit:**
Limit to 2MB/s to keep the Wi-Fi stable for others (Default is 5MB/s):
```bash
yt-cnd "<YOUR YOUTUBE URL>" --limit 2M
```
No limit (Full Speed / "The Nuclear Option"):
```bash
yt-cnd "<YOUR YOUTUBE URL>" --limit 0
```

**Audio Only (Lossless WAV for Sound Design):**
```bash
yt-cnd "<YOUR YOUTUBE URL>" -a
```

**Highest Quality (4K/8K for Master Shots):**
```bash
yt-cnd "<YOUR YOUTUBE URL>" --max
```

**Change the Download Directory:**
```bash
yt-cnd "<YOUR YOUTUBE URL>" -o ~/Desktop/MyFilmProject
```

---
**Candidates** coming soon. _Hopefully before GTA 6!_ ♘
