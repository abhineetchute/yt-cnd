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
            try:
                # Setup the request to the Cobalt API network
                api_url = "https://api.cobalt.tools/api/json"
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    # THE FIX: Spoof a real Mac browser so the API doesn't block the Python script
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                }
                payload = {
                    "url": url,
                    "vQuality": "1080",
                    "filenamePattern": "classic"
                }

                if "Audio" in format_type:
                    payload["isAudioOnly"] = True

                # Send request
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "stream" or data.get("status") == "redirect":
                        download_url = data.get("url")
                        status.update(label="✅ Link Generated!", state="complete", expanded=False)
                        
                        st.success("File is ready! Click below to download directly to your machine.")
                        st.markdown(f'<a href="{download_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#ff4b4b; color:white; border:none; border-radius:5px; cursor:pointer;">⬇️ Download File</button></a>', unsafe_allow_html=True)
                    else:
                        status.update(label="❌ API Error", state="error")
                        st.error(f"The acquisition network couldn't process this link. Response: {data}")
                else:
                    status.update(label="❌ Network Error", state="error")
                    # NEW: Exact error reporting so we know exactly why it failed
                    st.error(f"Connection blocked by API. (Status Code: {response.status_code})")
                    st.write("Server Response details:", response.text)
            
            except Exception as e:
                status.update(label="❌ Error Encountered", state="error")
                st.error(f"Error details: {e}")
