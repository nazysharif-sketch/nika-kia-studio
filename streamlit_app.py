import streamlit as st
import replicate
import os

# Initialize the authenticated Replicate client safely using your vault secret
client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

st.set_page_config(page_title="Nika & Kia Studio", page_icon="🎤", layout="wide")
st.title("Nika & Kia Studio 🎤")
st.subheader("Advanced Lip-Sync & Humanization Terminal")

# --- 2. TOP BAR: MODE SELECTOR ---
mode = st.radio("Project Mode", ["Solo Mode", "Duet Mode"], horizontal=True)

# --- 3. SIDEBAR / UPLOADERS ---
st.sidebar.header("Upload Media Assets")
singer1 = st.sidebar.file_uploader("Upload Singer 1 Image", type=["jpg", "jpeg", "png"])
audio_track = st.sidebar.file_uploader("Upload Audio Track", type=["wav", "mp3"])

# --- 4. HUMANIZATION ENGINE OPTIONS ---
st.header("Humanization Engine")
st.slider("Lip Sync Sharpness Multiplier", min_value=0, max_value=100, value=100)
st.slider("Expression Intensity", min_value=0, max_value=100, value=45)
st.checkbox("Natural Blink Engine", value=True)
st.checkbox("Micro Gaze Humanization", value=True)
st.checkbox("Character Inter-Eye Contact (Duet Only)", value=False)

# --- 5. THE MAIN GENERATE BUTTON ---
if st.button("🚀 GENERATE MUSIC VIDEO", use_container_width=True):
    if not singer1 or not audio_track:
        st.error("Missing Assets! Please make sure you have uploaded at least Singer 1's image and an audio track.")
    else:
        st.warning("Connecting to Replicate servers... Processing humanized lip-sync animation.")
        
        # Rewind file buffers so Replicate reads them cleanly from the start
        singer1.seek(0)
        audio_track.seek(0)
        
        try:
            # Re-ordered keys to strictly match Replicate's official endpoint blueprint
            output = client.run(
                "veed/fabric-1.0",
                input={
                    "audio": audio_track,
                    "image": singer1
                }
            )

            st.success("Render Complete!")
            # Converts the Replicate file object into a readable web link for Streamlit
            st.video(output.url)

        except Exception as e:
            st.error(f"Something went wrong during generation: {e}")

            st.success("Render Complete!")
            st.video(output)

        except Exception as e:
            st.error(f"Something went wrong during generation: {e}")
