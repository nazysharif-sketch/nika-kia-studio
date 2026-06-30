import streamlit as st
import replicate

# 1. Clear, streamlined UI for your core parameters
st.title("Nika AI Performance Dashboard 🎬")
st.subheader("Option A: Expression & Native Gesture Engine")

singer1 = st.file_uploader("Upload Nika's Reference Image", type=["jpg", "png", "jpeg"])
audio_track = st.file_uploader("Upload Persian Humming Audio Track", type=["mp3", "wav", "mp4"])

# 🛠️ THE NEW DIRECT INTENSITY DIAL:
# Pushing this to the lower end (1.5 - 1.9) opens up the tracking window to allow big arm movements.
# Pushing this to the higher end (2.5 - 3.0) tightens the frame to keep her incredibly steady.
motion_dynamics = st.slider(
    "Performance Movement Dynamics", 
    min_value=1.5, 
    max_value=3.0, 
    value=2.3, 
    step=0.1,
    help="Lower values expand the canvas allowing her arms to gesture dynamically with the audio swells."
)

if st.button("Generate Performance"):
    if singer1 and audio_track:
        with st.spinner("Processing native audio physics..."):
            
            # 2. Securely execute the targeted Replicate run
            output = replicate.run(
                "okaris/live-portrait:8be2edeab144ba0865f9fa84168f621ee417a2003db947802f900519f7c43300",
                input={
                    "source_image": singer1,
                    "driving_audio": audio_track,
                    "flag_stitching": True,
                    "flag_remap": True,
                    
                    # Target Nika explicitly and freeze the pianist
                    "input_face_index": 0, 
                    
                    # Driven directly by your new frontend slider control!
                    "scale": motion_dynamics,
                    "vy_ratio": -0.125
                }
            )
            
            st.video(output)
    else:
        st.warning("Please upload both an image and an audio track to begin.")
