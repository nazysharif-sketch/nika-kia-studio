import streamlit as st
import replicate

st.title("Nika AI Performance Dashboard 🎬")
st.subheader("Option A: Audio-Expression Engine")

singer1 = st.file_uploader("Upload Nika's Reference Image", type=["jpg", "png", "jpeg"])
audio_track = st.file_uploader("Upload Persian Humming Audio Track", type=["mp3", "wav", "mp4"])

# 🛠️ Our custom master dynamics bar mapped directly to the audio engine scale
motion_dynamics = st.slider(
    "Performance Movement Dynamics", 
    min_value=1.5, 
    max_value=3.5, 
    value=2.3, 
    step=0.1,
    help="Lower values allow her body and arms more room to gesture dynamically with the music!"
)

if st.button("Generate Performance"):
    if singer1 and audio_track:
        with st.spinner("Processing native audio physics..."):
            
            # Using the stable audio-to-video portrait animation schema
            output = replicate.run(
                "fofr/live-portrait:c961e6999a385744849a940428d052fcce9e2363160fc45610ec1f2cb17f6a73",
                input={
                    "face_image": singer1,
                    "driving_video": audio_track,  # Feeds your audio file safely
                    "live_portrait_scale": motion_dynamics,  # Controls her freedom of motion!
                    "live_portrait_vy_ratio": -0.12,
                    "live_portrait_stitching": True
                }
            )
            
            st.video(output)
    else:
        st.warning("Please upload both an image and an audio track to begin.")
