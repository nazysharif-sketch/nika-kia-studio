import streamlit as st
import replicate
import os

st.set_page_config(page_title="Nika & Kia Studio 🎤", layout="wide")

st.title("Nika & Kia Studio 🎤")
st.subheader("Advanced Lip-Sync & Humanization Terminal")

with st.sidebar:
    st.header("Authentication")
    replicate_api_token = st.text_input("Enter Replicate API Token:", type="password")

    if replicate_api_token:
        os.environ["REPLICATE_API_TOKEN"] = replicate_api_token
        st.success("API Token locked in!")
    else:
        st.warning("Enter token to activate backend.")

st.header("🎬 Performance Studio")

singer1 = st.file_uploader("📷 Upload Character Portrait", type=["jpg", "jpeg", "png"])
audio_track = st.file_uploader("🎵 Upload Audio Track", type=["mp3", "wav"])

st.divider()

performance_direction = st.text_area(
    "🎭 Performance Direction",
    placeholder="Example: Emotional Persian ballad, soft eye contact, natural blinking, subtle sadness, gentle breathing, restrained smile...",
    height=120,
)

st.divider()

lip_sharpness = st.slider("👄 Lip Sync Sharpness", 1, 100, 70)
expression_intensity = st.slider("😊 Expression Intensity", 0, 100, 45)

natural_blink = st.checkbox("👀 Natural Blink Engine", value=True)
micro_gaze = st.checkbox("✨ Micro Gaze Humanization", value=True)

output_format = st.selectbox(
    "🎯 Publish To",
    [
        "📱 Instagram Reels / TikTok",
        "▶️ YouTube Shorts",
        "📺 YouTube Landscape",
        "📷 Instagram Post",
        "📸 Instagram Portrait"
    ]
)

if output_format in [
    "📱 Instagram Reels / TikTok",
    "▶️ YouTube Shorts"
]:
    preview_ratio = "9 / 16"

elif output_format == "📺 YouTube Landscape":
    ratio_css = "16 / 9"

elif output_format == "📷 Instagram Post":
    ratio_css = "1 / 1"

elif output_format == "📸 Instagram Portrait":
    ratio_css = "4 / 5"

if st.button("🚀 GENERATE MUSIC VIDEO"):
    if not replicate_api_token:
        st.error("Authentication Error: Missing API Token in the sidebar.")
    elif not singer1 or not audio_track:
        st.error("Asset Error: Both a character portrait and an audio track are required.")
    else:
        st.warning("Connecting to Replicate servers... Processing humanized lip-sync animation.")

        try:
            client = replicate.Client(api_token=replicate_api_token)

            output = client.run(
                "veed/fabric-1.0",
                input={
                    "audio": audio_track,
                    "image": singer1,
                }
            )

            video_url = output.url if hasattr(output, "url") else str(output)

            st.success("Render Complete!")

            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        max-width: 360px;
                        margin: 0 auto;
                        aspect-ratio: {ratio_css};
                        overflow: hidden;
                        border-radius: 18px;
                        background: #111;
                        box-shadow: 0 8px 30px rgba(0,0,0,0.35);
                    ">
                        <video src="{video_url}" controls
                        style="
                            width: 100%;
                            height: 100%;
                            object-fit: cover;
                            background: #111;
                        "></video>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(f"[Open video result]({video_url})")

        except Exception as e:
            st.error(f"Something went wrong during generation: {e}")
