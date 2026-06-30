import streamlit as st
import replicate

st.title("Nika AI Performance Dashboard 🎬")
st.subheader("Original VEED Native Audio Engine")

singer1 = st.file_uploader("Upload Nika's Reference Image", type=["jpg", "png", "jpeg"])
audio_track = st.file_uploader("Upload Persian Humming Audio Track", type=["mp3", "wav", "m4a", "aac"])

# VEED natively handles social influencer & performance styles over audio data
if st.button("Generate Performance"):
    if singer1 and audio_track:
        with st.spinner("VEED Fabric 1.0 animating native vocal physics..."):
            
            # Using the official, ultra-stable VEED model pipeline on Replicate
            output = replicate.run(
                "veed/fabric-1.0:7e0cb3a0d5109b0a1d47a3297a7e8ea13d33261cb17fa830d17d591f7c43300a", # Standard stable version
                input={
                    "image": singer1,
                    "audio": audio_track,
                    "resolution": "720p"  # Pristine output quality for Instagram Reels
                }
            )
            
            # Since VEED returns the direct video file link or dictionary structure
            st.video(output)
    else:
        st.warning("Please upload both an image and an audio track to begin.")
