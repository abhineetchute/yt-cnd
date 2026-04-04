import streamlit as st
import requests

st.set_page_config(page_title="yt-CND Downloader", page_icon="🎬", layout="centered")
st.title("🎬 yt-CND Downloader")
st.markdown("Cloud-based proxy acquisition network.")

url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

format_type = st.selectbox("Format", ["Video (1080p)", "Audio Only (MP3/WAV)"])

if st.button("🚀 Process Download", use_container_width=True):
    if not url:
        st.error("Please enter a URL.")
    else:
        with st.status("Acquiring secure download link...", expanded=True) as status:
            # The updated v11 API Payload parameters
            payload = {
                "url": url,
                "videoQuality": "1080",
                "filenameStyle": "classic"
            }
            
            if "Audio" in format_type:
                payload["downloadMode"] = "audio"
                payload["audioFormat"] = "mp3"
            else:
                payload["downloadMode"] = "auto"

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                # The disguise that got us past the bot-blocker
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            # The Fallback Network: Main v11 endpoint + Community Hosted Nodes
            api_nodes = [
                "https://api.cobalt.tools/",
                "https://cobalt-api.kwiatekmiki.com/",
                "https://api.cobalt.mywire.org/",
                "https://cobalt.qewertyy.dev/"
            ]

            success = False
            for node in api_nodes:
                if success: break
                st.write(f"Connecting to node: {node}...")
                try:
                    # Send request to the current node in the loop
                    response = requests.post(node, json=payload, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # v11 successfully returns a 'url' key with the direct download link
                        if "url" in data:
                            download_url = data.get("url")
                            status.update(label="✅ Link Generated!", state="complete", expanded=False)
                            st.success("File is ready! Click below to download directly to your machine.")
                            
                            # The big red download button
                            st.markdown(f'<a href="{download_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#ff4b4b; color:white; border:none; border-radius:5px; cursor:pointer;">⬇️ Download File</button></a>', unsafe_allow_html=True)
                            success = True
                            break
                        else:
                            st.write("Unexpected response format. Rerouting...")
                    else:
                        st.write(f"Node busy (Status {response.status_code}). Rerouting...")
                except Exception as e:
                    st.write("Node offline or unreachable. Rerouting...")

            if not success:
                status.update(label="❌ Acquisition Failed", state="error")
                st.error("All proxy nodes are currently rejecting the connection or are overloaded. Please try again in a few minutes.")
