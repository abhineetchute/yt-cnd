import argparse
import os
import sys
import shutil
import platform
import yt_dlp

def check_dependencies():
    """Pre-flight check for FFmpeg and Node."""
    missing = []
    if not shutil.which("ffmpeg"): missing.append("ffmpeg")
    if not shutil.which("node"): missing.append("node")
    if missing:
        current_os = platform.system()
        print("\n❌ Missing System Dependencies!")
        if current_os == "Darwin":
            print(f"   brew install {' '.join(missing)}")
        elif current_os == "Windows":
            for dep in missing:
                pkg = "OpenJS.NodeJS" if dep == "node" else dep
                print(f"   winget install {pkg}")
        sys.exit(1)

def main():
    check_dependencies()
    default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    parser = argparse.ArgumentParser(description="yt-CND: A filmmaker's YouTube downloader.")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("-o", "--output", default=default_downloads, help="Output folder")
    parser.add_argument("-a", "--audio", action="store_true", help="Audio only (WAV)")
    parser.add_argument("--max", action="store_true", help="4K/8K resolution")
    # Added a flag to adjust the limit if you ever want to change it on the fly
    parser.add_argument("--limit", default="5M", help="Rate limit (e.g. 5M, 10M). Default is 5M.")
    
    args = parser.parse_args()
    url = args.url
    output_path = os.path.abspath(args.output)
    
    download_playlist = False
    if "list=" in url:
        if "playlist?list=" in url:
            download_playlist = True
        else:
            print("\n🎵 Playlist data detected!")
            while True:
                choice = input("Download [p]laylist or [v]ideo? (p/v): ").strip().lower()
                if choice == 'p':
                    download_playlist = True
                    break
                elif choice == 'v':
                    download_playlist = False
                    break
                else:
                    print("Invalid choice.")

    os.makedirs(output_path, exist_ok=True)

    # UPDATED: Template uses %(playlist)s for better naming
    if download_playlist:
        out_template = os.path.join(output_path, '%(playlist)s', '%(title)s.%(ext)s')
    else:
        out_template = os.path.join(output_path, '%(title)s.%(ext)s')

    # UPDATED: Added 'ratelimit' to prevent Wi-Fi crashes
    ydl_opts = {
        'retries': 15,
        'fragment_retries': 15,
        'socket_timeout': 60,
        'ratelimit': args.limit, # Limits download speed to save your Wi-Fi
        'outtmpl': out_template,
        'noplaylist': not download_playlist,
    }

    if args.audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav', 'preferredquality': '192'},
                {'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro', 'interaction', 'selfpromo']}
            ],
        })
    else:
        v_format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if args.max else 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts.update({
            'format': v_format,
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'SponsorBlock',
                'categories': ['sponsor', 'intro', 'outro', 'interaction', 'selfpromo']
            }],
        })

    print(f"\n🎬 yt-CND Initializing...")
    print(f"🚀 Speed Limit: {args.limit}/s")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
