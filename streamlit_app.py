import streamlit as st
import replicate

st.title("Nika AI Performance Dashboard 🎬")
st.subheader("Option A: LivePortrait Custom Dynamics")

singer1 = st.file_uploader("Upload Nika's Reference Image", type=["jpg", "png", "jpeg"])
audio_track = st.file_uploader("Upload Persian Humming Audio Track", type=["mp3", "wav", "mp4"])

# 🎛️ BACK ON SCREEN: Your master performance control slider!
motion_dynamics = st.slider(
    "Performance Movement Dynamics", 
    min_value=1.5, 
    max_value=3.5, 
    value=2.3, 
    step=0.1,
    help="Set to 1.8 to widen the frame and give her space to unleash her arm gestures!"
)

if st.button("Generate Performance"):
    if singer1 and audio_track:
        with st.spinner("Processing performance physics with custom slider settings..."):
            
            # This calls the live-portrait schema with the exact variables the server expects
            output = replicate.run(
                "fofr/live-portrait:cd7ed192aa7cf6687d77c6494a2027ca1a76d06f524a02f5faee1727280c6a9e",
                input={
                    "face_image": singer1,
                    "driving_video": audio_track,  
                    
                    # 🎯 Maps your dynamic slider directly to the engine scale!
                    "live_portrait_scale": motion_dynamics,  
                    "live_portrait_vy_ratio": -0.125,
                    "live_portrait_stitching": True
                }
            )
            
            # Displays the final processed video arrays
            if isinstance(output, list) and len(output) > 0:
                st.video(output[0])
            else:
                st.video(output)
    else:
        st.warning("Please upload both an image and an audio track to begin.")
