import argparse
import os
import sys
import shutil
import platform
import yt_dlp

def check_dependencies():
    """Pre-flight check for FFmpeg and a JS Runtime (Deno or Node)."""
    has_ffmpeg = shutil.which("ffmpeg")
    has_js = shutil.which("deno") or shutil.which("node")

    if not has_ffmpeg or not has_js:
        print("\n❌ Missing System Dependencies!")
        print("yt-CND requires FFmpeg and a JavaScript runtime (Deno or Node) to function.")
        current_os = platform.system()
        if current_os == "Darwin":
            print("👉 Run: brew install ffmpeg deno")
        sys.exit(1)

def parse_limit(limit_str):
    """Converts '5M' or '500K' string to a float for yt-dlp."""
    if not limit_str or limit_str == "0":
        return None
    try:
        if limit_str.lower().endswith('m'):
            return float(limit_str[:-1]) * 1024 * 1024
        if limit_str.lower().endswith('k'):
            return float(limit_str[:-1]) * 1024
        return float(limit_str)
    except ValueError:
        return None

def main():
    check_dependencies()
    default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    parser = argparse.ArgumentParser(description="yt-CND: A filmmaker's YouTube downloader.")
    parser.add_argument("url", help="YouTube URL")
    parser.add_argument("-o", "--output", default=default_downloads, help="Output folder")
    parser.add_argument("-a", "--audio", action="store_true", help="Audio only (WAV)")
    parser.add_argument("--max", action="store_true", help="4K/8K resolution")
    parser.add_argument("--limit", default="5M", help="Rate limit (e.g. 5M, 10M). Default is 5M.")
    parser.add_argument("--cookies", help="Browser to pull cookies from (e.g., chrome, safari, brave, firefox)")
    
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
    
    # Template logic
    if download_playlist:
        out_template = os.path.join(output_path, '%(playlist_title,playlist)s', '%(title)s.%(ext)s')
    else:
        out_template = os.path.join(output_path, '%(title)s.%(ext)s')

    # Logic for speed limit
    rate_limit = parse_limit(args.limit)

    ydl_opts = {
        'retries': 15,
        'fragment_retries': 15,
        'socket_timeout': 60,
        'ratelimit': rate_limit,
        'outtmpl': out_template,
        'noplaylist': not download_playlist,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'javascript_runtimes': ['deno', 'node'],
        'allow_unsecure_tools': True,
        'remote_components': ['ejs:github'],
    }

    if args.cookies:
        ydl_opts['cookiesfrombrowser'] = (args.cookies,)

    if args.audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav', 'preferredquality': '192'},
                               {'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro', 'interaction', 'selfpromo']}],
        })
    else:
        v_format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if args.max else 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts.update({
            'format': v_format,
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro', 'interaction', 'selfpromo']}],
        })

    print(f"\n🎬 yt-CND Initializing...")
    print(f"🚀 Speed Limit: {args.limit if rate_limit else 'Unlimited'}")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download complete!")
    except Exception as e:
        print(f"\n❌ yt-CND encountered an error: {e}")

if __name__ == "__main__":
    main()
