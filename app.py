import streamlit as st
import os
import yt_dlp
import tempfile
import shutil

# Page Setup
st.set_page_config(page_title="yt-CND Downloader", page_icon="🎬", layout="centered")
st.title("🎬 yt-CND Downloader")
st.markdown("Paste a YouTube link below to get clean, proxy-ready assets.")

# UI Inputs
url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("Format", ["Video (1080p MP4)", "Video (Max Quality)", "Audio Only (WAV)"])
with col2:
    browser_cookie = st.selectbox("Bypass Bot Block?", ["None", "Chrome", "Safari", "Firefox"])

# Logic
if st.button("🚀 Process Download", use_container_width=True):
    if not url:
        st.error("Please enter a URL.")
    else:
        # Create a temporary folder to hold the file while it processes
        temp_dir = tempfile.mkdtemp()
        
        with st.status("Processing Video... (This may take a minute)", expanded=True) as status:
            try:
                # 1. Configure Options
                st.write("Initializing secure connection...")
                out_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
                
                ydl_opts = {
                    'outtmpl': out_template,
                    'noplaylist': True, # Keep it to single videos for the web UI to avoid ZIP complexities
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                    'javascript_runtimes': ['node'], # Node is easiest for Docker
                    'allow_unsecure_tools': True,
                    'remote_components': ['ejs:github'],
                    'extractor_args': {'youtube': {'player_client': ['android', 'ios', 'web'], 'skip': ['dash', 'hls']}},
                }

                if browser_cookie != "None":
                    ydl_opts['cookiesfrombrowser'] = (browser_cookie.lower(),)

                if format_type == "Audio Only (WAV)":
                    ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'wav'}]})
                elif format_type == "Video (Max Quality)":
                    ydl_opts.update({'format': 'bestvideo+bestaudio', 'merge_output_format': 'mp4'})
                else:
                    ydl_opts.update({'format': 'bestvideo[height<=1080]+bestaudio', 'merge_output_format': 'mp4'})

                # 2. Download the file
                st.write("Downloading and merging streams via FFmpeg...")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    # Get the exact filename yt-dlp generated
                    downloaded_file = ydl.prepare_filename(info_dict)
                    
                    if format_type == "Audio Only (WAV)":
                        downloaded_file = downloaded_file.rsplit('.', 1)[0] + '.wav'

                status.update(label="✅ Ready for Download!", state="complete", expanded=False)

                # 3. Provide the Download Button to the User's Browser
                with open(downloaded_file, "rb") as file:
                    st.success("Success! Click below to save to your computer.")
                    st.download_button(
                        label="⬇️ Download File",
                        data=file,
                        file_name=os.path.basename(downloaded_file),
                        mime="video/mp4" if "Video" in format_type else "audio/wav",
                        use_container_width=True
                    )
            
            except Exception as e:
                status.update(label="❌ Error Encountered", state="error")
                st.error(f"Error details: {e}")
