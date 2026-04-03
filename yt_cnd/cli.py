import argparse
import os
import sys
import shutil
import platform
import yt_dlp

def check_dependencies():
    """Pre-flight check to ensure system dependencies exist with cross-platform instructions."""
    missing = []
    
    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")
    if not shutil.which("node"):
        missing.append("node")

    if missing:
        current_os = platform.system()
        print("\n❌ Missing System Dependencies!")
        print("yt-CND requires external tools to merge video/audio and bypass bot protection.")
        
        if current_os == "Darwin": # macOS
            print("Please install them using Homebrew:")
            print(f"   brew install {' '.join(missing)}")
        elif current_os == "Windows":
            print("Please install them using Winget (Windows Package Manager):")
            for dep in missing:
                # Node.js has a specific package name in winget
                pkg = "OpenJS.NodeJS" if dep == "node" else dep
                print(f"   winget install {pkg}")
            print("\n(Or download manually from their official websites and add them to your system PATH)")
        else: # Linux
            print("Please install them using your distribution's package manager (e.g., apt):")
            print(f"   sudo apt install {' '.join(missing)}")
            
        sys.exit(1)

def main():
    # 1. Run the pre-flight check
    check_dependencies()

    # 2. Establish the universal Downloads folder
    default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    # 3. Set up terminal arguments
    parser = argparse.ArgumentParser(description="yt-CND: A lightning-fast, robust YouTube downloader for editors.")
    parser.add_argument("url", help="The YouTube URL to download")
    parser.add_argument("-o", "--output", default=default_downloads, help=f"Output folder (defaults to {default_downloads})")
    
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio only (converts to lossless WAV)")
    parser.add_argument("--max", action="store_true", help="Bypass 1080p cap and download absolute highest resolution (4K/8K)")
    
    args = parser.parse_args()
    
    url = args.url
    output_path = os.path.abspath(args.output)
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    print(f"\n🎬 yt-CND Initializing...")
    print(f"🔗 Target: {url}")
    print(f"📁 Destination: {output_path}")
    print(f"⚙️  Mode: {'Audio Only (WAV)' if args.audio else 'Video (Max)' if args.max else 'Video (1080p)'}\n")

    # 4. Configure dynamic yt-dlp options
    if args.audio:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav', 'preferredquality': '192'},
                {'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro', 'interaction', 'selfpromo']}
            ],
        }
    else:
        video_format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if args.max else 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        
        ydl_opts = {
            'format': video_format,
            'merge_output_format': 'mp4',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'postprocessors': [{
                'key': 'SponsorBlock',
                'categories': ['sponsor', 'intro', 'outro', 'interaction', 'selfpromo']
            }],
        }

    # 5. Execute download
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download complete! Media is ready for the timeline.")
    except Exception as e:
        print(f"\n❌ yt-CND encountered an error: {e}")

if __name__ == "__main__":
    main()
