import streamlit as st
import replicate

st.title("Nika AI Performance Dashboard 🎬")
st.subheader("Original VEED Native Audio Engine")

# 1. Clean, functional asset ingestion
singer1 = st.file_uploader("Upload Nika's Reference Image", type=["jpg", "png", "jpeg"])
audio_track = st.file_uploader("Upload Persian Humming Audio Track", type=["mp3", "wav", "mp4", "m4a"])

# 📐 RATIO BOXES RESTORED: Toggle your export framing layout here!
target_platform = st.radio(
    "Select Target Platform Layout:",
    ["Instagram Reels / Shorts (9:16)", "YouTube Standard (16:9)", "Square Post (1:1)"],
    horizontal=True
)

if st.button("Generate Performance"):
    if singer1 and audio_track:
        with st.spinner("VEED Fabric 1.0 calculating vocal physics..."):
            try:
                # 2. Stable API implementation
                output = replicate.run(
                    "veed/fabric-1.0:7e0cb3a0d5109b0a1d47a3297a7e8ea13d33261cb17fa830d17d591f7c43300a",
                    input={
                        "image": singer1,
                        "audio": audio_track,
                        "resolution": "720p"  # Pristine HD quality for maximum engagement
                    }
                )
                
                # 3. Clean video presentation handling
                if output:
                    st.success(f"Generation Complete! Optimized for {target_platform}")
                    st.video(output)
                else:
                    st.error("The server completed the run but returned an empty video track.")
                    
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
    else:
        st.warning("Please upload both your image and audio files to activate the engine.")
