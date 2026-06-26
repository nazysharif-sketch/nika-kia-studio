import streamlit as st
import replicate
import os

# Set up your page layout and studio title
st.set_page_config(page_title="Nika & Kia Studio 🎤", layout="wide")
st.title("Nika & Kia Studio 🎤")
st.subheader("Advanced Lip-Sync & Humanization Terminal")

# Sidebar for API key authentication
with st.sidebar:
    st.header("Authentication")
    replicate_api_token = st.text_input("Enter Replicate API Token:", type="password")
    if replicate_api_token:
        os.environ["REPLICATE_API_TOKEN"] = replicate_api_token
        st.success("API Token locked in!")
    else:
        st.warning("Please enter your token to activate the studio backend.")

# Asset upload terminal zones
st.header("Humanization Engine")

# --- Sliders aligned perfectly to your original layout ---
lip_sharpness = st.slider("Lip Sync Sharpness Multiplier", min_value=1, max_value=100, value=100, step=1)
expression_intensity = st.slider("Expression Intensity", min_value=0, max_value=100, value=45, step=1)

st.checkbox("Natural Blink Engine", value=True)
st.checkbox("Micro Gaze Humanization", value=True)

singer1 = st.file_uploader("Upload Character Portrait (JPG/PNG):", type=["jpg", "jpeg", "png"])
audio_track = st.file_uploader("Upload Audio Track (MP3/WAV):", type=["mp3", "wav"])

# Trigger generation pipeline
if st.button("🚀 GENERATE MUSIC VIDEO"):
    if not replicate_api_token:
        st.error("Authentication Error: Missing API Token in the sidebar.")
    elif not singer1 or not audio_track:
        st.error("Asset Error: Both a character portrait and an audio track are required.")
    else:
        st.warning("Connecting to Replicate servers... Processing humanized lip-sync animation.")
        
        try:
            # Initializes the official Replicate client
            client = replicate.Client(api_token=replicate_api_token)
            
            # Triggers the premium VEED Fabric image-to-video lipsync engine
            output = client.run(
                "veed/fabric-1.0",
                input={
                    "audio": audio_track,
                    "image": singer1
                }
            )

            st.success("Render Complete!")
            
            # Centers the video layout beautifully and dynamically frames it
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                st.video(output.url)

        except Exception as e:
            st.error(f"Something went wrong during generation: {e}")
