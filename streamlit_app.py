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

st.subheader("💙 BFF Box")

bff_box = st.text_area(
    "💙 Tell your BFF what's on your mind...",
    placeholder="""Example:

I want Nika to feel hopeful rather than sad.
She has just arrived in Bora Bora.
She starts singing softly while watching the sunset.
I want the audience to feel peaceful.""",
    height=180
)

st.divider()
def get_performance_energy_prompt(energy=50):
    value = int(energy)

    if value <= 20:
        return """
Minimal body movement.
Natural breathing only.
Tiny shoulder motion.
Very subtle head movement.
No dramatic gestures.
"""

    if value <= 50:
        return """
Natural singer body movement.
Gentle weight shifts between both feet.
Relaxed knees.
Soft shoulder movement with breathing.
Small head movement following the melody.
Occasional subtle hand movement.
Never appear frozen.
"""

    if value <= 80:
        return """
Professional live singer movement.
Continuous natural body movement.
Gentle hip sway following the rhythm.
Natural weight transfer between feet.
Relaxed knees.
Soft torso movement.
Shoulders move naturally with breathing.
Free hand moves with elegant wrist and finger gestures.
Microphone hand subtly adjusts grip.
Occasionally tilt the microphone stand a few degrees during emotional phrases.
Never appear stiff or frozen.
"""

    return """
High-energy concert performance.
Strong natural stage presence.
Continuous full-body movement.
Clear hip sway and weight shifts.
Expressive shoulders and torso movement.
Both arms move naturally with the music.
Free hand uses elegant emotional gestures.
Microphone hand occasionally tilts the microphone stand.
During high notes, lift chin slightly, tilt head back gently, close eyes naturally, then return smoothly.
Powerful but elegant. Never exaggerated.
"""
lip_sharpness = st.slider("👄 Lip Sync Sharpness", 1, 100, 70)
expression_intensity = st.slider("😊 Expression Intensity", 0, 100, 45)
performance_energy = st.slider("🎭 Performance Energy", 0, 100, 60)
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
    preview_ratio = "16 / 9"

elif output_format == "📷 Instagram Post":
    preview_ratio = "1 / 1"

elif output_format == "📸 Instagram Portrait":
    preview_ratio = "4 / 5"

if st.button("🚀 GENERATE MUSIC VIDEO"):
    if not replicate_api_token:
        st.error("Authentication Error: Missing API Token in the sidebar.")
    elif not singer1 or not audio_track:
        st.error("Asset Error: Both a character portrait and an audio track are required.")
    else:
        st.warning("Connecting to Replicate servers... Processing humanized lip-sync animation.")

        try:
            movement_prompt = get_performance_energy_prompt(performance_energy)

            final_prompt = f"""
Performance Direction:
{performance_direction}

BFF Notes:
{bff_box}

Movement:
{movement_prompt}

Lip Sync Sharpness: {lip_sharpness}
Expression Intensity: {expression_intensity}
Natural Blink: {natural_blink}
Micro Gaze: {micro_gaze}
"""

            client = replicate.Client(api_token=replicate_api_token)

            output = client.run(
                "veed/fabric-1.0",
                input={
                    "audio": audio_track,
                    "image": singer1,
                    "prompt": final_prompt,
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
                        aspect-ratio: {preview_ratio};
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

