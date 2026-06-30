import streamlit as st
import replicate

st.title("Nika AI Performance Dashboard 🎬")
st.subheader("Option A: Expression Engine")

singer1 = st.file_uploader("Upload Nika's Reference Image", type=["jpg", "png", "jpeg"])
audio_track = st.file_uploader("Upload Persian Humming Audio Track", type=["mp3", "wav", "mp4"])

# 🛠️ Keep our direct movement style dynamics bar!
motion_dynamics = st.slider(
    "Performance Movement Dynamics", 
    min_value=1.8,  # The model's strict hardware minimum limit
    max_value=3.2,  # The model's strict hardware maximum limit
    value=2.3, 
    step=0.1
)

if st.button("Generate Performance"):
    if singer1 and audio_track:
        with st.spinner("Processing performance physics..."):
            
            # 2. Fire the code matching the exact official endpoint specifications
            output = replicate.run(
                "okaris/live-portrait:8be2edeab144ba0865f9fa84168f621ee417a2003db947802f900519f7c43300",
                input={
                    "source_image": singer1,
                    "driving_video": audio_track, # Passes your file cleanly into the media channel
                    "flag_do_crop": True,
                    "flag_remap": True,
                    "scale": motion_dynamics,     # Your working master slider!
                    "vx_ratio": 0,
                    "vy_ratio": -0.125
                }
            )
            
            st.video(output)
    else:
        st.warning("Please upload both an image and an audio track to begin.")
