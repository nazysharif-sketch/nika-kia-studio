import streamlit as st
import replicate
import os
client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

st.set_page_config(page_title="Nika & Kia Studio", page_icon="🎤", layout="wide")
st.title("Nika & Kia Studio 🎤")
st.subheader("Advanced Lip-Sync & Humanization Terminal")

# --- 2. TOP BAR: MODE SELECTOR ---
mode = st.radio("Project Mode", ["Solo Mode", "Duet Mode"], horizontal=True)

# --- 3. LAYOUT COLUMNS ---
col1, col2, col3 = st.columns([1, 1.5, 1])

# --- LEFT COLUMN: FILE UPLOADS ---
with col1:
    st.header("Asset Uploads")
    singer1 = st.file_uploader("Upload Singer 1 Image (Nika)", type=["png", "jpg", "jpeg"])
    
    singer2 = None
    if mode == "Duet Mode":
        singer2 = st.file_uploader("Upload Singer 2 Image (Kia)", type=["png", "jpg", "jpeg"])
        
    audio_track = st.file_uploader("Upload Master Audio Track (Supports up to 7 mins)", type=["wav", "mp3"])

# --- CENTER COLUMN: STUDIO CONTROLS & SLIDERS ---
with col2:
    st.header("Studio Controls")
    prompt = st.text_area("Video Director Prompt", placeholder="Describe the video mood, background scenery, and interactions here (e.g., Summer Salsa in Capri)...")
    
    st.markdown("### Humanization Engine")
    sharpness = st.slider("Lip-Sync Sharpness Multiplier", 0, 100, 100)
    intensity = st.slider("Expression Intensity", 0, 100, 75)
    
    blink_engine = st.checkbox("Natural Blink Engine", value=True)
    gaze_humanization = st.checkbox("Micro-Gaze Humanization", value=True)
    interaction = st.checkbox("Character Inter-Eye Contact (Duet Only)", value=mode == "Duet Mode")

# --- RIGHT COLUMN: QUALITY & RENDER ---
with col3:
    st.header("Master Render")
    resolution = st.selectbox("Select Render Quality", ["Download Full HD (1080p)", "Download Ultra HD (4K Master)"])
    
    # THE MAIN GENERATE BUTTON
    if st.button("🚀 GENERATE MUSIC VIDEO", use_container_width=True):
        if not singer1 or not audio_track:
            st.error("Missing Assets! Please make sure you have uploaded at least Singer 1's image and an audio track.")
        else:
            st.warning("Connecting to Replicate servers... Processing humanized lip-sync animation.")
     singer1.seek(0)
     audio_track.seek(0)
     try:
            try:
                # This kicks off the actual AI processing on Replicate's servers
                output = client.run(
                    "devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef",
                    input={
         "face": singer1,
         "audio": audio_track,
         "pads": "0 10 0 0"  # Automatically helps with natural lip padding
     }
                )
                
                st.success("Render Complete!")
                st.video(output) # Displays your working video with audio right on your screen!
                
            except Exception as e:
                st.error(f"Something went wrong during generation: {e}")
